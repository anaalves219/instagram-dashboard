import streamlit as st
import json
import requests
from datetime import datetime
import hashlib

# Configurações OAuth Google
GOOGLE_CLIENT_ID = st.secrets.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = st.secrets.get("GOOGLE_CLIENT_SECRET", "")
REDIRECT_URI = "https://instagram-dashboard-8vfqbyyrmfbnpmsbl3mbts.streamlit.app"

# E-mails autorizados para acessar o sistema
AUTHORIZED_EMAILS = {
    "anaflavia219@gmail.com": {
        "name": "Ana",
        "role": "vendedora",
        "theme": {"primary": "#9D4EDD", "secondary": "#06FFA5"}
    },
    "fernando.vendedor@gmail.com": {
        "name": "Fernando", 
        "role": "vendedor",
        "theme": {"primary": "#0EA5E9", "secondary": "#F97316"}
    }
    # Adicione outros e-mails autorizados aqui
}

def get_google_auth_url():
    """Gera URL de autenticação do Google"""
    if not GOOGLE_CLIENT_ID:
        return None
        
    import urllib.parse
    
    # Parâmetros OAuth2
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid email profile",
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent",
        "state": "streamlit_oauth"
    }
    
    # URL correta do Google OAuth2
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)
    return auth_url

def exchange_code_for_token(code):
    """Troca código de autorização por token de acesso"""
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        return None
        
    token_url = "https://www.googleapis.com/oauth2/v4/token"
    
    data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
        "code": code
    }
    
    try:
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erro OAuth: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Erro ao trocar código por token: {e}")
        return None

def get_user_info(access_token):
    """Obtém informações do usuário usando o token de acesso"""
    user_info_url = f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={access_token}"
    
    try:
        response = requests.get(user_info_url)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Erro ao obter informações do usuário: {e}")
        return None

def is_email_authorized(email):
    """Verifica se o e-mail está autorizado a acessar o sistema"""
    return email.lower() in [k.lower() for k in AUTHORIZED_EMAILS.keys()]

def get_user_profile(email):
    """Obtém perfil do usuário baseado no e-mail"""
    for auth_email, profile in AUTHORIZED_EMAILS.items():
        if email.lower() == auth_email.lower():
            return profile
    return None

def authenticate_with_google():
    """Processo completo de autenticação com Google"""
    
    # Verificar se há código de autorização na URL
    code = None
    try:
        query_params = st.query_params
        if "code" in query_params:
            code = query_params["code"]
    except:
        # Fallback para versão mais antiga do Streamlit
        try:
            query_params = st.experimental_get_query_params()
            if "code" in query_params:
                code = query_params["code"][0]
        except:
            return False
    
    if code:
        # Debug: mostrar código recebido (apenas primeiros caracteres por segurança)
        st.write(f"🔍 Debug: Código OAuth recebido: {code[:20]}...")
        
        # Limpar código se necessário (remover espaços, quebras de linha)
        import urllib.parse
        code = urllib.parse.unquote(code.strip())
        
        # Trocar código por token
        token_data = exchange_code_for_token(code)
        
        if token_data and "access_token" in token_data:
            # Obter informações do usuário
            user_info = get_user_info(token_data["access_token"])
            
            if user_info and "email" in user_info:
                email = user_info["email"]
                
                # Verificar se e-mail está autorizado
                if is_email_authorized(email):
                    user_profile = get_user_profile(email)
                    
                    # Salvar na sessão
                    st.session_state['authenticated'] = True
                    st.session_state['auth_method'] = 'google'
                    st.session_state['user_info'] = {
                        "username": email.split('@')[0],
                        "email": email,
                        "name": user_profile["name"],
                        "role": user_profile["role"],
                        "theme": user_profile["theme"],
                        "login_time": datetime.now().isoformat(),
                        "profile_picture": user_info.get("picture", "")
                    }
                    
                    # Limpar parâmetros da URL
                    try:
                        st.query_params.clear()
                    except:
                        st.experimental_set_query_params()
                    st.success(f"✅ Login realizado com sucesso! Bem-vindo(a), {user_profile['name']}!")
                    st.rerun()
                    
                else:
                    st.error(f"❌ E-mail {email} não autorizado a acessar o sistema!")
                    try:
                        st.query_params.clear()
                    except:
                        st.experimental_set_query_params()
                    
            else:
                st.error("❌ Erro ao obter informações do usuário do Google")
                
        else:
            st.error("❌ Erro ao obter token de acesso do Google")
    
    return False

def show_google_login_button():
    """Exibe botão de login com Google"""
    if not GOOGLE_CLIENT_ID:
        st.warning("⚠️ Google OAuth não configurado. Configure GOOGLE_CLIENT_ID e GOOGLE_CLIENT_SECRET nos secrets.")
        return False
        
    auth_url = get_google_auth_url()
    
    if auth_url:
        st.markdown("""
        <style>
        .google-btn {
            display: inline-flex;
            align-items: center;
            background-color: #4285f4;
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 500;
            font-size: 1rem;
            margin: 0.5rem 0;
            transition: background-color 0.3s ease;
            border: none;
            cursor: pointer;
            width: 100%;
            justify-content: center;
        }
        .google-btn:hover {
            background-color: #3367d6;
            color: white;
            text-decoration: none;
        }
        .google-icon {
            width: 20px;
            height: 20px;
            margin-right: 8px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <a href="{auth_url}" class="google-btn" target="_blank">
            <svg class="google-icon" viewBox="0 0 24 24">
                <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            Entrar com Google
        </a>
        <br><br>
        <small style="color: #666;">O login será aberto em uma nova aba. Após autorizar, volte para esta página.</small>
        """, unsafe_allow_html=True)
        
        return True
    
    return False

def logout_google():
    """Logout específico para autenticação Google"""
    if st.session_state.get('auth_method') == 'google':
        # Limpar sessão
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Configuração simplificada para desenvolvimento/teste
def setup_google_oauth_instructions():
    """Instruções para configurar Google OAuth"""
    return """
## 🔧 Configuração Google OAuth

### 1. **Google Cloud Console**
1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione existente
3. Habilite **Google+ API** e **Google OAuth2 API**

### 2. **Credenciais OAuth**
1. Vá em **APIs & Services** > **Credentials**
2. Clique **Create Credentials** > **OAuth 2.0 Client ID**
3. Application type: **Web application**
4. Authorized redirect URIs: `https://your-app.streamlit.app`

### 3. **Streamlit Secrets**
Adicione no Streamlit Cloud (Settings > Secrets):
```toml
GOOGLE_CLIENT_ID = "your-client-id.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "your-client-secret"
```

### 4. **E-mails Autorizados**
Edite `AUTHORIZED_EMAILS` em `utils/google_auth.py` com os e-mails permitidos.
"""