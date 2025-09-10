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
        
        // Fix: The API returns data in a nested structure
        this.cursos = cursosResponse.data?.cursos || []
        this.stats = statsResponse.data || null
        
        console.log('Cursos carregados:', this.cursos.length, 'cursos')
        
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
          console.log('Atualizando curso com dados:', cursoData)
          const response = await apiService.updateCurso(this.selectedCurso.id, cursoData)
          console.log('Resposta da atualização:', response)
          
          // Atualizar na lista local
          const index = this.cursos.findIndex(c => c.id === this.selectedCurso.id)
          if (index !== -1) {
            this.cursos.splice(index, 1, response.data)
          }
          
          this.showNotification('Curso atualizado com sucesso!', 'success')
        } else {
          // Criar novo curso
          console.log('🆕 Criando curso com dados:', cursoData)
          const response = await apiService.createCurso(cursoData)
          console.log('🆕 Resposta da criação:', response)
          
          // Verificar a estrutura da resposta
          if (response && response.data) {
            // Adicionar na lista local - fix: access the correct data structure
            const novoCurso = response.data
            this.cursos.unshift(novoCurso)
            this.showNotification('Curso criado com sucesso!', 'success')
          } else if (response) {
            // Se a resposta for diretamente o curso (sem envolvimento em data)
            const novoCurso = response
            this.cursos.unshift(novoCurso)
            this.showNotification('Curso criado com sucesso!', 'success')
          } else {
            console.error('❌ Resposta inesperada da API:', response)
            this.showNotification('Erro inesperado: resposta vazia da API', 'error')
          }
        }
        
        this.closeModal()
        
        // Update statistics immediately
        await this.loadStats()
        
      } catch (error) {
        console.error('❌ Erro detalhado ao salvar curso:', {
          error,
          message: error.message,
          stack: error.stack,
          isEditing: this.selectedCurso?.id ? 'sim' : 'não',
          cursoData
        })
        
        let errorMessage = 'Erro ao salvar curso'
        if (error.message) {
          errorMessage = error.message
        }
        
        this.showNotification(errorMessage, 'error')
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
        this.stats = response.data || null
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

/* Dark mode styles */
.dark-mode .dashboard {
  background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
}

.dashboard-header {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 24px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.dark-mode .dashboard-header {
  background: rgba(31, 41, 55, 0.95);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 24px;
}

.header-info h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 8px 0;
  line-height: 1.2;
}

.dark-mode .header-info h1 {
  color: #f9fafb;
}

.header-info p {
  color: #6b7280;
  font-size: 1.125rem;
  margin: 0;
}

.dark-mode .header-info p {
  color: #d1d5db;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.stats-section {
  margin-bottom: 24px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 24px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.dark-mode .stat-card {
  background: rgba(31, 41, 55, 0.95);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-icon {
  font-size: 2rem;
  margin-bottom: 16px;
}

.stat-info {
  text-align: center;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 8px;
}

.dark-mode .stat-value {
  color: #f9fafb;
}

.stat-label {
  color: #6b7280;
  font-weight: 500;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.dark-mode .stat-label {
  color: #d1d5db;
}

.filters-section {
  margin-bottom: 24px;
}

.filters-container {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 24px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.dark-mode .filters-container {
  background: rgba(31, 41, 55, 0.95);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.search-box {
  margin-bottom: 16px;
}

.search-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s ease;
  background: white;
  color: #1f2937;
}

.dark-mode .search-input {
  border-color: #4b5563;
  background: #1f2937;
  color: #f9fafb;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.dark-mode .search-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
}

.filter-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.filter-btn {
  padding: 8px 16px;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 20px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #6b7280;
}

.dark-mode .filter-btn {
  border-color: #4b5563;
  background: #1f2937;
  color: #d1d5db;
}

.filter-btn:hover:not(.active) {
  background: #f9fafb;
  border-color: #9ca3af;
}

.dark-mode .filter-btn:hover:not(.active) {
  background: #374151;
  border-color: #6b7280;
}

.filter-btn.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
}

.courses-section {
  margin-bottom: 24px;
}

.loading-container,
.empty-state,
.no-results {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
  text-align: center;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 32px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.dark-mode .loading-container,
.dark-mode .empty-state,
.dark-mode .no-results {
  background: rgba(31, 41, 55, 0.95);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.loading-spinner-large {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 24px;
}

.dark-mode .loading-spinner-large {
  border-color: #4b5563;
  border-top-color: #3b82f6;
}

.empty-icon,
.no-results-icon {
  font-size: 4rem;
  margin-bottom: 24px;
}

.courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
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
  
  .dashboard-header,
  .filters-container {
    padding: 20px;
  }
  
  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .header-info h1 {
    font-size: 2rem;
  }
  
  .courses-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .header-actions {
    width: 100%;
    justify-content: center;
  }
}
</style>
