<template>
  <div class="course-detail">
    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container">
      <div class="loading-spinner-large"></div>
      <p>Carregando detalhes do curso...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <div class="error-icon">❌</div>
      <h2>Erro ao carregar curso</h2>
      <p>{{ error }}</p>
      <div class="error-actions">
        <button class="btn btn-primary" @click="loadCursoData">
          🔄 Tentar Novamente
        </button>
        <router-link to="/" class="btn btn-secondary">
          ← Voltar ao Dashboard
        </router-link>
      </div>
    </div>

    <!-- Course Content -->
    <div v-else-if="curso" class="course-content">
      <!-- Header -->
      <header class="course-header">
        <div class="header-nav">
          <router-link to="/" class="back-btn">
            ← Voltar
          </router-link>

        </div>
        
        <div class="course-title-section">
          <h1 class="course-title">{{ curso.titulo }}</h1>
          <div class="course-meta">
            <span class="meta-item">
              📚 {{ curso.total_aulas }} aulas total
            </span>
            <span class="meta-item">
              ✅ {{ curso.aulas_concluidas }} concluídas
            </span>
            <span class="meta-item">
              🗓️ Criado em {{ formatDate(curso.created_at) }}
            </span>
          </div>
          
          <div class="course-link" v-if="curso.link">
            <a 
              :href="curso.link" 
              target="_blank" 
              class="external-link"
            >
              🔗 Acessar Curso Online
            </a>
          </div>
        </div>
        
        <div class="progress-section">
          <ProgressBar 
            :percentage="curso.progresso || 0"
            label="Progresso Geral"
          />
        </div>
      </header>

      <!-- Main Content -->
      <main class="main-content">
        <!-- Lessons Section -->
        <section class="lessons-section">
          <div class="section-header">
            <h2 class="section-title">
              📋 Controle de Aulas
            </h2>
            <div class="lessons-controls">
              <button 
                class="btn btn-outline"
                @click="toggleAllLessons(false)"
                :disabled="isUpdating"
              >
                ❌ Desmarcar Todas
              </button>
              <button 
                class="btn btn-outline"
                @click="toggleAllLessons(true)"
                :disabled="isUpdating"
              >
                ✅ Marcar Todas
              </button>
            </div>
          </div>
          
          <div class="lessons-grid">
            <div 
              v-for="numeroAula in curso.total_aulas"
              :key="numeroAula"
              class="lesson-item"
              :class="{ 
                'completed': isLessonCompleted(numeroAula),
                'updating': updatingLessons.includes(numeroAula)
              }"
            >
              <label class="lesson-checkbox">
                <input 
                  type="checkbox"
                  :checked="isLessonCompleted(numeroAula)"
                  @change="toggleLesson(numeroAula)"
                  :disabled="updatingLessons.includes(numeroAula)"
                />
                <span class="checkbox-custom"></span>
                <span class="lesson-text">
                  Aula {{ numeroAula }}
                </span>
              </label>
              
              <div 
                v-if="updatingLessons.includes(numeroAula)" 
                class="lesson-spinner"
              ></div>
            </div>
          </div>
          
          <div class="lessons-summary">
            <div class="summary-stats">
              <span class="summary-item">
                📊 {{ curso.aulas_concluidas }}/{{ curso.total_aulas }} concluídas
              </span>
              <span class="summary-item">
                🎯 {{ curso.progresso.toFixed(1) }}% completado
              </span>
              <span class="summary-item">
                ⏱️ {{ remainingLessons }} aulas restantes
              </span>
            </div>
          </div>
        </section>

        <!-- Notes Section -->
        <section class="notes-section">
          <div class="section-header">
            <h2 class="section-title">
              📝 Anotações
            </h2>
            <div class="notes-controls">
              <button 
                v-if="isEditingNotes"
                class="btn btn-primary"
                @click="saveNotes"
                :disabled="isSavingNotes"
              >
                <span v-if="isSavingNotes" class="loading-spinner"></span>
                {{ isSavingNotes ? 'Salvando...' : 'Salvar' }}
              </button>
              <button 
                v-if="isEditingNotes"
                class="btn btn-secondary"
                @click="cancelEditNotes"
                :disabled="isSavingNotes"
              >
                Cancelar
              </button>
              <button 
                v-if="!isEditingNotes"
                class="btn btn-outline"
                @click="startEditNotes"
              >
                ✏️ Editar
              </button>
            </div>
          </div>
          
          <div class="notes-content">
            <div v-if="!isEditingNotes" class="notes-display">
              <p v-if="curso.anotacoes" class="notes-text">
                {{ curso.anotacoes }}
              </p>
              <p v-else class="no-notes">
                Nenhuma anotação adicionada ainda.
                <button class="link-btn" @click="startEditNotes">
                  Clique aqui para adicionar
                </button>
              </p>
            </div>
            
            <div v-if="isEditingNotes" class="notes-editor">
              <textarea
                ref="notesTextarea"
                v-model="editingNotes"
                class="notes-textarea"
                placeholder="Digite suas anotações sobre este curso..."
                rows="6"
                maxlength="1000"
              ></textarea>
              <div class="character-count">
                {{ editingNotes.length }}/1000 caracteres
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>

    <!-- Notifications -->
    <div v-if="notification" class="notification" :class="notification.type">
      {{ notification.message }}
    </div>
  </div>
