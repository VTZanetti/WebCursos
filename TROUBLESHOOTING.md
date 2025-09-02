# 🔧 WebCurso - Guia de Solução de Problemas

## 🚨 Problemas Mais Comuns e Soluções

### 1. Erro de CORS no Navegador

**Sintomas:**
- Erro no console: `CORS policy: No 'Access-Control-Allow-Origin' header`
- Frontend não consegue carregar dados
- Requests falhando no Network tab

**Diagnóstico:**
```bash
# Testar se backend está respondendo
curl http://127.0.0.1:5000/api/health
```

**Soluções:**
1. **Backend não está rodando**:
   ```bash
   cd backend
   venv\Scripts\activate  # Windows
   python app.py
   ```

2. **Porta incorreta**:
   - Verifique se API está em `http://127.0.0.1:5000`
   - Confirme CORS configurado para `localhost:3000`

3. **Cache do navegador**:
   ```bash
   # Limpar cache (Ctrl+Shift+R) ou modo incógnito
   ```

---

### 2. Comandos Não Encontrados

#### `npm: command not found`

**Causa:** Node.js não instalado ou não no PATH

**Solução:**
1. Baixar Node.js LTS de: https://nodejs.org/
2. Reiniciar terminal após instalação
3. Verificar: `node --version && npm --version`

#### `python: command not found`

**Causa:** Python não instalado ou não no PATH

**Solução:**
1. Baixar Python de: https://www.python.org/downloads/
2. ⚠️ **IMPORTANTE**: Marcar "Add Python to PATH" durante instalação
3. Reiniciar terminal
4. Verificar: `python --version`

---

### 3. Porta Já Está em Uso

**Sintomas:**
- `Address already in use`
- `Port 5000 is already in use`

**Soluções:**

**Windows:**
```bash
# Encontrar processo usando a porta
netstat -ano | findstr :5000

# Matar processo (substitua PID pelo número encontrado)
taskkill /PID [PID_NUMBER] /F

# Alternativa: matar todos processos Python
taskkill /F /IM python.exe
```

**Linux/macOS:**
```bash
# Encontrar e matar processo
lsof -ti:5000 | xargs kill -9

# Alternativa
sudo fuser -k 5000/tcp
```

---

### 4. Dependências Não Instaladas

#### Erro pip no Backend

**Sintomas:**
- `ModuleNotFoundError: No module named 'flask'`
- `No module named 'flask_cors'`

**Solução:**
```bash
cd backend

# Verificar se ambiente virtual está ativado
# Deve aparecer (venv) no prompt

# Se não ativado:
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# Reinstalar dependências
pip install -r requirements.txt
```

#### Erro npm no Frontend

**Sintomas:**
- `Cannot resolve module 'vue'`
- `Error: Cannot find module`

**Solução:**
```bash
cd frontend

# Limpar cache e reinstalar
rm -rf node_modules package-lock.json  # Linux/macOS
# rmdir /s node_modules & del package-lock.json  # Windows

npm install
```

---

### 5. Banco de Dados Corrompido

**Sintomas:**
- `OperationalError: no such table: cursos`
- `Database is locked`
- Dados não aparecem no frontend

**Soluções:**

1. **Reinicializar banco:**
   ```bash
   cd backend
   
   # Deletar banco atual
   del instance\database.sqlite  # Windows
   # rm instance/database.sqlite  # Linux/macOS
   
   # Recriar banco
   python init_db.py
   ```

2. **Permissões de arquivo:**
   ```bash
   # Verificar permissões da pasta instance
   # Deve ser writeable pelo usuário atual
   ```

---

### 6. Frontend Não Carrega Dados

**Sintomas:**
- Dashboard vazio
- Loading infinito
- "API Offline" no rodapé

**Diagnóstico Passo a Passo:**

1. **Verificar backend:**
   ```bash
   curl http://127.0.0.1:5000/api/health
   # Deve retornar: {"success": true, ...}
   ```

2. **Verificar CORS:**
   ```bash
   curl -H "Origin: http://localhost:3000" http://127.0.0.1:5000/api/cursos
   ```

