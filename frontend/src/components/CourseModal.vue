<template>
  <div class="modal-overlay" v-if="isVisible" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2 class="modal-title">
          {{ isEditing ? 'Editar Curso' : 'Novo Curso' }}
        </h2>
        <button class="btn-close" @click="closeModal" title="Fechar">
          ✕
        </button>
      </div>

      <form @submit.prevent="handleSubmit" class="course-form">
        <div class="form-group">
          <label for="titulo" class="form-label">
            Título do Curso *
          </label>
          <input
            id="titulo"
            v-model="form.titulo"
            type="text"
            class="form-input"
            :class="{ 'input-error': errors.titulo }"
            placeholder="Ex: Curso de Vue.js Avançado"
            required
            maxlength="200"
          />
          <span v-if="errors.titulo" class="error-message">
            {{ errors.titulo }}
          </span>
        </div>

        <div class="form-group">
          <label for="total_aulas" class="form-label">
            Total de Aulas *
          </label>
          <input
            id="total_aulas"
            v-model.number="form.total_aulas"
            type="number"
            class="form-input"
            :class="{ 'input-error': errors.total_aulas }"
            placeholder="Ex: 30"
            required
            min="1"
            max="1000"
          />
          <span v-if="errors.total_aulas" class="error-message">
            {{ errors.total_aulas }}
          </span>
        </div>

        <div class="form-row">
          <div class="form-group form-group-half">
            <label for="horas" class="form-label">
              Horas
            </label>
            <input
              id="horas"
              v-model.number="form.horas"
              type="number"
              class="form-input"
              :class="{ 'input-error': errors.horas }"
              placeholder="Ex: 15"
              min="0"
              max="999"
            />
            <span v-if="errors.horas" class="error-message">
              {{ errors.horas }}
            </span>
          </div>

          <div class="form-group form-group-half">
            <label for="minutos" class="form-label">
              Minutos
            </label>
            <input
              id="minutos"
              v-model.number="form.minutos"
              type="number"
              class="form-input"
              :class="{ 'input-error': errors.minutos }"
              placeholder="Ex: 30"
              min="0"
              max="59"
            />
            <span v-if="errors.minutos" class="error-message">
              {{ errors.minutos }}
            </span>
          </div>
        </div>

        <div v-if="estimativasPorAula" class="estimativas-info">
          <div class="estimativas-item">
            <span class="estimativas-label">🕒 Duração por aula:</span>
            <span class="estimativas-value">{{ estimativasPorAula }}</span>
          </div>
        </div>

        <div class="form-group">
          <label for="link" class="form-label">
            Link do Curso
          </label>
          <input
            id="link"
            v-model="form.link"
            type="url"
            class="form-input"
            :class="{ 'input-error': errors.link }"
            placeholder="https://exemplo.com/curso"
            maxlength="500"
          />
          <span v-if="errors.link" class="error-message">
            {{ errors.link }}
          </span>
          <small class="form-hint">
            URL completa do curso (opcional)
          </small>
        </div>

        <div class="form-group">
          <label for="anotacoes" class="form-label">
            Anotações
          </label>
          <textarea
            id="anotacoes"
            v-model="form.anotacoes"
            class="form-textarea"
            :class="{ 'input-error': errors.anotacoes }"
            placeholder="Suas anotações sobre o curso..."
            rows="4"
            maxlength="1000"
          ></textarea>
          <div class="character-count">
            {{ form.anotacoes?.length || 0 }}/1000
          </div>
          <span v-if="errors.anotacoes" class="error-message">
            {{ errors.anotacoes }}
          </span>
        </div>

        <div class="form-actions">
          <button 
            type="button" 
            class="btn btn-secondary" 
            @click="closeModal"
            :disabled="isLoading"
          >
            Cancelar
          </button>
          <button 
            type="submit" 
            class="btn btn-primary"
            :disabled="isLoading || !isFormValid"
          >
            <span v-if="isLoading" class="loading-spinner"></span>
            {{ isLoading ? 'Salvando...' : (isEditing ? 'Atualizar' : 'Criar Curso') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CourseModal',
  props: {
    isVisible: {
      type: Boolean,
      default: false
    },
    curso: {
      type: Object,
      default: null
    }
  },
  emits: ['close', 'save'],
  data() {
    return {
      form: {
        titulo: '',
        total_aulas: null,
        link: '',
        anotacoes: '',
        horas: 0,
        minutos: 0
      },
      errors: {},
      isLoading: false
    }
  },
  computed: {
    isEditing() {
      return Boolean(this.curso?.id)
    },
    isFormValid() {
      return this.form.titulo.trim() && 
             this.form.total_aulas && 
             this.form.total_aulas > 0 &&
             Object.keys(this.errors).length === 0
    },
    estimativasPorAula() {
      if (!this.form.total_aulas || this.form.total_aulas <= 0) {
        return null
      }
      
      const horas = this.form.horas || 0
      const minutos = this.form.minutos || 0
      const totalMinutos = (horas * 60) + minutos
      
      if (totalMinutos <= 0) {
        return null
      }
      
      const minutosPorAula = totalMinutos / this.form.total_aulas
      const horasPorAula = Math.floor(minutosPorAula / 60)
      const minutosRestantes = Math.round(minutosPorAula % 60)
      
      if (horasPorAula > 0 && minutosRestantes > 0) {
        return `${horasPorAula}h ${minutosRestantes}min`
      } else if (horasPorAula > 0) {
        return `${horasPorAula}h`
      } else if (minutosRestantes > 0) {
        return `${minutosRestantes}min`
      } else {
        return "< 1min"
      }
    }
  },
  watch: {
    isVisible(newValue) {
      if (newValue) {
        this.resetForm()
        if (this.curso) {
          this.populateForm()
        }
        // Focus no primeiro input após o modal abrir
        this.$nextTick(() => {
          const firstInput = document.getElementById('titulo')
          if (firstInput) firstInput.focus()
        })
      }
    },
    'form.titulo'() {
      this.validateField('titulo')
    },
    'form.total_aulas'() {
      this.validateField('total_aulas')
    },
    'form.link'() {
      this.validateField('link')
    },
    'form.horas'() {
      this.validateField('horas')
    },
    'form.minutos'() {
      this.validateField('minutos')
    }
  },
  methods: {
    resetForm() {
      this.form = {
        titulo: '',
        total_aulas: null,
        link: '',
        anotacoes: '',
        horas: 0,
        minutos: 0
      }
      this.errors = {}
      this.isLoading = false
    },
    
    populateForm() {
      if (this.curso) {
        this.form = {
          titulo: this.curso.titulo || '',
          total_aulas: this.curso.total_aulas || null,
          link: this.curso.link || '',
          anotacoes: this.curso.anotacoes || '',
          horas: this.curso.horas || 0,
          minutos: this.curso.minutos || 0
        }
      }
    },
    
    validateField(fieldName) {
      // Remove error using Vue 3 reactivity
      delete this.errors[fieldName]
      
      switch (fieldName) {
        case 'titulo':
          if (!this.form.titulo.trim()) {
            this.errors[fieldName] = 'Título é obrigatório'
          } else if (this.form.titulo.length < 3) {
            this.errors[fieldName] = 'Título deve ter pelo menos 3 caracteres'
          }
          break;
          
        case 'total_aulas':
          if (!this.form.total_aulas) {
            this.errors[fieldName] = 'Total de aulas é obrigatório'
          } else if (this.form.total_aulas < 1) {
            this.errors[fieldName] = 'Deve ter pelo menos 1 aula'
          } else if (this.form.total_aulas > 1000) {
            this.errors[fieldName] = 'Máximo de 1000 aulas'
          }
          break;
          
        case 'link':
          if (this.form.link && !this.isValidUrl(this.form.link)) {
            this.errors[fieldName] = 'URL inválida'
          }
          break;
          
        case 'horas':
          if (this.form.horas !== null && this.form.horas !== '' && this.form.horas !== 0 && (this.form.horas < 0 || this.form.horas > 999)) {
            this.errors[fieldName] = 'Horas deve ser entre 0 e 999'
          }
          break;
          
        case 'minutos':
          if (this.form.minutos !== null && this.form.minutos !== '' && this.form.minutos !== 0 && (this.form.minutos < 0 || this.form.minutos >= 60)) {
            this.errors[fieldName] = 'Minutos deve ser entre 0 e 59'
          }
          break;
      }
    },
    
    validateForm() {
      this.validateField('titulo')
      this.validateField('total_aulas')
      this.validateField('link')
      this.validateField('horas')
      this.validateField('minutos')
      
      return Object.keys(this.errors).length === 0
    },
    
    isValidUrl(string) {
      try {
        new URL(string)
        return true
      } catch (_) {
        return false
      }
    },
    
    async handleSubmit() {
      if (!this.validateForm()) {
        return
      }
      
      this.isLoading = true
      
      try {
        const formData = {
          titulo: this.form.titulo.trim(),
          total_aulas: parseInt(this.form.total_aulas),
          link: this.form.link.trim(),
          anotacoes: this.form.anotacoes.trim(),
          horas: this.form.horas || 0,
          minutos: this.form.minutos || 0
        }
        
        this.$emit('save', formData)
      } catch (error) {
        console.error('Erro ao processar formulário:', error)
      } finally {
        this.isLoading = false
      }
    },
    
    closeModal() {
      if (this.isLoading) return
      this.$emit('close')
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
  animation: fadeIn 0.3s ease;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px rgba(0, 0, 0, 0.1), 0 10px 10px rgba(0, 0, 0, 0.04);
  animation: slideUp 0.3s ease;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 0;
  margin-bottom: 24px;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  padding: 4px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.btn-close:hover {
  background: #f3f4f6;
  color: #374151;
}

.course-form {
  padding: 0 24px 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-row {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.form-group-half {
  flex: 1;
  margin-bottom: 0;
}

.estimativas-info {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;
}

.dark-mode .estimativas-info {
  background: #2d3748;
  border-color: #4a5568;
}

.estimativas-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.estimativas-label {
  font-weight: 500;
  color: #4a5568;
  font-size: 0.875rem;
}

.dark-mode .estimativas-label {
  color: #a0aec0;
}

.estimativas-value {
  font-weight: 600;
  color: #2b6cb0;
  font-size: 0.875rem;
}

.dark-mode .estimativas-value {
  color: #63b3ed;
}

.form-label {
  display: block;
  font-weight: 500;
  color: #374151;
  margin-bottom: 6px;
  font-size: 0.875rem;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s ease;
  background: white;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
  font-family: inherit;
}

.input-error {
  border-color: #ef4444;
}

.input-error:focus {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.error-message {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 4px;
  display: block;
}

.form-hint {
  color: #6b7280;
  font-size: 0.875rem;
  margin-top: 4px;
  display: block;
}

.character-count {
  text-align: right;
  font-size: 0.75rem;
  color: #9ca3af;
  margin-top: 4px;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 32px;
  padding-top: 20px;
  border-top: 1px solid #e5e7eb;
}

.btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  font-size: 0.875rem;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  min-height: 44px;
}

.btn:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
}

.btn-secondary:hover:not(:disabled) {
  background: #e5e7eb;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* Dark mode support */
.dark-mode .modal-overlay {
  background: rgba(0, 0, 0, 0.7);
}

.dark-mode .modal-content {
  background: #1f2937;
  box-shadow: 0 20px 25px rgba(0, 0, 0, 0.3), 0 10px 10px rgba(0, 0, 0, 0.2);
}

.dark-mode .modal-title {
  color: #f9fafb;
}

.dark-mode .btn-close {
  color: #9ca3af;
}

.dark-mode .btn-close:hover {
  background: #374151;
  color: #e5e7eb;
}

.dark-mode .form-label {
  color: #e5e7eb;
}

.dark-mode .form-input,
.dark-mode .form-textarea {
  background: #1f2937;
  border-color: #4b5563;
  color: #f9fafb;
}

.dark-mode .form-input:focus,
.dark-mode .form-textarea:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
}

.dark-mode .input-error {
  border-color: #ef4444;
}

.dark-mode .input-error:focus {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.3);
}

.dark-mode .error-message {
  color: #f87171;
}

.dark-mode .form-hint {
  color: #9ca3af;
}

.dark-mode .character-count {
  color: #9ca3af;
}

.dark-mode .form-actions {
  border-top-color: #4b5563;
}

.dark-mode .btn-secondary {
  background: #374151;
  color: #e5e7eb;
}

.dark-mode .btn-secondary:hover:not(:disabled) {
  background: #4b5563;
}

.dark-mode .btn-primary {
  background: #3b82f6;
  color: white;
}

.dark-mode .btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.dark-mode .loading-spinner {
  border-color: transparent;
  border-top-color: currentColor;
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Responsividade */
@media (max-width: 640px) {
  .modal-content {
    width: 95%;
    margin: 20px;
  }
  
  .modal-header {
    padding: 20px 20px 0;
  }
  
  .course-form {
    padding: 0 20px 20px;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }
}
</style>