</template>

<script>
import ProgressBar from '../components/ProgressBar.vue'
import apiService from '../services/api.js'

export default {
  name: 'CourseDetailView',
  components: {
    ProgressBar
  },
  data() {
    return {
      curso: null,
      isLoading: false,
      isUpdating: false,
      isSavingNotes: false,
      isEditingNotes: false,
      editingNotes: '',
      originalNotes: '',
      updatingLessons: [],
      error: null,
      notification: null
    }
  },
  computed: {
    courseId() {
      return parseInt(this.$route.params.id)
    },
    remainingLessons() {
      if (!this.curso) return 0
      return this.curso.total_aulas - this.curso.aulas_concluidas
    }
  },
  async mounted() {
    await this.loadCursoData()
  },
  methods: {
    async loadCursoData() {
      if (!this.courseId) {
        this.error = 'ID do curso inválido'
        return
      }

      this.isLoading = true
      this.error = null

      try {
        const response = await apiService.getCurso(this.courseId)
        this.curso = response.data
        this.originalNotes = this.curso.anotacoes || ''
      } catch (error) {
        console.error('Erro ao carregar curso:', error)
        this.error = error.message || 'Erro ao carregar dados do curso'
      } finally {
        this.isLoading = false
      }
    },

    isLessonCompleted(numeroAula) {
      return this.curso?.aulas_concluidas_list?.includes(numeroAula) || false
    },

    async toggleLesson(numeroAula) {
      if (this.updatingLessons.includes(numeroAula)) return

      const isCurrentlyCompleted = this.isLessonCompleted(numeroAula)
      const newStatus = !isCurrentlyCompleted

      // Adicionar à lista de aulas sendo atualizadas
      this.updatingLessons.push(numeroAula)

      try {
        const response = await apiService.toggleAula(
          this.courseId, 
          numeroAula, 
          newStatus
        )

        // Atualizar dados localmente com a resposta da API
        this.curso.aulas_concluidas = response.data.total_aulas_concluidas
        this.curso.aulas_concluidas_list = response.data.aulas_concluidas_list
        this.curso.progresso = response.data.progresso

        this.showNotification(
          `Aula ${numeroAula} ${newStatus ? 'marcada como concluída' : 'desmarcada'}!`,
          'success'
        )
      } catch (error) {
        console.error('Erro ao atualizar aula:', error)
        this.showNotification(
          error.message || 'Erro ao atualizar aula',
          'error'
        )
      } finally {
        // Remover da lista de aulas sendo atualizadas
        const index = this.updatingLessons.indexOf(numeroAula)
        if (index > -1) {
          this.updatingLessons.splice(index, 1)
        }
      }
    },

    async toggleAllLessons(markAsCompleted) {
      if (this.isUpdating) return

      this.isUpdating = true

      try {
        const promises = []
        
        for (let numeroAula = 1; numeroAula <= this.curso.total_aulas; numeroAula++) {
          const isCurrentlyCompleted = this.isLessonCompleted(numeroAula)
          
          // Só fazer a requisição se o status for diferente do desejado
          if (isCurrentlyCompleted !== markAsCompleted) {
            promises.push(
              apiService.toggleAula(this.courseId, numeroAula, markAsCompleted)
            )
          }
        }

        if (promises.length > 0) {
          const responses = await Promise.all(promises)
          
          // Update local state based on API responses
          // Use the last response to get the most up-to-date course data
          if (responses.length > 0) {
            const lastResponse = responses[responses.length - 1]
            this.curso.aulas_concluidas = lastResponse.data.total_aulas_concluidas
            this.curso.aulas_concluidas_list = lastResponse.data.aulas_concluidas_list
            this.curso.progresso = lastResponse.data.progresso
          }
          
          this.showNotification(
            `Todas as aulas foram ${markAsCompleted ? 'marcadas como concluídas' : 'desmarcadas'}!`,
            'success'
          )
        } else {
          this.showNotification('Nenhuma alteração necessária', 'info')
        }
      } catch (error) {
        console.error('Erro ao atualizar todas as aulas:', error)
        this.showNotification('Erro ao atualizar aulas', 'error')
      } finally {
        this.isUpdating = false
      }
    },

    startEditNotes() {
      this.isEditingNotes = true
      this.editingNotes = this.curso.anotacoes || ''
      
      // Focus no textarea após o próximo tick
      this.$nextTick(() => {
        if (this.$refs.notesTextarea) {
          this.$refs.notesTextarea.focus()
        }
      })
    },

    cancelEditNotes() {
      this.isEditingNotes = false
      this.editingNotes = this.originalNotes
    },

    async saveNotes() {
      this.isSavingNotes = true

      try {
        const response = await apiService.updateCurso(this.courseId, {
          anotacoes: this.editingNotes.trim()
        })

        // Atualizar dados localmente
        this.curso.anotacoes = response.data.anotacoes
        this.originalNotes = this.curso.anotacoes
        this.isEditingNotes = false

        this.showNotification('Anotações salvas com sucesso!', 'success')
      } catch (error) {
        console.error('Erro ao salvar anotações:', error)
        this.showNotification(
          error.message || 'Erro ao salvar anotações',
          'error'
        )
      } finally {
        this.isSavingNotes = false
      }
    },

    formatDate(dateString) {
      if (!dateString) return ''
      try {
        const date = new Date(dateString)
        return date.toLocaleDateString('pt-BR', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric'
        })
      } catch {
        return dateString
      }
    },

    showNotification(message, type = 'info') {
      this.notification = { message, type }
      setTimeout(() => {
        this.notification = null
      }, 4000)
    }
  }
}
</script>

