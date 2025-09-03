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
        // Create an array of lessons to update
        const aulasToUpdate = []
        
        for (let numeroAula = 1; numeroAula <= this.curso.total_aulas; numeroAula++) {
          const isCurrentlyCompleted = this.isLessonCompleted(numeroAula)
          
          // Only update if the current status is different from desired status
          if (isCurrentlyCompleted !== markAsCompleted) {
            aulasToUpdate.push({
              numero_aula: numeroAula,
              concluida: markAsCompleted
            })
            // Add to updating lessons list for UI feedback
            this.updatingLessons.push(numeroAula)
          }
        }

        if (aulasToUpdate.length > 0) {
          try {
            // Try to use the batch endpoint first (more efficient)
            const response = await apiService.batchToggleAulas(this.courseId, aulasToUpdate)
            
            // Update local state with the response
            this.curso.aulas_concluidas = response.data.total_aulas_concluidas
            this.curso.aulas_concluidas_list = response.data.aulas_concluidas_list
            this.curso.progresso = response.data.progresso
            
            this.showNotification(
              `Todas as aulas foram ${markAsCompleted ? 'marcadas como concluídas' : 'desmarcadas'}!`,
              'success'
            )
          } catch (batchError) {
            // If batch endpoint fails, fall back to individual calls
            console.warn('Batch endpoint failed, falling back to individual calls:', batchError)
            
            // Process lessons in smaller batches to avoid overwhelming the server
            const batchSize = 5
            const batches = []
            
            for (let i = 0; i < aulasToUpdate.length; i += batchSize) {
              batches.push(aulasToUpdate.slice(i, i + batchSize))
            }
            
            // Process each batch sequentially
            let lastResponse = null
            let hasError = false
            
            for (const batch of batches) {
              try {
                // Create promises for all lessons in this batch
                const promises = batch.map(aula => 
                  apiService.toggleAula(this.courseId, aula.numero_aula, aula.concluida)
                )
                
                // Wait for all promises in this batch to complete
                const responses = await Promise.all(promises)
                lastResponse = responses[responses.length - 1] // Use the last response for final state
              } catch (batchError) {
                console.error('Error processing batch:', batchError)
                hasError = true
                // Continue with other batches
              }
            }
            
            // Update local state with the final response if we have one
            if (lastResponse) {
              this.curso.aulas_concluidas = lastResponse.data.total_aulas_concluidas
              this.curso.aulas_concluidas_list = lastResponse.data.aulas_concluidas_list
              this.curso.progresso = lastResponse.data.progresso
            }
            
            if (hasError) {
              this.showNotification(
                `Alguns erros ocorreram ao atualizar as aulas. Verifique o console para mais detalhes.`,
                'error'
              )
            } else {
              this.showNotification(
                `Todas as aulas foram ${markAsCompleted ? 'marcadas como concluídas' : 'desmarcadas'}!`,
                'success'
              )
            }
          }
        } else {
          this.showNotification('Nenhuma alteração necessária', 'info')
        }
      } catch (error) {
        console.error('Erro ao atualizar todas as aulas:', error)
        this.showNotification('Erro ao atualizar aulas: ' + (error.message || 'Erro desconhecido'), 'error')
      } finally {
        // Clear the updating lessons list
        this.updatingLessons = []
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

/* Dark mode styles */
.dark-mode .course-detail {
  background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
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

.dark-mode .loading-spinner-large {
  border-color: #4b5563;
  border-top-color: #3b82f6;
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

.dark-mode .course-header {
  background: rgba(31, 41, 55, 0.95);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
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

.dark-mode .back-btn {
  color: #60a5fa;
}

.back-btn:hover {
  background: #eff6ff;
}

.dark-mode .back-btn:hover {
  background: #374151;
}

.course-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 16px 0;
  line-height: 1.2;
}

.dark-mode .course-title {
  color: #f9fafb;
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

.dark-mode .meta-item {
  color: #d1d5db;
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

.dark-mode .external-link {
  color: #60a5fa;
}

.external-link:hover {
  color: #2563eb;
}

.dark-mode .external-link:hover {
  color: #93c5fd;
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

.dark-mode .lessons-section,
.dark-mode .notes-section {
  background: rgba(31, 41, 55, 0.95);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
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

.dark-mode .section-title {
  color: #f9fafb;
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

.dark-mode .btn-outline {
  border-color: #4b5563;
  color: #d1d5db;
}

.btn-outline:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #9ca3af;
}

.dark-mode .btn-outline:hover:not(:disabled) {
  background: #374151;
  border-color: #6b7280;
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

.dark-mode .lesson-item {
  background: #374151;
  border-color: #4b5563;
}

.lesson-item:hover {
  background: #f3f4f6;
  border-color: #d1d5db;
}

.dark-mode .lesson-item:hover {
  background: #4b5563;
  border-color: #6b7280;
}

.lesson-item.completed {
  background: #ecfdf5;
  border-color: #10b981;
}

.dark-mode .lesson-item.completed {
  background: #064e3b;
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

.dark-mode .checkbox-custom {
  border-color: #4b5563;
  background: #1f2937;
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

.dark-mode .lesson-text {
  color: #f9fafb;
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

.dark-mode .lesson-spinner {
  border-color: #4b5563;
  border-top-color: #3b82f6;
}

.lessons-summary {
  border-top: 1px solid #e5e7eb;
  padding-top: 20px;
}

.dark-mode .lessons-summary {
  border-top-color: #4b5563;
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

.dark-mode .summary-item {
  color: #d1d5db;
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

.dark-mode .notes-display {
  background: #374151;
}

.notes-text {
  color: #374151;
  line-height: 1.6;
  margin: 0;
  white-space: pre-wrap;
}

.dark-mode .notes-text {
  color: #f9fafb;
}

.no-notes {
  color: #9ca3af;
  text-align: center;
  margin: 40px 0;
}

.dark-mode .no-notes {
  color: #9ca3af;
}

.link-btn {
  background: none;
  border: none;
  color: #3b82f6;
  text-decoration: underline;
  cursor: pointer;
  font: inherit;
}

.dark-mode .link-btn {
  color: #60a5fa;
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
  background: white;
  color: #1f2937;
}

.dark-mode .notes-textarea {
  border-color: #4b5563;
  background: #1f2937;
  color: #f9fafb;
}

.notes-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.dark-mode .notes-textarea:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
}

.character-count {
  text-align: right;
  color: #9ca3af;
  font-size: 0.875rem;
  margin-top: 8px;
}

.dark-mode .character-count {
  color: #9ca3af;
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