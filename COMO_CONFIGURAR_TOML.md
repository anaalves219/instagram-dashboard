# 📋 Como Configurar TOML no Streamlit Cloud

## 🎯 Formato TOML (OBRIGATÓRIO)

### **⚠️ IMPORTANTE:**
- **NÃO use** `[secrets]` no Streamlit Cloud
- **Use APENAS** as variáveis diretas
- **Uma variável por linha**
- **Sempre use aspas duplas** para strings

## 📋 CONFIGURAÇÃO MÍNIMA (Funcional)

### **Cole isso no Streamlit Cloud:**
```toml
SUPABASE_URL = "https://seuprojectoid.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNldXByb2plY3RvaWQiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTY5MTU5NzAwMCwiZXhwIjoyMDA3MTczMDAwfQ.sua-chave-anon-muito-longa-aqui"
```

## 🚀 CONFIGURAÇÃO COMPLETA (Com Google OAuth)

### **Cole isso no Streamlit Cloud:**
```toml
# Supabase (OBRIGATÓRIO)
SUPABASE_URL = "https://seuprojectoid.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNldXByb2plY3RvaWQiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTY5MTU5NzAwMCwiZXhwIjoyMDA3MTczMDAwfQ.sua-chave-anon-muito-longa-aqui"

# Google OAuth (OPCIONAL - para login com Gmail)
GOOGLE_CLIENT_ID = "123456789012-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "GOCSPX-abcdefghijklmnopqrstuvwxyz"
```

## 🔧 Como Colocar no Streamlit Cloud

### **Passo a Passo:**

1. **Acesse seu app** no Streamlit Cloud
2. **Clique em "Manage app"** (canto inferior direito)
3. **Vá em "Settings"** (menu lateral)
4. **Clique em "Secrets"**
5. **Cole o código TOML** na caixa de texto
6. **Clique "Save"**
7. **Aguarde o app reiniciar** (2-3 minutos)

### **🖼️ Visual:**
```
┌─ Streamlit Cloud ─────────────────────┐
│  📱 Your App                          │
│  ┌─ Settings ──────────────────────┐  │
│  │  📋 General                     │  │
│  │  🔐 Secrets  ← CLIQUE AQUI     │  │
│  │  🔧 Advanced                   │  │
│  └─────────────────────────────────┘  │
│                                       │
│  ┌─ Secrets ──────────────────────┐   │
│  │ SUPABASE_URL = "https://..."   │   │
│  │ SUPABASE_ANON_KEY = "eyJ..."   │   │
│  │ GOOGLE_CLIENT_ID = "123..."    │   │
│  │ GOOGLE_CLIENT_SECRET = "GOC..."│   │
│  │                                │   │
│  │        [💾 Save]               │   │
│  └────────────────────────────────┘   │
└───────────────────────────────────────┘
```

## ✅ EXEMPLOS CORRETOS

### **✅ CERTO:**
```toml
SUPABASE_URL = "https://abc123.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiJ9..."
GOOGLE_CLIENT_ID = "123-abc.apps.googleusercontent.com"
```

### **❌ ERRADO:**
```toml
[secrets]  ← NÃO USE ISSO
SUPABASE_URL = https://abc123.supabase.co  ← SEM ASPAS
SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiJ9...'  ← ASPAS SIMPLES
```

## 🔍 Como Obter as Chaves

### **🗃️ SUPABASE:**
1. **Vá no Supabase** → Seu projeto
2. **Settings** → **API**
3. **Copie:**
   - **URL**: `https://seuprojectoid.supabase.co`
   - **anon public**: `eyJhbGci...` (chave muito longa)

### **🔐 GOOGLE OAUTH:**
1. **Google Cloud Console** → Seu projeto
2. **APIs & Services** → **Credentials**
3. **OAuth 2.0 Client ID** → Clique no seu
4. **Copie:**
   - **Client ID**: `123456-abc.apps.googleusercontent.com`
   - **Client Secret**: `GOCSPX-abc123def456`

## 🧪 Como Testar

### **1. Após Salvar:**
- App reinicia automaticamente
- Aguarde 2-3 minutos

### **2. Verificar se Funcionou:**
- **Se Supabase OK**: Não aparece "⚠️ Supabase não configurado"
- **Se Google OK**: Aparece botão "Entrar com Google"
- **Se erro**: Aparece mensagem de erro específica

### **3. Logs de Erro:**
- **Clique "Manage app"** → **Logs**
- **Procure por:** "secrets", "SUPABASE", "GOOGLE"

## ⚠️ Problemas Comuns

### **"KeyError: SUPABASE_URL"**
- Verifica se está escrito exatamente: `SUPABASE_URL`
- Verifica se tem aspas duplas
- Aguarda app reiniciar

### **"Google OAuth não configurado"**
- Verifica `GOOGLE_CLIENT_ID` e `GOOGLE_CLIENT_SECRET`
- Verifica se não tem espaços extras
- Confirma se aspas estão corretas

### **"Secrets not found"**
- Clica "Save" novamente
- Aguarda reinicialização completa
- Atualiza página do app

## 🎯 TEMPLATE PRONTO PARA USAR

### **Copie, substitua valores e cole:**
```toml
SUPABASE_URL = "COLE_SUA_URL_SUPABASE_AQUI"
SUPABASE_ANON_KEY = "COLE_SUA_CHAVE_ANON_AQUI"
GOOGLE_CLIENT_ID = "COLE_SEU_CLIENT_ID_AQUI"
GOOGLE_CLIENT_SECRET = "COLE_SEU_CLIENT_SECRET_AQUI"
```

### **Exemplo Real:**
```toml
SUPABASE_URL = "https://xyzabc123.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh5emFiYzEyMyIsInJvbGUiOiJhbm9uIiwiaWF0IjoxNjkxNTk3MDAwLCJleHAiOjIwMDcxNzMwMDB9.suachavemuito_longa_aqui"
GOOGLE_CLIENT_ID = "123456789012-abcdefghijklmnopqrstuvwxyz123456.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "GOCSPX-abcdefGHIJKLmnopqrSTUVwxyz123"
```

## 🚀 Resultado Final

### **Com Configuração Mínima:**
- ✅ Login tradicional funciona
- ✅ Dashboard completo
- ✅ Vendas e Leads operacionais

### **Com Configuração Completa:**
- ✅ Login tradicional funciona
- ✅ Login com Google funciona
- ✅ Sistema híbrido completo
- ✅ Máxima flexibilidade

---

**🎯 Cole o TOML, salve, aguarde reiniciar e teste!**