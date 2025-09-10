# ⚡ WebCurso - Guia de Início Rápido

## 🚀 Inicialização em 5 Minutos

Este é um guia express para desenvolvedores experientes que desejam executar rapidamente a aplicação WebCurso.

---

## ✅ Pré-requisitos (Verificação Rápida)

```bash
# Verificar se Python e Node.js estão instalados
python --version  # >= 3.8
node --version    # >= 16.0
npm --version     # >= 8.0
```

Se algum comando falhar, instale:
- **Python**: https://www.python.org/downloads/
- **Node.js**: https://nodejs.org/ (versão LTS)

---

## 🔧 Configuração Express

### Backend (Terminal 1)

```bash
# 1. Navegar e configurar ambiente
cd c:\Dev\WebCurso\backend
python -m venv venv

# 2. Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate

# 3. Instalar dependências e inicializar
pip install -r requirements.txt
python init_db.py

# 4. Iniciar API
python app.py
```

**✅ API rodando em: http://127.0.0.1:5000**

### Frontend (Terminal 2)

```bash
# 1. Navegar para frontend
cd c:\Dev\WebCurso\frontend

# 2. Instalar dependências
npm install

# 3. Iniciar desenvolvimento
npm run dev
```

**✅ App rodando em: http://localhost:3000**

---

## 🎯 Teste Rápido

1. **Abrir navegador**: http://localhost:3000
2. **Verificar dashboard**: Deve mostrar cursos exemplo
3. **Criar curso**: Botão "➕ Novo Curso"
4. **Navegar**: Clicar em qualquer card de curso
5. **Marcar aulas**: Checkboxes nos detalhes

---

## 🐛 Problemas Comuns

| Erro | Solução Rápida |
|------|----------------|
| `CORS Error` | Verifique se backend está rodando |
| `npm: command not found` | Instale Node.js |
| `python: command not found` | Instale Python |
| `Address already in use` | Mate processo: `taskkill /F /IM python.exe` |

---

## 📋 Comandos de Desenvolvimento

### Reiniciar Aplicação
```bash
# Parar servidores: Ctrl+C em ambos terminais
# Reiniciar:
# Terminal 1: cd backend && python app.py  
# Terminal 2: cd frontend && npm run dev
```

### Reset Banco de Dados
```bash
cd backend
python init_db.py  # Apaga dados existentes
```

### Testar API Diretamente
```bash
curl http://127.0.0.1:5000/api/health
curl http://127.0.0.1:5000/api/cursos
```

---

## 🎓 Próximos Passos

- **Documentação completa**: `README.md`
- **Deploy para produção**: `DEPLOYMENT.md`
- **Guia de instalação**: `INSTALL.md`
- **Detalhes do frontend**: `frontend/README.md`

---

**🎉 WebCurso pronto para uso! Interface moderna + API robusta**