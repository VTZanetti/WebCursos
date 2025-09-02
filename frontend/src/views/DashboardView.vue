<template>
  <div class="dashboard">
    <!-- Header do Dashboard -->
    <header class="dashboard-header">
      <div class="header-content">
        <div class="header-info">
          <h1 class="dashboard-title">
            📚 WebCurso Dashboard
          </h1>
          <p class="dashboard-subtitle">
            Gerencie seu progresso nos cursos
          </p>
        </div>
        
        <div class="header-actions">
          <button 
            class="btn btn-primary"
            @click="openCreateModal"
            :disabled="isLoading"
          >
            <span class="btn-icon">➕</span>
            Novo Curso
          </button>
          

        </div>
      </div>
    </header>

    <!-- Estatísticas -->
    <section class="stats-section" v-if="stats">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">📊</div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.total_cursos }}</div>
            <div class="stat-label">Total de Cursos</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">✅</div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.total_aulas_concluidas }}</div>
            <div class="stat-label">Aulas Concluídas</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">🎯</div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.total_aulas_disponiveis }}</div>
            <div class="stat-label">Total de Aulas</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">📈</div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.progresso_geral }}%</div>
            <div class="stat-label">Progresso Geral</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Filtros e Busca -->
    <section class="filters-section">
      <div class="filters-container">
        <div class="search-box">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="🔍 Buscar cursos..."
            class="search-input"
          />
        </div>
        
        <div class="filter-buttons">
          <button
            v-for="filter in filters"
            :key="filter.key"
            class="filter-btn"
            :class="{ 'active': activeFilter === filter.key }"
            @click="activeFilter = filter.key"
          >
            {{ filter.label }}
          </button>
        </div>
      </div>
    </section>

    <!-- Lista de Cursos -->
    <main class="courses-section">
      <!-- Loading State -->
      <div v-if="isLoading && cursos.length === 0" class="loading-container">
        <div class="loading-spinner-large"></div>
        <p>Carregando cursos...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="!isLoading && cursos.length === 0" class="empty-state">
        <div class="empty-icon">📚</div>
        <h3>Nenhum curso encontrado</h3>
        <p>Comece criando seu primeiro curso!</p>
        <button class="btn btn-primary" @click="openCreateModal">
          ➕ Criar Primeiro Curso
        </button>
      </div>

      <!-- Courses Grid -->
      <div v-else class="courses-grid">
        <CourseCard
          v-for="curso in filteredCursos"
          :key="curso.id"
          :curso="curso"
          @edit="openEditModal"
          @delete="confirmDeleteCurso"
        />
      </div>

      <!-- No Results -->
      <div v-if="filteredCursos.length === 0 && cursos.length > 0" class="no-results">
        <div class="no-results-icon">🔍</div>
        <h3>Nenhum curso encontrado</h3>
        <p>Tente ajustar os filtros de busca</p>
      </div>
    </main>

    <!-- Modal de Curso -->
    <CourseModal
      :is-visible="isModalVisible"
      :curso="selectedCurso"
      @close="closeModal"
      @save="handleSaveCurso"
    />

    <!-- Confirmation Modal -->
    <ConfirmationModal
      :visible="showDeleteModal"
      :titulo="'Confirmar Exclusão'"
      :mensagem="`Tem certeza que deseja excluir o curso?`"
      :aviso-mensagem="'Esta ação não pode ser desfeita e todas as aulas concluídas serão perdidas.'"
      :nome-item="cursoToDelete?.titulo"
      :texto-confirmar="'Excluir'"
      :texto-cancelar="'Cancelar'"
      :is-processing="isDeletingCurso"
      @confirm="executeDelete"
      @cancel="cancelDelete"
    />

    <!-- Notifications -->
    <div v-if="notification" class="notification" :class="notification.type">
      {{ notification.message }}
    </div>
  </div>
</template>

<script>
import CourseCard from '../components/CourseCard.vue'
import CourseModal from '../components/CourseModal.vue'
import ConfirmationModal from '../components/ConfirmationModal.vue'
import apiService from '../services/api.js'