<style scoped>
.course-detail {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60vh;
  gap: 20px;
  text-align: center;
}

.error-container {
  color: #ef4444;
}

.error-icon {
  font-size: 4rem;
}

.error-actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

.loading-spinner-large {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.course-content {
  max-width: 1000px;
  margin: 0 auto;
}

.course-header {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 24px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.header-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.back-btn {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: #eff6ff;
}

.course-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 16px 0;
  line-height: 1.2;
}

.course-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  margin-bottom: 16px;
}

.meta-item {
  color: #6b7280;
  font-weight: 500;
}

.external-link {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
  font-size: 1.1rem;
  padding: 8px 0;
  display: inline-block;
  transition: color 0.2s ease;
}

.external-link:hover {
  color: #2563eb;
}

.progress-section {
  margin-top: 24px;
}

.main-content {
  display: grid;
  gap: 24px;
  grid-template-columns: 1fr;
}

.lessons-section,
.notes-section {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 32px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.lessons-controls,
.notes-controls {
  display: flex;
  gap: 8px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn-secondary {
  background: #6b7280;
  color: white;
}

.btn-outline {
  background: transparent;
  border: 1px solid #d1d5db;
  color: #6b7280;
}

.btn-outline:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #9ca3af;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-icon.rotating {
  animation: spin 1s linear infinite;
}

.lessons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 24px;
}