3. **Console do navegador (F12):**
   - Verificar erros JavaScript
   - Checar Network tab para requests falhando

**Soluções:**
- Reiniciar backend: `python app.py`
- Limpar cache do navegador
- Verificar proxy no `vite.config.js`

---

### 7. Problemas de Performance

#### Backend Lento

**Causas:**
- Muitas requisições simultâneas
- Banco de dados grande
- Debug mode em produção

**Soluções:**
```bash
# Verificar se debug está desabilitado em produção
# Em app.py: app.run(debug=False)

# Otimizar banco (caso necessário)
python -c "
import sqlite3
conn = sqlite3.connect('instance/database.sqlite')
conn.execute('VACUUM')
conn.close()
"
```

#### Frontend Lento

**Causas:**
- Muitos dados sendo carregados
- Componentes não otimizados

**Soluções:**
```bash
# Build de produção otimizada
npm run build
npm run preview

# Verificar bundle size
npm run build -- --analyze
```

---

### 8. Problemas de Ambiente Virtual

#### Virtual Environment Não Ativa

**Sintomas:**
- Comando `pip install` instala globalmente
- ImportError mesmo com dependências "instaladas"

**Soluções:**

**Windows:**
```bash
cd backend

# Recriar ambiente virtual
rmdir /s venv
python -m venv venv
venv\Scripts\activate

# Confirmar ativação (deve aparecer (venv))
pip install -r requirements.txt
```

**Linux/macOS:**
```bash
cd backend

# Recriar ambiente virtual
rm -rf venv
python3 -m venv venv
source venv/bin/activate

# Confirmar ativação (deve aparecer (venv))
pip install -r requirements.txt
```

---

### 9. Problemas de Rede/Firewall

#### Requests Bloqueados

**Sintomas:**
- Timeout errors
- Connection refused
- Firewall warnings

**Soluções:**

1. **Firewall Windows:**
   - Permitir Python/Node.js através do firewall
   - Ou temporariamente desabilitar para teste

2. **Antivírus:**
   - Adicionar pasta do projeto à whitelist
   - Alguns antivírus bloqueiam servidores locais

3. **Proxy corporativo:**
   ```bash
   # Configurar proxy npm (se necessário)
   npm config set proxy http://proxy:port
   npm config set https-proxy http://proxy:port
   ```

---

### 10. Problemas de Versão

#### Versões Incompatíveis

**Sintomas:**
- Warnings sobre versões
- Funcionalidades não funcionando

**Verificação:**
```bash
# Backend
python --version  # Deve ser >= 3.8
pip list | grep -E "(Flask|flask-cors)"

# Frontend  
node --version    # Deve ser >= 16.0
npm list vue      # Deve ser >= 3.4.0
```

**Soluções:**
- Atualizar Python/Node.js se necessário
- Usar versões específicas do requirements.txt/package.json

---

## 🆘 Como Reportar Problemas

Se o problema persistir:

1. **Colete informações:**
   ```bash
   # Versões do sistema
   python --version
   node --version
   npm --version
   
   # Log completo do erro
   # Screenshots do console (F12)
   ```

2. **Passos para reproduzir:**
   - O que você estava tentando fazer
   - Comandos executados
   - Mensagens de erro completas

3. **Ambiente:**
   - Sistema operacional
   - Se está usando virtual environment
   - Se alterou alguma configuração

---

## ✅ Lista de Verificação Rápida

Quando algo não funciona, verifique na ordem:

- [ ] Backend está rodando? (`curl http://127.0.0.1:5000/api/health`)
- [ ] Frontend está rodando? (`http://localhost:3000`)
- [ ] Ambiente virtual ativado? (deve aparecer `(venv)`)
- [ ] Dependências instaladas? (`pip list`, `npm list`)
- [ ] Banco de dados existe? (`ls instance/database.sqlite`)
- [ ] Sem erros no console? (F12 no navegador)
- [ ] Firewall/antivírus não está bloqueando?
- [ ] Versões corretas? (Python >= 3.8, Node >= 16.0)

---

**💡 Dica:** A maioria dos problemas são resolvidos reiniciando ambos os servidores e verificando se as dependências estão instaladas corretamente.