export default {
  name: 'DashboardView',
  components: {
    CourseCard,
    CourseModal,
    ConfirmationModal
  },
  data() {
    return {
      cursos: [],
      stats: null,
      isLoading: false,
      isDeletingCurso: false,
      isModalVisible: false,
      showDeleteModal: false,
      selectedCurso: null,
      cursoToDelete: null,
      searchQuery: '',
      activeFilter: 'todos',
      notification: null,
      filters: [
        { key: 'todos', label: 'Todos' },
        { key: 'nao_iniciados', label: 'Não Iniciados' },
        { key: 'em_progresso', label: 'Em Progresso' },
        { key: 'concluidos', label: 'Concluídos' }
      ]
    }
  },
  computed: {
    filteredCursos() {
      let filtered = [...this.cursos]

      // Filtrar por busca
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(curso =>
          curso.titulo.toLowerCase().includes(query) ||
          (curso.anotacoes && curso.anotacoes.toLowerCase().includes(query))
        )
      }

      // Filtrar por status
      switch (this.activeFilter) {
        case 'nao_iniciados':
          filtered = filtered.filter(curso => (curso.progresso || 0) === 0)
          break
        case 'em_progresso':
          filtered = filtered.filter(curso => {
            const progresso = curso.progresso || 0
            return progresso > 0 && progresso < 100
          })
          break
        case 'concluidos':
          filtered = filtered.filter(curso => (curso.progresso || 0) >= 100)
          break
      }

      return filtered
    }
  },
  async mounted() {
    await this.loadDashboardData()
  },
  methods: {
    async loadDashboardData() {
      this.isLoading = true
      
      try {
        // Carregar cursos e estatísticas em paralelo
        const [cursosResponse, statsResponse] = await Promise.all([
          apiService.getCursos(),
          apiService.getStats()
        ])
        
        this.cursos = cursosResponse.data || []
        this.stats = statsResponse.data || null
        
      } catch (error) {
        console.error('Erro ao carregar dashboard:', error)
        this.showNotification('Erro ao carregar dados do dashboard', 'error')
      } finally {
        this.isLoading = false
      }
    },

    openCreateModal() {
      this.selectedCurso = null
      this.isModalVisible = true
    },

    openEditModal(curso) {
      this.selectedCurso = curso
      this.isModalVisible = true
    },

    closeModal() {
      this.isModalVisible = false
      this.selectedCurso = null
    },

    async handleSaveCurso(cursoData) {
      try {
        if (this.selectedCurso?.id) {
          // Editar curso existente
          const response = await apiService.updateCurso(this.selectedCurso.id, cursoData)
          
          // Atualizar na lista local
          const index = this.cursos.findIndex(c => c.id === this.selectedCurso.id)
          if (index !== -1) {
            this.cursos.splice(index, 1, response.data)
          }
          
          this.showNotification('Curso atualizado com sucesso!', 'success')
        } else {
          // Criar novo curso
          const response = await apiService.createCurso(cursoData)
          
          // Adicionar na lista local
          this.cursos.unshift(response.data)
          
          this.showNotification('Curso criado com sucesso!', 'success')
        }
        
        this.closeModal()
        
        // Update statistics immediately
        await this.loadStats()
        
      } catch (error) {
        console.error('Erro ao salvar curso:', error)
        this.showNotification(
          error.message || 'Erro ao salvar curso', 
          'error'
        )
      }
    },

    confirmDeleteCurso(curso) {
      this.cursoToDelete = curso
      this.showDeleteModal = true
    },

    cancelDelete() {
      this.showDeleteModal = false
      this.cursoToDelete = null
    },

    async executeDelete() {
      if (!this.cursoToDelete) return

      this.isDeletingCurso = true
      
      try {
        await apiService.deleteCurso(this.cursoToDelete.id)
        
        // Remover da lista local
        const index = this.cursos.findIndex(c => c.id === this.cursoToDelete.id)
        if (index !== -1) {
          this.cursos.splice(index, 1)
        }
        
        this.showNotification('Curso excluído com sucesso!', 'success')
        this.cancelDelete()
        
        // Update statistics immediately
        await this.loadStats()
        
      } catch (error) {
        console.error('Erro ao excluir curso:', error)
        this.showNotification(
          error.message || 'Erro ao excluir curso', 
          'error'
        )
      } finally {
        this.isDeletingCurso = false
      }
    },

    async loadStats() {
      try {
        const response = await apiService.getStats()
        this.stats = response.data
      } catch (error) {
        console.error('Erro ao carregar estatísticas:', error)
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
.dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.dashboard-header {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 24px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
}

.dashboard-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.dashboard-subtitle {
  color: #6b7280;
  font-size: 1.1rem;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.btn {
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
  transform: translateY(-2px);
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
}

.btn-secondary:hover:not(:disabled) {
  background: #e5e7eb;
}

.btn-danger {
  background: #ef4444;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #dc2626;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-icon.rotating {
  animation: spin 1s linear infinite;
}

.stats-section {
  margin-bottom: 24px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  font-size: 2rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
}

.stat-label {
  color: #6b7280;
  font-size: 0.875rem;
}

.filters-section {
  margin-bottom: 24px;
}

.filters-container {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  backdrop-filter: blur(10px);
}

.search-input {
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  width: 250px;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
}

.filter-buttons {
  display: flex;
  gap: 8px;
}

.filter-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 20px;
  background: #f3f4f6;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn.active,
.filter-btn:hover {
  background: #3b82f6;
  color: white;
}

.courses-section {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  min-height: 400px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
  gap: 16px;
}

.loading-spinner-large {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.empty-state,
.no-results {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
  gap: 16px;
  text-align: center;
  color: #6b7280;
}

.empty-icon,
.no-results-icon {
  font-size: 4rem;
  opacity: 0.5;
}

.courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 0;
  padding: 20px;
}

.delete-modal {
  background: white;
  border-radius: 12px;
  padding: 32px;
  max-width: 400px;
  text-align: center;
}

.delete-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.delete-warning {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 8px;
}

.delete-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
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
  .dashboard {
    padding: 12px;
  }
  
  .dashboard-header {
    padding: 20px;
  }
  
  .header-content {
    flex-direction: column;
    text-align: center;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .filters-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-input {
    width: 100%;
  }
  
  .filter-buttons {
    justify-content: center;
    flex-wrap: wrap;
  }
  
  .courses-grid {
    grid-template-columns: 1fr;
  }
}
</style>