.lesson-item {
  background: #f9fafb;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  transition: all 0.3s ease;
  position: relative;
}

.lesson-item:hover {
  background: #f3f4f6;
  border-color: #d1d5db;
}

.lesson-item.completed {
  background: #ecfdf5;
  border-color: #10b981;
}

.lesson-item.updating {
  opacity: 0.7;
  pointer-events: none;
}

.lesson-checkbox {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  width: 100%;
}

.lesson-checkbox input[type="checkbox"] {
  display: none;
}

.checkbox-custom {
  width: 20px;
  height: 20px;
  border: 2px solid #d1d5db;
  border-radius: 4px;
  background: white;
  position: relative;
  transition: all 0.2s ease;
}

.lesson-checkbox input:checked + .checkbox-custom {
  background: #10b981;
  border-color: #10b981;
}

.lesson-checkbox input:checked + .checkbox-custom::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-weight: bold;
  font-size: 14px;
}

.lesson-text {
  font-weight: 500;
  color: #374151;
  user-select: none;
}

.lesson-spinner {
  position: absolute;
  top: 50%;
  right: 12px;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  border: 2px solid #e5e7eb;
  border-top: 2px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.lessons-summary {
  border-top: 1px solid #e5e7eb;
  padding-top: 20px;
}

.summary-stats {
  display: flex;
  justify-content: center;
  gap: 32px;
  flex-wrap: wrap;
}

.summary-item {
  color: #6b7280;
  font-weight: 500;
  text-align: center;
}

.notes-content {
  min-height: 120px;
}

.notes-display {
  padding: 16px;
  background: #f9fafb;
  border-radius: 8px;
  min-height: 120px;
}

.notes-text {
  color: #374151;
  line-height: 1.6;
  margin: 0;
  white-space: pre-wrap;
}

.no-notes {
  color: #9ca3af;
  text-align: center;
  margin: 40px 0;
}

.link-btn {
  background: none;
  border: none;
  color: #3b82f6;
  text-decoration: underline;
  cursor: pointer;
  font: inherit;
}

.notes-textarea {
  width: 100%;
  padding: 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-family: inherit;
  font-size: 1rem;
  line-height: 1.5;
  resize: vertical;
  min-height: 120px;
}

.notes-textarea:focus {
  outline: none;
  border-color: #3b82f6;
}

.character-count {
  text-align: right;
  color: #9ca3af;
  font-size: 0.875rem;
  margin-top: 8px;
}

.notification {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 16px 20px;
  border-radius: 8px;
  color: white;
  font-weight: 500;
  z-index: 1001;
  animation: slideIn 0.3s ease;
}

.notification.success {
  background: #10b981;
}

.notification.error {
  background: #ef4444;
}

.notification.info {
  background: #3b82f6;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Responsividade */
@media (max-width: 768px) {
  .course-detail {
    padding: 12px;
  }
  
  .course-header,
  .lessons-section,
  .notes-section {
    padding: 20px;
  }
  
  .course-title {
    font-size: 2rem;
  }
  
  .course-meta {
    flex-direction: column;
    gap: 8px;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .lessons-grid {
    grid-template-columns: 1fr;
  }
  
  .summary-stats {
    flex-direction: column;
    gap: 12px;
  }
  
  .header-nav {
    flex-wrap: wrap;
  }
}
</style>