<template>
  <div v-if="visible" class="modal-overlay" @click="handleOverlayClick">
    <div class="modal-container" @click.stop>
      <!-- Modal Content -->
      <div class="modal-content">
        <!-- Alert Icon -->
        <div class="modal-icon">
          <div class="alert-icon">
            <span>⚠️</span>
          </div>
        </div>

        <!-- Title -->
        <h2 class="modal-title">
          {{ titulo }}
        </h2>

        <!-- Main Message -->
        <p class="modal-message">
          {{ mensagem }}
        </p>

        <!-- Warning Message -->
        <div v-if="avisoMensagem" class="modal-warning">
          <span class="warning-icon">⚠️</span>
          <span class="warning-text">{{ avisoMensagem }}</span>
        </div>

        <!-- Item Info -->
        <div v-if="nomeItem" class="modal-item-info">
          <strong>{{ nomeItem }}</strong>
        </div>

        <!-- Action Buttons -->
        <div class="modal-actions">
          <button 
            class="btn btn-cancel"
            @click="handleCancel"
            type="button"
          >
            {{ textoCancelar }}
          </button>
          
          <button 
            class="btn btn-confirm"
            @click="handleConfirm"
            type="button"
            :disabled="isProcessing"
          >
            <span v-if="isProcessing" class="loading-spinner"></span>
            {{ isProcessing ? 'Excluindo...' : textoConfirmar }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConfirmationModal',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    titulo: {
      type: String,
      default: 'Confirmar Ação'
    },
    mensagem: {
      type: String,
      default: 'Tem certeza que deseja continuar?'
    },
    avisoMensagem: {
      type: String,
      default: ''
    },
    nomeItem: {
      type: String,
      default: ''
    },
    textoConfirmar: {
      type: String,
      default: 'Confirmar'
    },
    textoCancelar: {
      type: String,
      default: 'Cancelar'
    },
    isProcessing: {
      type: Boolean,
      default: false
    },
    allowOverlayClose: {
      type: Boolean,
      default: true
    }
  },
  emits: ['confirm', 'cancel'],
  methods: {
    handleConfirm() {
      if (!this.isProcessing) {
        this.$emit('confirm')
      }
    },
    
    handleCancel() {
      if (!this.isProcessing) {
        this.$emit('cancel')
      }
    },
    
    handleOverlayClick() {
      if (this.allowOverlayClose && !this.isProcessing) {
        this.handleCancel()
      }
    },
    
    handleEscapeKey(event) {
      if (event.key === 'Escape' && this.visible && !this.isProcessing) {
        this.handleCancel()
      }
    }
  },
  mounted() {
    document.addEventListener('keydown', this.handleEscapeKey)
  },
  
  beforeUnmount() {
    document.removeEventListener('keydown', this.handleEscapeKey)
  },
  
  watch: {
    visible(newVal) {
      if (newVal) {
        document.body.style.overflow = 'hidden'
      } else {
        document.body.style.overflow = ''
      }
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.modal-container {
  width: 90%;
  max-width: 480px;
  max-height: 90vh;
  overflow-y: auto;
  animation: slideUp 0.3s ease;
}

.modal-content {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  text-align: center;
  position: relative;
}

.modal-icon {
  margin-bottom: 20px;
}

.alert-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto;
  background: linear-gradient(135deg, #fee2e2, #fecaca);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  border: 3px solid #f87171;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 16px 0;
  line-height: 1.3;
}

.modal-message {
  font-size: 1rem;
  color: #6b7280;
  margin: 0 0 16px 0;
  line-height: 1.5;
}

.modal-warning {
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  padding: 12px 16px;
  margin: 16px 0;
  display: flex;
  align-items: center;
  gap: 8px;
  text-align: left;
}

.warning-icon {
  font-size: 16px;
  flex-shrink: 0;
}

.warning-text {
  font-size: 0.875rem;
  color: #dc2626;
  font-weight: 500;
}

.modal-item-info {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 12px 16px;
  margin: 16px 0;
  font-size: 0.875rem;
  color: #374151;
}

.modal-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
  justify-content: center;
}

.btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  min-width: 100px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-cancel {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.btn-cancel:hover:not(:disabled) {
  background: #e5e7eb;
  border-color: #9ca3af;
  transform: translateY(-1px);
}

.btn-confirm {
  background: #dc2626;
  color: white;
  border: 1px solid #dc2626;
}

.btn-confirm:hover:not(:disabled) {
  background: #b91c1c;
  border-color: #b91c1c;
  transform: translateY(-1px);
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none !important;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes spin {
  0% { 
    transform: rotate(0deg); 
  }
  100% { 
    transform: rotate(360deg); 
  }
}

/* Responsive Design */
@media (max-width: 640px) {
  .modal-container {
    width: 95%;
    margin: 20px 0;
  }
  
  .modal-content {
    padding: 24px;
  }
  
  .modal-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    padding: 14px 24px;
  }
  
  .alert-icon {
    width: 56px;
    height: 56px;
    font-size: 28px;
  }
  
  .modal-title {
    font-size: 1.25rem;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .modal-content {
    background: #1f2937;
    color: #f9fafb;
  }
  
  .modal-title {
    color: #f9fafb;
  }
  
  .modal-message {
    color: #d1d5db;
  }
  
  .modal-item-info {
    background: #374151;
    border-color: #4b5563;
    color: #e5e7eb;
  }
  
  .btn-cancel {
    background: #374151;
    color: #e5e7eb;
    border-color: #4b5563;
  }
  
  .btn-cancel:hover:not(:disabled) {
    background: #4b5563;
    border-color: #6b7280;
  }
}

/* Explicit dark mode classes */
.dark-mode .modal-overlay {
  background: rgba(0, 0, 0, 0.7);
}

.dark-mode .modal-content {
  background: #1f2937;
  color: #f9fafb;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.dark-mode .modal-title {
  color: #f9fafb;
}

.dark-mode .modal-message {
  color: #d1d5db;
}

.dark-mode .modal-warning {
  background: #374151;
  border-color: #4b5563;
}

.dark-mode .warning-text {
  color: #f87171;
}

.dark-mode .modal-item-info {
  background: #374151;
  border-color: #4b5563;
  color: #e5e7eb;
}

.dark-mode .btn-cancel {
  background: #374151;
  color: #e5e7eb;
  border-color: #4b5563;
}

.dark-mode .btn-cancel:hover:not(:disabled) {
  background: #4b5563;
  border-color: #6b7280;
}

.dark-mode .btn-confirm {
  background: #b91c1c;
  border-color: #b91c1c;
}

.dark-mode .btn-confirm:hover:not(:disabled) {
  background: #991b1b;
  border-color: #991b1b;
}

.dark-mode .loading-spinner {
  border-color: rgba(255, 255, 255, 0.3);
  border-top-color: white;
}

.dark-mode .alert-icon {
  background: linear-gradient(135deg, #374151, #4b5563);
  border-color: #f87171;
}
</style>