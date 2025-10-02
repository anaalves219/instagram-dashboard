# 📱 Configuração Instagram API - Guia Completo

## 🎯 O que você vai conseguir

- ✅ Dados reais de followers, reach, impressões
- ✅ Análise de posts com métricas completas  
- ✅ Demografia da audiência
- ✅ Performance de hashtags
- ✅ Insights de engajamento
- ✅ Token de longo prazo (60 dias)

## 🚀 Passo a Passo

### **1. Meta for Developers (Facebook)**

#### **1.1 Criar App:**
1. Acesse [developers.facebook.com](https://developers.facebook.com)
2. **Create App** → **Business** → **Next**
3. **App Display Name**: "Instagram Sales Dashboard"
4. **App Contact Email**: seu email
5. **Create App**

#### **1.2 Adicionar Instagram Basic Display:**
1. No dashboard do app → **Add Product**
2. Encontre **Instagram Basic Display** → **Set Up**
3. **Create New App** → Confirme

#### **1.3 Configurar Instagram Basic Display:**
1. **Settings** → **Basic Display**
2. **Instagram App ID**: Anote este ID
3. **Instagram App Secret**: Anote este Secret
4. **Valid OAuth Redirect URIs**: 
   ```
   https://instagram-dashboard-8vfqbyyrmfbnpmsbl3mbts.streamlit.app/
   https://localhost:8501/
   ```

### **2. Instagram Business Account**

#### **2.1 Converter para Business:**
1. No Instagram app → **Configurações**
2. **Conta** → **Mudar para conta profissional**
3. **Empresa** ou **Criador** (escolha Empresa)
4. **Categoria**: Marketing/Vendas
5. **Finalizar**

#### **2.2 Conectar com Facebook:**
1. **Configurações** → **Conta** 
2. **Páginas vinculadas** → **Conectar página**
3. Conecte com uma página do Facebook (crie se necessário)

### **3. Obter Access Token**

#### **3.1 Autorizar App:**
1. Abra este URL no navegador (substitua APP_ID):
   ```
   https://api.instagram.com/oauth/authorize?client_id={APP_ID}&redirect_uri=https://localhost:8501/&scope=user_profile,user_media&response_type=code
   ```

2. **Autorize** o acesso ao seu Instagram

3. Você será redirecionado para:
   ```
   https://localhost:8501/?code=AUTHORIZATION_CODE
   ```

4. **Copie o código** da URL

#### **3.2 Trocar código por token:**
```bash
curl -X POST \
  https://api.instagram.com/oauth/access_token \
  -F client_id={APP_ID} \
  -F client_secret={APP_SECRET} \
  -F grant_type=authorization_code \
  -F redirect_uri=https://localhost:8501/ \
  -F code={AUTHORIZATION_CODE}
```

**Resposta:**
```json
{
  "access_token": "IGQVJYeUk5...",
  "user_id": 123456789
}
```

#### **3.3 Converter para token de longo prazo:**
```bash
curl -i -X GET \
  "https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret={APP_SECRET}&access_token={SHORT_LIVED_TOKEN}"
```

**Resposta:**
```json
{
  "access_token": "IGQVJXeUk5Y...",
  "token_type": "bearer",
  "expires_in": 5183944
}
```

### **4. Obter Business Account ID**

```bash
curl -i -X GET \
  "https://graph.instagram.com/me?fields=id,username&access_token={LONG_LIVED_TOKEN}"
```

**Resposta:**
```json
{
  "id": "17841456781234567",
  "username": "seu_username"
}
```

### **5. Configurar Streamlit Secrets**

No Streamlit Cloud → **Settings** → **Secrets**:

```toml
# Instagram API (OBRIGATÓRIO para Analytics)
INSTAGRAM_TOKEN = "IGQVJXeUk5Y_LONG_LIVED_TOKEN_AQUI"
INSTAGRAM_BUSINESS_ID = "17841456781234567"

# Existing secrets
SUPABASE_URL = "sua_url_supabase"
SUPABASE_ANON_KEY = "sua_chave_supabase"
GOOGLE_CLIENT_ID = "seu_google_client_id"
GOOGLE_CLIENT_SECRET = "seu_google_client_secret"
```

## 🔄 Renovação Automática do Token

### **Script Python para renovar:**

```python
import requests
import streamlit as st

def refresh_instagram_token():
    """Renova token do Instagram (60 dias)"""
    
    current_token = st.secrets["INSTAGRAM_TOKEN"]
    
    url = "https://graph.instagram.com/refresh_access_token"
    params = {
        'grant_type': 'ig_refresh_token',
        'access_token': current_token
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        new_token = data['access_token']
        expires_in = data['expires_in']  # segundos
        
        print(f"✅ Token renovado com sucesso!")
        print(f"🕐 Expira em: {expires_in // 86400} dias")
        print(f"🔑 Novo token: {new_token[:20]}...")
        
        return new_token
    else:
        print(f"❌ Erro ao renovar token: {response.text}")
        return None

# Executar
if __name__ == "__main__":
    refresh_instagram_token()
```

## 📊 APIs Disponíveis

### **Instagram Basic Display API:**
- ✅ Posts do usuário
- ✅ Informações básicas
- ✅ Mídia (fotos/vídeos)
- ❌ Insights/Analytics

### **Instagram Graph API (Business):**
- ✅ Insights detalhados
- ✅ Demografia da audiência  
- ✅ Métricas de posts
- ✅ Hashtag analytics
- ✅ Story insights

## 🧪 Testando a Configuração

### **1. Verificar token:**
```bash
curl -i -X GET \
  "https://graph.instagram.com/me?fields=id,username,media_count,followers_count&access_token={TOKEN}"
```

### **2. Buscar insights:**
```bash
curl -i -X GET \
  "https://graph.instagram.com/{USER_ID}/insights?metric=impressions,reach,profile_views&period=day&access_token={TOKEN}"
```

### **3. Listar posts:**
```bash
curl -i -X GET \
  "https://graph.instagram.com/{USER_ID}/media?fields=id,caption,media_type,timestamp,like_count,comments_count&access_token={TOKEN}"
```

## ⚠️ Limitações e Rate Limits

### **Rate Limits:**
- **Basic Display**: 200 calls/hour/user
- **Graph API**: 4800 calls/hour/app
- **Insights**: 240 calls/hour/user

### **Cache Strategy:**
```python
@st.cache_data(ttl=3600)  # 1 hora
def get_instagram_data():
    # Sua função aqui
    pass
```

### **Dados Disponíveis:**

#### **Account Insights:**
- Impressions
- Reach  
- Profile views
- Website clicks
- Follower count

#### **Media Insights:**
- Likes
- Comments
- Saves
- Shares
- Reach
- Impressions
- Engagement rate

#### **Audience Insights:**
- Gender
- Age range
- Top cities
- Top countries

## 🔧 Troubleshooting

### **Erro: "Invalid access token"**
- ✅ Verificar se token não expirou
- ✅ Renovar token
- ✅ Verificar se Business Account está configurado

### **Erro: "Insufficient privileges"**
- ✅ Conta deve ser Business ou Creator
- ✅ App deve ter permissões corretas
- ✅ Verificar se app foi aprovado pelo Facebook

### **Erro: "Rate limit exceeded"**
- ✅ Implementar cache (1 hora recomendado)
- ✅ Reduzir frequência de calls
- ✅ Usar batch requests quando possível

### **Dados não aparecem:**
- ✅ Aguardar 24-48h após converter para Business
- ✅ Verificar se há posts recentes
- ✅ Verificar se Business Account tem atividade mínima

## 📚 Links Úteis

- **[Meta for Developers](https://developers.facebook.com)**
- **[Instagram Basic Display API](https://developers.facebook.com/docs/instagram-basic-display-api)**  
- **[Instagram Graph API](https://developers.facebook.com/docs/instagram-api)**
- **[API Explorer](https://developers.facebook.com/tools/explorer/)**
- **[Rate Limiting](https://developers.facebook.com/docs/graph-api/overview/rate-limiting/)**

---

🎉 **Após configurar, você terá acesso completo aos dados reais do Instagram no dashboard!**