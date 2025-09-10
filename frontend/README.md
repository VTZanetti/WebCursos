# WebCurso Frontend

Interface moderna e responsiva construída com Vue.js 3 + Vite para o sistema de gerenciamento de cursos.

## 🚀 Tecnologias

- **Vue.js 3** - Framework JavaScript reativo
- **Vite** - Ferramenta de build ultrarrápida
- **Vue Router** - Roteamento SPA
- **Axios** - Cliente HTTP
- **CSS3** - Estilização moderna com gradientes e animações

## 📁 Estrutura do Projeto

```
frontend/
├── src/
│   ├── components/           # Componentes reutilizáveis
│   │   ├── CourseCard.vue   # Card de curso
│   │   ├── ProgressBar.vue  # Barra de progresso
│   │   └── CourseModal.vue  # Modal de criação/edição
│   ├── views/               # Views/Páginas
│   │   ├── DashboardView.vue    # Dashboard principal
│   │   └── CourseDetailView.vue # Detalhes do curso
│   ├── services/            # Serviços
│   │   └── api.js          # Cliente da API
│   ├── router/             # Configuração de rotas
│   │   └── index.js
│   ├── App.vue            # Componente raiz
│   └── main.js           # Ponto de entrada
├── package.json          # Dependências e scripts
├── vite.config.js       # Configuração do Vite
└── index.html          # Template HTML
```

## ⚙️ Configuração

### Pré-requisitos
- Node.js 16+ 
- npm ou yarn
- Backend rodando em `http://localhost:5000`

### Instalação

```bash
# 1. Entre no diretório frontend
cd frontend

# 2. Instale as dependências
npm install

# 3. Inicie o servidor de desenvolvimento
npm run dev
```

### Scripts Disponíveis

```bash
# Desenvolvimento
npm run dev          # Servidor de desenvolvimento (http://localhost:3000)

# Build para produção
npm run build        # Gera build otimizado na pasta dist/

# Preview da build
npm run preview      # Visualiza a build de produção
```

### Script Automatizado (Windows)
```bash
# Execute no diretório frontend
start_dev.bat
```

## 🎨 Componentes

### CourseCard.vue
Card responsivo que exibe:
- Título e metadados do curso
- Barra de progresso visual
- Ações de editar/deletar
- Link externo (opcional)
- Anotações truncadas

### ProgressBar.vue
Componente de progresso com:
- Animações suaves
- Cores dinâmicas baseadas na porcentagem
- Efeito de brilho
- Suporte a dark mode

### CourseModal.vue
Modal completo para CRUD de cursos:
- Validação em tempo real
- Estados de loading
- Formulário responsivo
- Contador de caracteres

## 📱 Views

### DashboardView.vue
Dashboard principal com:
- Estatísticas em tempo real
- Grid responsivo de cursos
- Sistema de filtros e busca
- Estados de loading e erro
- Integração completa com API

### CourseDetailView.vue
Página de detalhes com:
- Controle individual de aulas
- Editor de anotações inline
- Barra de progresso detalhada
- Ações em lote (marcar todas)
- Navegação breadcrumb

## 🔌 API Integration

### Serviço API (api.js)
Cliente HTTP centralizado com:
- Interceptors para tratamento de erros
- Timeout configurado
- Base URL automática
- Métodos para todos os endpoints

### Endpoints Consumidos
- `GET /api/cursos` - Lista cursos
- `POST /api/cursos` - Cria curso
- `GET /api/cursos/:id` - Detalhes do curso
- `PUT /api/cursos/:id` - Atualiza curso
- `DELETE /api/cursos/:id` - Remove curso
- `POST /api/cursos/:id/aula` - Controla aulas
- `GET /api/stats` - Estatísticas
- `GET /api/health` - Status da API

## 🎯 Funcionalidades

### Dashboard
- ✅ Listagem de cursos com paginação visual
- ✅ Estatísticas em tempo real
- ✅ Filtros por status (não iniciado, em progresso, concluído)
- ✅ Busca por título e anotações
- ✅ Modal de criação/edição
- ✅ Confirmação de exclusão
- ✅ Notificações de sucesso/erro

### Detalhes do Curso
- ✅ Grid interativo de aulas
- ✅ Checkbox de progresso individual
- ✅ Editor de anotações inline
- ✅ Ações em lote
- ✅ Estados de loading
- ✅ Validação de dados

### UX/UI
- ✅ Design responsivo (mobile-first)
- ✅ Animações suaves
- ✅ Estados de loading
- ✅ Feedback visual
- ✅ Temas dark/light
- ✅ Acessibilidade (WCAG)

## 🌐 Configuração de Proxy

O Vite está configurado para fazer proxy das requisições da API:

```javascript
// vite.config.js
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      changeOrigin: true,
      secure: false,
    }
  }
}
```

## 📱 Responsividade

### Breakpoints
- **Mobile**: < 640px
- **Tablet**: 640px - 768px  
- **Desktop**: > 768px

### Adaptações Mobile
- Grid de cursos em coluna única
- Modal fullscreen
- Navegação simplificada
- Botões maiores para touch
- Tipografia otimizada

## 🚀 Performance

### Otimizações Implementadas
- **Code Splitting** - Componentes lazy-loaded
- **Tree Shaking** - Remoção de código não utilizado
- **Asset Optimization** - Compressão de imagens e CSS
- **Gzip Compression** - Redução do tamanho dos arquivos
- **Cache Strategy** - Headers de cache otimizados

### Métricas Esperadas
- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3s
- **Bundle Size**: < 100KB gzipped

## 🔧 Customização

### Tema e Cores
Edite as variáveis CSS em `App.vue`:

```css
:root {
  --primary-color: #3b82f6;
  --success-color: #10b981;
  --error-color: #ef4444;
  /* ... outras variáveis */
}
```

### API Base URL
Modifique em `services/api.js`:

```javascript
const api = axios.create({
  baseURL: 'http://localhost:5000/api', // Altere aqui
  // ...
})
```

## 🧪 Desenvolvimento

### Hot Reload
O Vite oferece hot reload ultrarrápido durante o desenvolvimento.

### DevTools
Instale a extensão Vue DevTools para debugging:
- Chrome: Vue.js devtools
- Firefox: Vue.js devtools

### Debugging
```javascript
// Habilitar logs da API
localStorage.setItem('debug', 'api:*')

// Desabilitar
localStorage.removeItem('debug')
```

## 📦 Build para Produção

```bash
# Gerar build otimizado
npm run build

# Arquivos serão gerados em dist/
# Faça deploy da pasta dist/ para seu servidor web
```

### Configuração do Servidor Web
Para SPAs Vue.js, configure o servidor para redirecionar todas as rotas para `index.html`.

#### Nginx
```nginx
location / {
  try_files $uri $uri/ /index.html;
}
```

#### Apache
```apache
RewriteEngine On
RewriteRule ^index\.html$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.html [L]
```

## 🐛 Troubleshooting

### API não conecta
1. Verifique se o backend está rodando
2. Confirme a URL da API
3. Verifique CORS no backend

### Erros de build
1. Limpe node_modules: `rm -rf node_modules && npm install`
2. Limpe cache: `npm run dev -- --force`

### Performance lenta
1. Verifique Network tab no DevTools
2. Analise bundle size: `npm run build -- --analyze`

---

**🎓 Interface moderna para o sistema WebCurso - Construído com Vue.js 3 e muito ❤️**