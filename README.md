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

### Passo 3: Iniciar o Servidor de Desenvolvimento Vue.js

```bash
# Iniciar servidor de desenvolvimento
npm run dev
```

**Saída esperada:**
```
  VITE v5.0.0  ready in 1234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: http://[your-ip]:5173/
```

**✅ Frontend configurado com sucesso! A interface estará disponível em `http://localhost:5173`**

---

## ☁️ Implantação no Servidor Ubuntu com Docker

### 📋 Pré-requisitos para Implantação

1. **Servidor Ubuntu** com acesso SSH
2. **Docker** instalado no servidor
3. **Docker Compose** instalado no servidor
4. **Git** (opcional, para clonar o repositório)

### 🔧 Passos para Implantação

#### 1. Acesse seu servidor Ubuntu via SSH

```bash
ssh zanetti@192.168.0.200
# Senha: password
```

#### 2. Instale o Docker e Docker Compose (se ainda não estiverem instalados)

```bash
# Atualize o sistema
sudo apt update

# Instale dependências
sudo apt install apt-transport-https ca-certificates curl software-properties-common

# Adicione a chave GPG do Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Adicione o repositório do Docker
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Atualize novamente
sudo apt update

# Instale o Docker
sudo apt install docker-ce

# Instale o Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Dê permissão de execução
sudo chmod +x /usr/local/bin/docker-compose

# Adicione seu usuário ao grupo docker
sudo usermod -aG docker $USER

# Reinicie a sessão ou execute:
newgrp docker
```

#### 3. Transfira os arquivos do projeto para o servidor

Você pode usar o `scp` para transferir os arquivos:

```bash
# Na sua máquina local, execute:
scp -r c:\Users\vitor\OneDrive\Documentos\Dev\WebCursos zanetti@192.168.0.200:/home/zanetti/
```

Ou clone o repositório se estiver no GitHub:

```bash
# No servidor Ubuntu
git clone [URL_DO_SEU_REPOSITORIO] WebCursos
cd WebCursos
```

#### 4. Construa e execute os contêineres com Docker Compose

```bash
# Navegue até o diretório do projeto
cd /home/zanetti/WebCursos

# Construa e inicie os serviços
docker-compose up -d
```

#### 5. Acesse a aplicação

Após a implantação, a aplicação estará disponível nos seguintes endereços:

- **Frontend**: http://192.168.0.200:3000
- **Backend API**: http://192.168.0.200:5000
- **Portainer**: http://192.168.0.200:9000 (já disponível)

#### 6. Configuração do Tailscale

Como você já tem o Tailscale configurado no servidor, a aplicação será acessível de todos os seus PCs conectados à mesma rede Tailscale. Você pode acessar usando o IP do Tailscale do seu servidor.

### 🔄 Comandos Úteis do Docker

```bash
# Ver status dos contêineres
docker-compose ps

# Ver logs
docker-compose logs

# Parar os serviços
docker-compose down

# Reconstruir e reiniciar
docker-compose up -d --build

# Ver logs em tempo real
docker-compose logs -f
```

---

## 📡 Endpoints da API

A API RESTful do WebCurso oferece os seguintes endpoints:

### Cursos
- `GET /api/cursos` - Listar todos os cursos
- `POST /api/cursos` - Criar um novo curso
- `GET /api/cursos/<id>` - Obter detalhes de um curso específico
- `PUT /api/cursos/<id>` - Atualizar um curso
- `DELETE /api/cursos/<id>` - Deletar um curso

### Aulas
- `POST /api/cursos/<id>/aula` - Marcar/desmarcar aula como concluída
- `POST /api/cursos/<id>/batch-aulas` - Atualizar múltiplas aulas em lote

### Utilitários
- `GET /api/health` - Verificação de saúde da API
- `GET /api/stats` - Estatísticas gerais

---

## 🛠️ Scripts de Inicialização

O projeto inclui scripts para facilitar a inicialização:

### Windows
- `scripts\start.bat` - Inicia ambos backend e frontend
- `scripts\start.ps1` - Versão PowerShell
- `scripts\start-backend.ps1` - Apenas backend
- `scripts\start-frontend.ps1` - Apenas frontend

### Linux/macOS
- Execute diretamente os comandos Python e npm

---

## 📁 Estrutura do Projeto

```
WebCursos/
├── backend/                 # API Flask
│   ├── app.py              # Aplicação principal
│   ├── database.py         # Gerenciamento de banco de dados
│   ├── init_db.py          # Inicialização do banco de dados
│   ├── requirements.txt    # Dependências Python
│   └── instance/           # Banco de dados SQLite
├── frontend/               # Aplicação Vue.js
│   ├── src/                # Código fonte Vue
│   ├── package.json        # Dependências Node.js
│   └── vite.config.js      # Configuração do Vite
├── scripts/                # Scripts de inicialização
└── docker-compose.yml      # Orquestração Docker
```

---

## 🔒 Segurança

Para uso em produção, considere:

1. **Configurar HTTPS** com Let's Encrypt
2. **Definir variáveis de ambiente** para chaves secretas
3. **Implementar autenticação** de usuários
4. **Configurar um proxy reverso** (Nginx/Apache)
5. **Fazer backup regular** do banco de dados

---

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto é licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 📞 Contato

Seu Nome - [@seu_perfil](https://twitter.com/seu_perfil) - seu.email@exemplo.com

Link do Projeto: [https://github.com/seu_usuario/WebCurso](https://github.com/seu_usuario/WebCurso)