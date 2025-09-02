<template>
  <div id="app">
    <!-- Navigation Bar -->
    <nav class="navbar" v-if="!isLoading">
      <div class="navbar-content">
        <router-link to="/" class="navbar-brand">
          <span class="brand-icon">🎓</span>
          <span class="brand-text">WebCurso</span>
        </router-link>
        
        <div class="navbar-nav">
          <router-link 
            to="/" 
            class="nav-link"
            :class="{ 'active': $route.name === 'dashboard' }"
          >
            📊 Dashboard
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content">
      <!-- Loading Screen -->
      <div v-if="isLoading" class="app-loading">
        <div class="loading-animation">
          <div class="loading-spinner-large"></div>
          <h2>Carregando WebCurso...</h2>
          <p>Verificando conexão com a API...</p>
        </div>
      </div>

      <!-- Error Screen -->
      <div v-else-if="appError" class="app-error">
        <div class="error-content">
          <div class="error-icon">⚠️</div>
          <h2>Erro de Conexão</h2>
          <p>{{ appError }}</p>
          <div class="error-details">
            <p>Verifique se o backend está rodando em:</p>
            <code>http://localhost:5000</code>
          </div>
          <button class="btn btn-primary" @click="checkApiConnection">
            🔄 Tentar Novamente
          </button>
        </div>
      </div>

      <!-- App Content -->
      <div v-else class="app-wrapper">
        <router-view />
      </div>
    </main>

    <!-- Global Notifications -->
    <div v-if="globalNotification" class="global-notification" :class="globalNotification.type">
      {{ globalNotification.message }}
    </div>

    <!-- Footer -->
    <footer class="app-footer" v-if="!isLoading && !appError">
      <div class="footer-content">
        <p>&copy; 2025 WebCurso - Sistema de Gerenciamento de Cursos</p>
        <div class="footer-links">
          <span class="footer-status" :class="{ 'online': isApiOnline, 'offline': !isApiOnline }">
            {{ isApiOnline ? '🟢 API Online' : '🔴 API Offline' }}
          </span>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import apiService from './services/api.js'

export default {
  name: 'App',
  data() {
    return {
      isLoading: true,
      appError: null,
      isApiOnline: false,
      globalNotification: null,
      healthCheckInterval: null
    }
  },
  async mounted() {
    await this.initializeApp()
    this.startHealthCheck()
  },
  beforeUnmount() {
    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval)
    }
  },
  methods: {
    async initializeApp() {
      try {
        this.isLoading = true
        this.appError = null
        
        // Verificar conexão com a API
        await this.checkApiConnection()
        
        // Pequeno delay para melhor UX
        await new Promise(resolve => setTimeout(resolve, 1000))
        
      } catch (error) {
        console.error('Erro ao inicializar aplicação:', error)
        this.appError = 'Não foi possível conectar com a API do backend'
      } finally {
        this.isLoading = false
      }
    },

    async checkApiConnection() {
      try {
        await apiService.healthCheck()
        this.isApiOnline = true
        this.appError = null
        
        if (!this.isLoading) {
          this.showGlobalNotification('Conexão com API restabelecida', 'success')
        }
      } catch (error) {
        this.isApiOnline = false
        
        if (this.isLoading) {
          throw error
        } else {
          this.showGlobalNotification('Conexão com API perdida', 'error')
        }
      }
    },

    startHealthCheck() {
      // Verificar status da API a cada 30 segundos
      this.healthCheckInterval = setInterval(async () => {
        await this.checkApiConnection()
      }, 30000)
    },

    showGlobalNotification(message, type = 'info') {
      this.globalNotification = { message, type }
      
      setTimeout(() => {
        this.globalNotification = null
      }, 4000)
    }
  }
}
</script>

<style>
/* Reset e Variáveis CSS */
:root {
  --primary-color: #3b82f6;
  --primary-hover: #2563eb;
  --success-color: #10b981;
  --error-color: #ef4444;
  --warning-color: #f59e0b;
  --info-color: #3b82f6;
  
  --text-primary: #1f2937;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;
  
  --bg-primary: #ffffff;
  --bg-secondary: #f9fafb;
  --bg-muted: #f3f4f6;
  
  --border-color: #e5e7eb;
  --shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
  
  --border-radius: 8px;
  --border-radius-lg: 12px;
  
  --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-family);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Navigation */
