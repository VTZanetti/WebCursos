import axios from 'axios'

// Configuração base do axios
const api = axios.create({
  // Use relative URLs to work with Vite proxy
  baseURL: '/api',  // This will be proxied to http://localhost:5000/api
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 15000,  // Increased timeout for better reliability
  withCredentials: false
})

// Enhanced interceptor for better error handling
api.interceptors.response.use(
  (response) => {
    // Log successful responses in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`✅ API Success: ${response.config.method?.toUpperCase()} ${response.config.url}`, response.data)
    }
    return response
  },
  (error) => {
    // Enhanced error logging
    const errorDetails = {
      url: error.config?.url,
      method: error.config?.method?.toUpperCase(),
      status: error.response?.status,
      message: error.response?.data?.error || error.message,
      data: error.response?.data
    }
    
    console.error('❌ API Error:', errorDetails)
    
    // Return enhanced error with user-friendly messages
    const enhancedError = new Error()
    enhancedError.originalError = error
    enhancedError.status = error.response?.status
    enhancedError.serverMessage = error.response?.data?.error
    enhancedError.userMessage = getUserFriendlyMessage(error)
    
    return Promise.reject(enhancedError)
  }
)

// Function to generate user-friendly error messages
function getUserFriendlyMessage(error) {
  const status = error.response?.status
  const serverMessage = error.response?.data?.error
  
  if (!error.response) {
    return 'Não foi possível conectar ao servidor. Verifique sua conexão com a internet e se o backend está rodando.'
  }
  
  switch (status) {
    case 400:
      return serverMessage || 'Dados inválidos enviados para o servidor.'
    case 404:
      return serverMessage || 'Recurso não encontrado.'
    case 500:
      return serverMessage || 'Erro interno do servidor. Tente novamente em alguns momentos.'
    case 503:
      return 'Servidor temporariamente indisponível. Tente novamente em alguns momentos.'
    default:
      return serverMessage || `Erro no servidor (${status}). Tente novamente.`
  }
}

// Serviços da API com tratamento robusto de erros
export const apiService = {
  // ===== CURSOS =====
  
  // Buscar todos os cursos
  async getCursos() {
    try {
      const response = await api.get('/cursos')
      return response.data
    } catch (error) {
      const message = error.userMessage || 'Erro ao carregar lista de cursos'
      throw new Error(message)
    }
  },

  // Buscar curso por ID
  async getCurso(id) {
    try {
      const response = await api.get(`/cursos/${id}`)
      return response.data
    } catch (error) {
      if (error.status === 404) {
        throw new Error('Curso não encontrado')
      }
      const message = error.userMessage || 'Erro ao carregar detalhes do curso'
      throw new Error(message)
    }
  },

  // Criar novo curso
  async createCurso(cursoData) {
    try {
      const response = await api.post('/cursos', cursoData)
      return response.data
    } catch (error) {
      if (error.status === 400) {
        const message = error.serverMessage || 'Dados do curso inválidos'
        throw new Error(message)
      }
      const message = error.userMessage || 'Erro ao criar novo curso'
      throw new Error(message)
    }
  },

  // Atualizar curso
  async updateCurso(id, cursoData) {
    try {
      const response = await api.put(`/cursos/${id}`, cursoData)
      return response.data
    } catch (error) {
      if (error.status === 404) {
        throw new Error('Curso não encontrado')
      }
      if (error.status === 400) {
        const message = error.serverMessage || 'Dados do curso inválidos'
        throw new Error(message)
      }
      const message = error.userMessage || 'Erro ao atualizar curso'
      throw new Error(message)
    }
  },

  // Deletar curso
  async deleteCurso(id) {
    try {
      const response = await api.delete(`/cursos/${id}`)
      return response.data
    } catch (error) {
      if (error.status === 404) {
        throw new Error('Curso não encontrado')
      }
      const message = error.userMessage || 'Erro ao excluir curso'
      throw new Error(message)
    }
  },

  // ===== AULAS =====

  // Marcar/desmarcar aula como concluída
  async toggleAula(cursoId, numeroAula, concluida) {
    try {
      const response = await api.post(`/cursos/${cursoId}/aula`, {
        numero_aula: numeroAula,
        concluida: concluida
      })
      return response.data
    } catch (error) {
      if (error.status === 404) {
        throw new Error('Curso não encontrado')
      }
      if (error.status === 400) {
        const message = error.serverMessage || 'Número de aula inválido'
        throw new Error(message)
      }
      const message = error.userMessage || 'Erro ao atualizar progresso da aula'
      throw new Error(message)
    }
  },

  // Marcar/desmarcar múltiplas aulas como concluídas em lote
  async batchToggleAulas(cursoId, aulas) {
    try {
      const response = await api.post(`/cursos/${cursoId}/aulas/batch`, {
        aulas: aulas
      })
      return response.data
    } catch (error) {
      if (error.status === 404) {
        throw new Error('Curso não encontrado')
      }
      if (error.status === 400) {
        const message = error.serverMessage || 'Dados das aulas inválidos'
        throw new Error(message)
      }
      const message = error.userMessage || 'Erro ao atualizar progresso das aulas'
      throw new Error(message)
    }
  },

  // ===== ESTATÍSTICAS =====

  // Buscar estatísticas gerais
  async getStats() {
    try {
      const response = await api.get('/stats')
      return response.data
    } catch (error) {
      const message = error.userMessage || 'Erro ao carregar estatísticas'
      throw new Error(message)
    }
  },

  // Verificar status da API
  async healthCheck() {
    try {
      const response = await api.get('/health')
      return response.data
    } catch (error) {
      const message = error.userMessage || 'Servidor não está respondendo'
      throw new Error(message)
    }
  }
}

export default apiService