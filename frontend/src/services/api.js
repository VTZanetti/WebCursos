import axios from 'axios'

// Configuração base do axios
const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 10000
})

// Interceptor para tratar respostas
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// Serviços da API
export const apiService = {
  // ===== CURSOS =====
  
  // Buscar todos os cursos
  async getCursos() {
    try {
      const response = await api.get('/cursos')
      return response.data
    } catch (error) {
      throw new Error(`Erro ao buscar cursos: ${error.message}`)
    }
  },

  // Buscar curso por ID
  async getCurso(id) {
    try {
      const response = await api.get(`/cursos/${id}`)
      return response.data
    } catch (error) {
      if (error.response?.status === 404) {
        throw new Error('Curso não encontrado')
      }
      throw new Error(`Erro ao buscar curso: ${error.message}`)
    }
  },

  // Criar novo curso
  async createCurso(cursoData) {
    try {
      const response = await api.post('/cursos', cursoData)
      return response.data
    } catch (error) {
      if (error.response?.status === 400) {
        throw new Error('Dados do curso inválidos')
      }
      throw new Error(`Erro ao criar curso: ${error.message}`)
    }
  },

  // Atualizar curso
  async updateCurso(id, cursoData) {
    try {
      const response = await api.put(`/cursos/${id}`, cursoData)
      return response.data
    } catch (error) {
      if (error.response?.status === 404) {
        throw new Error('Curso não encontrado')
      }
      if (error.response?.status === 400) {
        throw new Error('Dados do curso inválidos')
      }
      throw new Error(`Erro ao atualizar curso: ${error.message}`)
    }
  },

  // Deletar curso
  async deleteCurso(id) {
    try {
      const response = await api.delete(`/cursos/${id}`)
      return response.data
    } catch (error) {
      if (error.response?.status === 404) {
        throw new Error('Curso não encontrado')
      }
      throw new Error(`Erro ao deletar curso: ${error.message}`)
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
      if (error.response?.status === 404) {
        throw new Error('Curso não encontrado')
      }
      if (error.response?.status === 400) {
        throw new Error('Número de aula inválido')
      }
      throw new Error(`Erro ao atualizar aula: ${error.message}`)
    }
  },

  // ===== ESTATÍSTICAS =====

  // Buscar estatísticas gerais
  async getStats() {
    try {
      const response = await api.get('/stats')
      return response.data
    } catch (error) {
      throw new Error(`Erro ao buscar estatísticas: ${error.message}`)
    }
  },

  // Verificar status da API
  async healthCheck() {
    try {
      const response = await api.get('/health')
      return response.data
    } catch (error) {
      throw new Error(`API não está respondendo: ${error.message}`)
    }
  }
}

export default apiService