# 🎓 WebCurso - Sistema de Gerenciamento de Cursos

## 📋 Visão Geral do Projeto

O **WebCurso** é uma aplicação web moderna para gerenciamento de cursos online, desenvolvida com arquitetura de separação entre backend e frontend:

### Arquitetura da Aplicação

```
┌─────────────────────┐    HTTP/JSON    ┌─────────────────────┐
│                     │   Requests      │                     │
│   Frontend Vue.js   │◄───────────────►│   Backend Flask     │
│                     │                 │                     │
│  • Interface SPA    │                 │  • API RESTful      │
│  • Vue Router       │                 │  • 8 Endpoints      │
│  • Axios HTTP       │                 │  • Validação        │
│  • Componentes      │                 │  • CORS             │
│                     │                 │                     │
└─────────────────────┘                 └─────────────────────┘
                                                    │
                                                    │ SQLite
                                                    ▼
                                        ┌─────────────────────┐
                                        │                     │
                                        │  Banco de Dados     │
                                        │                     │
                                        │  • Cursos           │
                                        │  • Aulas Concluídas │
                                        │  • Progresso        │
                                        │                     │
                                        └─────────────────────┘
```

**Componentes Principais:**
- **Backend**: API RESTful desenvolvida em Flask (Python)
- **Frontend**: SPA (Single Page Application) desenvolvida em Vue.js 3
- **Banco de Dados**: SQLite para persistência de dados (configuração permanente)
- **Comunicação**: HTTP/JSON entre frontend e backend via CORS

---

## 💻 Pré-requisitos de Software

Antes de iniciar, certifique-se de que os seguintes softwares estão instalados em seu sistema:

### Obrigatórios:

#### 1. Python 3.8+ e Pip
- **Download**: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- **Versão mínima**: Python 3.8 ou superior
- **Verificação**:
  ```bash
  python --version
  pip --version
  ```

