# 🔐 Configuração Google OAuth - Login com Gmail

## 🎯 O que Foi Implementado

### **🚀 Funcionalidades:**
- ✅ Login tradicional (usuário/senha) mantido
- ✅ Login com Google OAuth adicionado
- ✅ Sistema híbrido - duas opções de login
- ✅ E-mails autorizados controlados por código
- ✅ Interface integrada no mesmo formulário

### **🔒 Segurança:**
- ✅ Apenas e-mails pré-autorizados podem acessar
- ✅ OAuth oficial do Google
- ✅ Tokens seguros e temporários
- ✅ Logout específico por método

## 🛠️ Configuração Passo a Passo

### **1. Google Cloud Console**

#### **1.1 Criar/Configurar Projeto:**
1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione existente
3. Nome sugerido: "Instagram Sales Dashboard"

#### **1.2 Habilitar APIs:**
1. Vá em **APIs & Services** > **Library**
2. Procure e habilite:
   - **Google+ API** 
   - **Google Identity Services API**
   - **OAuth2 API**

#### **1.3 Criar Credenciais OAuth:**
1. Vá em **APIs & Services** > **Credentials**
2. Clique **+ Create Credentials** > **OAuth 2.0 Client ID**
3. Configure:
   - **Application type**: Web application
   - **Name**: Instagram Sales Dashboard
   - **Authorized JavaScript origins**: 
     - `https://your-app.streamlit.app` (sua URL do Streamlit)
   - **Authorized redirect URIs**: 
     - `https://your-app.streamlit.app` (mesma URL)

### **2. Configurar Streamlit Cloud**

#### **2.1 Secrets do Streamlit:**
1. Vá no seu app no **Streamlit Cloud**
2. **Settings** > **Secrets**
3. Adicione:

```toml
# Supabase (existente)
SUPABASE_URL = "sua-url-supabase"
SUPABASE_ANON_KEY = "sua-chave-supabase"

# Google OAuth (NOVO)
GOOGLE_CLIENT_ID = "123456789-abc123.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "GOCSPX-abc123def456ghi789"
```

#### **2.2 Obter Client ID e Secret:**
1. No Google Cloud Console > **Credentials**
2. Clique no OAuth 2.0 Client ID criado
3. Copie:
   - **Client ID** → `GOOGLE_CLIENT_ID`
   - **Client Secret** → `GOOGLE_CLIENT_SECRET`

### **3. Configurar E-mails Autorizados**

#### **3.1 Editar Lista de E-mails:**
No arquivo `utils/google_auth.py`, edite:

```python
AUTHORIZED_EMAILS = {
    "ana.vendedora@gmail.com": {
        "name": "Ana",
        "role": "vendedora", 
        "theme": {"primary": "#9D4EDD", "secondary": "#06FFA5"}
    },
    "fernando.vendedor@gmail.com": {
        "name": "Fernando",
        "role": "vendedor",
        "theme": {"primary": "#0EA5E9", "secondary": "#F97316"}
    },
    "seuemail@gmail.com": {
        "name": "Seu Nome",
        "role": "vendedor",
        "theme": {"primary": "#9D4EDD", "secondary": "#06FFA5"}
    }
}
```

#### **3.2 Atualizar Redirect URI:**
No arquivo `utils/google_auth.py`, linha 9:
```python
REDIRECT_URI = "https://sua-url-real.streamlit.app"
```

## ✅ Como Testar

### **1. Teste Local (Limitado):**
- Login tradicional funciona normalmente
- Google OAuth precisa de HTTPS (não funciona local)

### **2. Teste Produção:**
1. **Deploy** no Streamlit Cloud
2. **Configure** secrets com credenciais Google
3. **Teste** login tradicional
4. **Teste** login com Google
5. **Verifique** se apenas e-mails autorizados acessam

## 🎯 Interface do Usuário

### **Tela de Login:**
```
🚀 Instagram Sales
Dashboard de Vendas High Ticket

🔐 Acesso ao Sistema
👤 Usuário: [ana ou fernando]
🔑 Senha: [senha]
[🚀 Entrar]

────────────────────

🔐 Ou entre com Google
[🔍 Entrar com Google] <- Botão azul do Google

🔒 Acesso Restrito: Apenas e-mails autorizados

────────────────────

🎮 Credenciais Demo:
- Ana: ana / ana2024
- Fernando: fernando / fernando2024
```

## 🔄 Fluxo de Autenticação

### **Google OAuth Flow:**
1. **Usuário clica** "Entrar com Google"
2. **Redirecionado** para Google
3. **Autoriza** acesso ao app
4. **Google retorna** código de autorização
5. **App troca** código por token
6. **App obtém** informações do usuário
7. **Verifica** se e-mail está autorizado
8. **Se autorizado:** Login realizado
9. **Se não:** Acesso negado

### **Login Tradicional:**
1. **Usuário digita** usuário/senha
2. **Sistema verifica** credenciais
3. **Se correto:** Login realizado
4. **Se incorreto:** Erro exibido

## 🛡️ Segurança Implementada

### **Controle de Acesso:**
- ✅ E-mails whitelist (lista autorizada)
- ✅ OAuth oficial do Google
- ✅ Tokens temporários
- ✅ Sessões isoladas

### **Validações:**
- ✅ Verificação de e-mail autorizado
- ✅ Tokens válidos
- ✅ Redirect URI configurado
- ✅ Secrets protegidos

## 🚀 Vantagens do Sistema

### **Para Usuários:**
- 🔐 **Conveniência**: Login com conta Google
- 🛡️ **Segurança**: Sem necessidade de lembrar senhas
- ⚡ **Rapidez**: Login em 2 cliques
- 🔄 **Flexibilidade**: Dois métodos disponíveis

### **Para Administrador:**
- 🔒 **Controle**: Lista de e-mails autorizados
- 📊 **Rastreamento**: Método de login identificado
- 🛠️ **Manutenção**: Fácil adicionar/remover usuários
- 🔐 **Backup**: Login tradicional sempre disponível

## ⚠️ Resolução de Problemas

### **"Google OAuth não configurado":**
- Verifique `GOOGLE_CLIENT_ID` nos secrets
- Verifique `GOOGLE_CLIENT_SECRET` nos secrets

### **"E-mail não autorizado":**
- Adicione o e-mail em `AUTHORIZED_EMAILS`
- Faça commit e deploy

### **"Erro ao obter token":**
- Verifique redirect URI no Google Cloud
- Deve ser exatamente a URL do seu app

### **"Botão Google não aparece":**
- Verifique se secrets estão configurados
- Aguarde deploy completo

---

🎉 **Sistema de Autenticação Dupla Implementado com Sucesso!**