.navbar {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: var(--shadow);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  font-weight: 700;
  font-size: 1.25rem;
  color: var(--primary-color);
  transition: all 0.2s ease;
}

.navbar-brand:hover {
  transform: translateY(-1px);
}

.brand-icon {
  font-size: 1.5rem;
}

.navbar-nav {
  display: flex;
  gap: 8px;
}

.nav-link {
  color: var(--text-secondary);
  text-decoration: none;
  padding: 8px 16px;
  border-radius: var(--border-radius);
  font-weight: 500;
  transition: all 0.2s ease;
}

.nav-link:hover,
.nav-link.active {
  color: var(--primary-color);
  background: rgba(59, 130, 246, 0.1);
}

/* Main Content */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.app-wrapper {
  flex: 1;
}

/* Loading Screen */
.app-loading {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 40px 20px;
}

.loading-animation {
  text-align: center;
  color: white;
}

.loading-spinner-large {
  width: 64px;
  height: 64px;
  border: 6px solid rgba(255, 255, 255, 0.3);
  border-top: 6px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 24px;
}

.loading-animation h2 {
  font-size: 1.5rem;
  margin-bottom: 8px;
  font-weight: 600;
}

.loading-animation p {
  opacity: 0.8;
  font-size: 1rem;
}

/* Error Screen */
.app-error {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 40px 20px;
}

.error-content {
  background: rgba(255, 255, 255, 0.95);
  border-radius: var(--border-radius-lg);
  padding: 48px;
  text-align: center;
  max-width: 500px;
  backdrop-filter: blur(10px);
  box-shadow: var(--shadow-lg);
}

.error-icon {
  font-size: 4rem;
  margin-bottom: 24px;
}

.error-content h2 {
  color: var(--error-color);
  font-size: 1.5rem;
  margin-bottom: 16px;
}

.error-content p {
  color: var(--text-secondary);
  margin-bottom: 16px;
  line-height: 1.5;
}

.error-details {
  background: var(--bg-muted);
  border-radius: var(--border-radius);
  padding: 16px;
  margin: 20px 0;
  text-align: left;
}

.error-details code {
  background: rgba(59, 130, 246, 0.1);
  color: var(--primary-color);
  padding: 4px 8px;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.875rem;
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border: none;
  border-radius: var(--border-radius);
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
  line-height: 1;
}

.btn-primary {
  background: var(--primary-color);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: var(--primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow);
}

.btn-secondary {
  background: var(--bg-muted);
  color: var(--text-primary);
}

.btn-secondary:hover:not(:disabled) {
  background: #e5e7eb;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

/* Global Notifications */
.global-notification {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 16px 24px;
  border-radius: var(--border-radius);
  color: white;
  font-weight: 500;
  z-index: 1000;
  min-width: 300px;
  box-shadow: var(--shadow-lg);
  animation: slideInRight 0.3s ease;
}

.global-notification.success {
  background: var(--success-color);
}

.global-notification.error {
  background: var(--error-color);
}

.global-notification.warning {
  background: var(--warning-color);
}

.global-notification.info {
  background: var(--info-color);
}

/* Footer */
.app-footer {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-top: 1px solid var(--border-color);
  padding: 20px 0;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.footer-links {
  display: flex;
  gap: 16px;
  align-items: center;
}

.footer-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
}

.footer-status.online {
  background: rgba(16, 185, 129, 0.1);
  color: var(--success-color);
}

.footer-status.offline {
  background: rgba(239, 68, 68, 0.1);
  color: var(--error-color);
}

/* Animations */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Scrollbar Styling */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: var(--bg-muted);
}

::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #d1d5db;
}

/* Responsividade */
@media (max-width: 768px) {
  .navbar-content {
    padding: 0 16px;
  }
  
  .navbar-brand {
    font-size: 1.125rem;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 12px;
    text-align: center;
    padding: 0 16px;
  }
  
  .global-notification {
    right: 16px;
    left: 16px;
    min-width: auto;
  }
  
  .error-content {
    padding: 32px 24px;
    margin: 0 16px;
  }
  
  .app-loading,
  .app-error {
    padding: 20px 16px;
  }
}

/* Focus Styles */
button:focus,
input:focus,
textarea:focus,
select:focus,
a:focus {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}

/* Print Styles */
@media print {
  .navbar,
  .app-footer,
  .global-notification {
    display: none;
  }
  
  body {
    background: white;
  }
  
  .main-content {
    background: white;
  }
}
</style>