#### 2. Node.js 16+ e NPM
- **Download**: [https://nodejs.org/](https://nodejs.org/) (versão LTS recomendada)
- **Versão mínima**: Node.js 16.0 ou superior
- **Verificação**:
  ```bash
  node --version
  npm --version
  ```

### Opcionais (mas recomendados):

#### 3. Git (para versionamento)
- **Download**: [https://git-scm.com/downloads](https://git-scm.com/downloads)

#### 4. Visual Studio Code (editor recomendado)
- **Download**: [https://code.visualstudio.com/](https://code.visualstudio.com/)
- **Extensões úteis**: Python, Vetur (Vue), GitLens

---

## 🔧 Configuração do Backend

### Passo 1: Navegação para o Diretório Backend

```bash
# Navegue até o diretório raiz do projeto
cd c:\Dev\WebCurso

# Entre no diretório backend
cd backend
```

### Passo 2: Criação e Ativação do Ambiente Virtual Python

**Windows (PowerShell/CMD):**
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate

# Confirmar ativação (deve aparecer (venv) no prompt)
```

**Linux/macOS:**
```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Confirmar ativação (deve aparecer (venv) no prompt)
```

### Passo 3: Instalação das Dependências

```bash
# Instalar dependências do requirements.txt
pip install -r requirements.txt

# Verificar instalação (opcional)
pip list
```

**Dependências que serão instaladas:**
- Flask==2.3.3
- Flask-CORS==4.0.0
- SQLAlchemy==2.0.21

### Passo 4: Inicialização do Banco de Dados

O WebCurso agora usa SQLite permanentemente, sem necessidade de configuração adicional:

```bash
# Executar script de inicialização (primeira vez apenas)
python init_db.py
```

**Saída esperada:**
```
Banco de dados inicializado em: C:\Dev\WebCurso\backend\instance\database.sqlite
Tabelas criadas:
- cursos (id, titulo, link, total_aulas, anotacoes, created_at, updated_at)
- aulas_concluidas (id, curso_id, numero_aula, created_at)

Inserindo dados de exemplo...
Dados de exemplo inseridos!
```

### Passo 5: Iniciar o Servidor da API Flask

```bash
# Iniciar servidor Flask (SQLite é usado automaticamente)
python app.py
```

**Saída esperada:**
```
🚀 Iniciando API do WebCurso...
📊 Endpoints disponíveis:
   GET    /api/cursos          - Listar cursos
   POST   /api/cursos          - Criar curso
   GET    /api/cursos/<id>     - Detalhes do curso
   PUT    /api/cursos/<id>     - Atualizar curso
   DELETE /api/cursos/<id>     - Deletar curso
   POST   /api/cursos/<id>/aula - Controlar aulas concluídas
   GET    /api/health          - Status da API
   GET    /api/stats           - Estatísticas gerais

🌐 CORS habilitado para:
   - http://localhost:3000
   - http://localhost:8080
   - http://127.0.0.1:3000
   - http://127.0.0.1:8080

 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://[your-ip]:5000
```

**✅ Backend configurado com sucesso! A API estará disponível em `http://127.0.0.1:5000`**

---

## 🎨 Configuração do Frontend

### Passo 1: Navegação para o Diretório Frontend

```bash
# Em um NOVO terminal (mantenha o backend rodando)
cd c:\Dev\WebCurso

# Entre no diretório frontend
cd frontend
```

### Passo 2: Instalação das Dependências do Node.js

```bash
# Instalar dependências do package.json
npm install
```

**Dependências que serão instaladas:**
- vue@^3.4.0
- vue-router@^4.2.5
- axios@^1.6.0
- @vitejs/plugin-vue@^4.5.0
- vite@^5.0.0

**Saída esperada:**
```
added [número] packages, and audited [número] packages in [tempo]s

[número] packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
```

### Passo 3: Iniciar o Servidor de Desenvolvimento Vite

```bash
# Iniciar servidor de desenvolvimento
npm run dev
```

**Saída esperada:**
```
  VITE v5.0.0  ready in [tempo] ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**✅ Frontend configurado com sucesso! A aplicação estará disponível em `http://localhost:3000`**

---

## 🚀 Executando a Aplicação

### Configuração de Terminais

Para executar a aplicação completa, você precisará de **2 terminais simultâneos**:

#### Terminal 1 - Backend (API Flask)
```bash
cd c:\Dev\WebCurso\backend
venv\Scripts\activate  # Windows
# ou source venv/bin/activate  # Linux/macOS
python app.py
```

#### Terminal 2 - Frontend (Vue.js)
```bash
cd c:\Dev\WebCurso\frontend
npm run dev
```

### URLs de Acesso

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **API Backend** | `http://127.0.0.1:5000` | Endpoints da API RESTful |
| **Frontend** | `http://localhost:3000` | Interface web da aplicação |
| **Health Check** | `http://127.0.0.1:5000/api/health` | Status da API |
| **Documentação API** | `http://127.0.0.1:5000/api/cursos` | Lista de cursos (JSON) |

### Acessando e Usando a Aplicação

#### 1. Acesso Inicial
1. **Abra o navegador** e acesse: `http://localhost:3000`
2. **Aguarde o carregamento** da interface (alguns segundos na primeira vez)
3. **Verifique a conexão** - deve aparecer "🟢 API Online" no rodapé

#### 2. Navegação Principal

**Dashboard (Página Inicial):**
- **URL**: `http://localhost:3000/`
- **Funcionalidades**:
  - Visualizar estatísticas gerais
  - Ver lista de cursos existentes
  - Criar novos cursos (botão "➕ Novo Curso")
  - Filtrar cursos por status
  - Buscar cursos por título

**Detalhes do Curso:**
- **URL**: `http://localhost:3000/curso/{id}`
- **Acesso**: Clique em qualquer card de curso no dashboard
- **Funcionalidades**:
  - Visualizar informações detalhadas
  - Controlar aulas concluídas (checkboxes)
  - Editar anotações do curso
  - Ver progresso visual atualizado

#### 3. Fluxo de Uso Recomendado

1. **Explorar dados exemplo**:
   - Acesse o dashboard
   - Observe os cursos pré-carregados
   - Clique em um curso para ver detalhes

2. **Criar novo curso**:
   - Clique em "➕ Novo Curso"
   - Preencha: título, total de aulas, link (opcional), anotações
   - Clique "Criar Curso"

3. **Gerenciar progresso**:
   - Entre nos detalhes de um curso
   - Marque aulas como concluídas usando os checkboxes
   - Observe a atualização do progresso em tempo real

4. **Editar informações**:
   - No dashboard: botão "✏️" para editar curso
   - Nos detalhes: botão "✏️ Editar" para anotações

#### 4. Verificação de Funcionamento

**Teste rápido de integração:**
```bash
# Em um terceiro terminal, teste a API diretamente:
curl http://127.0.0.1:5000/api/health

# Resposta esperada: {"success": true, "message": "API funcionando corretamente"}
```

**Indicadores visuais de sucesso:**
- ✅ Dashboard carrega com estatísticas
- ✅ Lista de cursos aparece (mínimo 2 cursos exemplo)
- ✅ Modal de criação abre/fecha corretamente
- ✅ Navegação entre páginas funciona
- ✅ Checkboxes respondem ao clique
- ✅ Rodapé mostra "🟢 API Online"

---

## 🛠 Comandos Úteis para Desenvolvimento

### Backend
```bash
# Reiniciar banco de dados (apaga dados)
python init_db.py

# Executar testes da API
python test_api.py

# Verificar status da API
curl http://127.0.0.1:5000/api/health
```

### Frontend
```bash
# Limpar cache e reinstalar dependências
rm -rf node_modules package-lock.json
npm install

# Build para produção
npm run build

# Visualizar build de produção
npm run preview
```

### Ambos
```bash
# Parar servidores
Ctrl + C  # Em cada terminal

# Reiniciar aplicação completa
# Terminal 1: cd backend && python app.py
# Terminal 2: cd frontend && npm run dev
```

---

## 🔍 Solução de Problemas

### Problemas Comuns

#### 1. "CORS Error" no navegador
**Causa**: Backend não está rodando ou CORS mal configurado
**Solução**:
```bash
# Verifique se o backend está rodando
curl http://127.0.0.1:5000/api/health

# Se não estiver, inicie:
cd backend && python app.py
```

#### 2. "npm: command not found"
**Causa**: Node.js não instalado
**Solução**: Instale Node.js de [nodejs.org](https://nodejs.org/)

#### 3. "python: command not found"
**Causa**: Python não instalado ou não no PATH
**Solução**: Instale Python de [python.org](https://python.org/) e adicione ao PATH

#### 4. Erro "Address already in use"
**Causa**: Porta já está sendo usada
**Solução**:
```bash
# Windows - matar processo na porta 5000
netstat -ano | findstr :5000
taskkill /PID [PID] /F

# Linux/macOS - matar processo na porta 5000
lsof -ti:5000 | xargs kill -9
```

#### 5. Frontend não carrega dados
**Causa**: Backend não está rodando ou URL incorreta
**Verificação**:
1. Confirme que backend está em `http://127.0.0.1:5000`
2. Teste: `curl http://127.0.0.1:5000/api/cursos`
3. Verifique console do navegador (F12)

---

## 📚 Próximos Passos

Após configurar com sucesso:

1. **Explore a aplicação** usando o fluxo recomendado acima
2. **Leia a documentação técnica** em `DEPLOYMENT.md`
3. **Consulte detalhes do frontend** em `frontend/README.md`
4. **Para produção**, veja `INSTALL.md` e `DEPLOYMENT.md`

---

## 🎯 Resumo de Comandos Rápidos

### Inicialização Rápida (Primeira Vez)
```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python app.py

# Frontend (novo terminal)
cd frontend
npm install
npm run dev
```

### Execução Diária
```bash
# Backend
cd backend && venv\Scripts\activate && python app.py

# Frontend (novo terminal)  
cd frontend && npm run dev
```

**🎉 Aplicação rodando em: `http://localhost:3000`**

---

*Desenvolvido com ❤️ - Sistema WebCurso para Gerenciamento de Cursos*