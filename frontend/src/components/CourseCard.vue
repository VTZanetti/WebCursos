<template>
  <div class="course-card" @click="navigateToCourse(curso)">
    <div class="course-card-header">
      <h3 class="course-title">{{ curso.titulo }}</h3>
      <div class="course-actions">
        <button 
          class="btn btn-edit" 
          @click.stop="$emit('edit', curso)"
          title="Editar curso"
        >
          ✏️
        </button>
        <button 
          class="btn btn-delete" 
          @click.stop="$emit('delete', curso)"
          title="Deletar curso"
        >
          🗑️
        </button>
      </div>
    </div>

    <div class="course-meta">
      <div class="course-stats">
        <span class="stat-item">
          📚 {{ curso.total_aulas }} aulas
        </span>
        <span class="stat-item">
          ✅ {{ curso.aulas_concluidas }} concluídas
        </span>
      </div>
      
      <div class="course-link" v-if="curso.link">
        <a 
          :href="curso.link" 
          target="_blank" 
          @click.stop
          class="external-link"
          title="Abrir link do curso"
        >
          🔗 Acessar
        </a>
      </div>
    </div>

    <div class="course-progress">
      <ProgressBar 
        :percentage="curso.progresso || 0"
        :label="`Progresso`"
      />
    </div>

    <div class="course-notes" v-if="curso.anotacoes">
      <p class="notes-text">{{ truncatedNotes }}</p>
    </div>

    <div class="course-footer">
      <div class="course-dates">
        <small class="date-text">
          Criado: {{ formatDate(curso.created_at) }}
        </small>
        <small class="date-text" v-if="isUpdated">
          Atualizado: {{ formatDate(curso.updated_at) }}
        </small>
      </div>
      <div class="progress-badge" :class="getProgressBadgeClass(curso.progresso)">
        {{ getProgressStatus(curso.progresso) }}
      </div>
    </div>
  </div>
</template>

<script>
import ProgressBar from './ProgressBar.vue'
import { useRouter } from 'vue-router'

export default {
  name: 'CourseCard',
  components: {
    ProgressBar
  },
  props: {
    curso: {
      type: Object,
      required: true,
      validator: (curso) => {
        return curso && typeof curso.id !== 'undefined' && curso.titulo
      }
    }
  },
  emits: ['edit', 'delete'],
  setup() {
    const router = useRouter()
    
    const navigateToCourse = (curso) => {
      router.push(`/curso/${curso.id}`)
    }
    
    return {
      navigateToCourse
    }
  },
  computed: {
    truncatedNotes() {
      if (!this.curso.anotacoes) return ''
      const maxLength = 100
      return this.curso.anotacoes.length > maxLength 
        ? this.curso.anotacoes.substring(0, maxLength) + '...'
        : this.curso.anotacoes
    },
    isUpdated() {
      return this.curso.updated_at && this.curso.updated_at !== this.curso.created_at
    }
  },
  methods: {
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
    getProgressStatus(percentage) {
      if (percentage >= 100) return 'Concluído'
      if (percentage >= 70) return 'Quase lá'
      if (percentage >= 40) return 'Em progresso'
      if (percentage > 0) return 'Iniciado'
      return 'Não iniciado'
    },
    getProgressBadgeClass(percentage) {
      if (percentage >= 100) return 'badge-complete'
      if (percentage >= 70) return 'badge-high'
      if (percentage >= 40) return 'badge-medium'
      if (percentage > 0) return 'badge-low'
      return 'badge-none'
    }
  }
}
</script>

<style scoped>
.course-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
}

/* Dark mode styles */
.dark-mode .course-card {
  background: #1f2937;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3), 0 2px 4px rgba(0, 0, 0, 0.2);
}

.course-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  border-color: #3b82f6;
}

.dark-mode .course-card:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
  border-color: #3b82f6;
}

.course-card:active {
  transform: translateY(-2px);
}

.course-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.course-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
  line-height: 1.4;
  flex: 1;
  margin-right: 12px;
}

.dark-mode .course-title {
  color: #f9fafb;
}

.course-actions {
  display: flex;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.course-card:hover .course-actions {
  opacity: 1;
}

.btn {
  background: none;
  border: none;
  padding: 6px 8px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.btn-edit:hover {
  background: #eff6ff;
  transform: scale(1.1);
}

.dark-mode .btn-edit:hover {
  background: #374151;
}

.btn-delete:hover {
  background: #fef2f2;
  transform: scale(1.1);
}

.dark-mode .btn-delete:hover {
  background: #374151;
}

.course-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 8px;
}

.course-stats {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.stat-item {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
}

.dark-mode .stat-item {
  color: #d1d5db;
}

.external-link {
  color: #3b82f6;
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.dark-mode .external-link {
  color: #60a5fa;
}

.external-link:hover {
  background: #eff6ff;
  color: #2563eb;
}

.dark-mode .external-link:hover {
  background: #374151;
  color: #93c5fd;
}

.course-progress {
  margin-bottom: 16px;
}

.course-notes {
  margin-bottom: 16px;
}

.notes-text {
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.5;
  margin: 0;
  font-style: italic;
}

.dark-mode .notes-text {
  color: #d1d5db;
}

.course-footer {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  flex-wrap: wrap;
  gap: 8px;
}

.course-dates {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.date-text {
  font-size: 0.75rem;
  color: #9ca3af;
}

.dark-mode .date-text {
  color: #9ca3af;
}

.progress-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-none {
  background: #f3f4f6;
  color: #6b7280;
}

.dark-mode .badge-none {
  background: #374151;
  color: #d1d5db;
}

.badge-low {
  background: #fef3c7;
  color: #92400e;
}

.dark-mode .badge-low {
  background: #713f12;
  color: #fde68a;
}

.badge-medium {
  background: #dbeafe;
  color: #1e40af;
}

.dark-mode .badge-medium {
  background: #1e3a8a;
  color: #93c5fd;
}

.badge-high {
  background: #d1fae5;
  color: #065f46;
}

.dark-mode .badge-high {
  background: #064e3b;
  color: #6ee7b7;
}

.badge-complete {
  background: #dcfce7;
  color: #166534;
}

.dark-mode .badge-complete {
  background: #052e16;
  color: #34d399;
}

/* Responsividade */
@media (max-width: 640px) {
  .course-card {
    margin: 8px;
    padding: 16px;
  }
  
  .course-title {
    font-size: 1.125rem;
  }
  
  .course-meta {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .course-footer {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .course-actions {
    opacity: 1;
  }
}

/* Loading state */
.course-card.loading {
  pointer-events: none;
  opacity: 0.6;
}

.course-card.loading::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.4),
    transparent
  );
  animation: loading 1.5s infinite;
}

.dark-mode .course-card.loading::after {
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.1),
    transparent
  );
}

@keyframes loading {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}
</style>