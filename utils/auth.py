import streamlit as st
import hashlib
import json
from datetime import datetime

# Configurações de usuários (em produção, mover para secrets)
USERS = {
    "ana": {
        "password_hash": "ec7be197de9fbe3a60c8af23a9ffad7783bb684470c9d137ef4bde4e56354b70",  # senha: ana2024
        "name": "Ana",
        "role": "vendedora",
        "theme": {"primary": "#9D4EDD", "secondary": "#06FFA5"}
    },
    "fernando": {
        "password_hash": "8fd97a694b066d5fb4f251eca8bbdf3f5210321230cfab366a028bff435bff68",  # senha: fernando2024  
        "name": "Fernando",
        "role": "vendedor",
        "theme": {"primary": "#0EA5E9", "secondary": "#F97316"}
    }
}

def hash_password(password: str) -> str:
    """Gera hash da senha"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, password_hash: str) -> bool:
    """Verifica se a senha confere com o hash"""
    return hash_password(password) == password_hash

def authenticate_user(username: str, password: str) -> dict:
    """Autentica usuário e retorna informações"""
    username = username.lower().strip()
    
    if username not in USERS:
        return None
    
    user_data = USERS[username]
    if verify_password(password, user_data["password_hash"]):
        return {
            "username": username,
            "name": user_data["name"],
            "role": user_data["role"],
            "theme": user_data["theme"],
            "login_time": datetime.now().isoformat()
        }
    
    return None

def check_authentication() -> bool:
    """Verifica se o usuário está autenticado"""
    return 'authenticated' in st.session_state and st.session_state['authenticated']

def login_page():
    """Exibe página de login"""
    
    # CSS customizado para a página de login
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        margin-top: 5rem;
    }
    
    .login-title {
        text-align: center;
        color: white;
        font-size: 2.5rem;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    
    .login-subtitle {
        text-align: center;
        color: rgba(255,255,255,0.8);
        margin-bottom: 2rem;
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(255,255,255,0.1);
        border: 2px solid rgba(255,255,255,0.2);
        border-radius: 10px;
        color: white;
        font-size: 1.1rem;
        padding: 0.8rem;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.6);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #06FFA5;
        box-shadow: 0 0 0 2px rgba(6, 255, 165, 0.2);
    }
    
    .login-button {
        background: linear-gradient(45deg, #06FFA5, #9D4EDD);
        border: none;
        border-radius: 10px;
        color: white;
        font-weight: bold;
        font-size: 1.1rem;
        padding: 0.8rem 2rem;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .login-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Container principal
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="login-container">
            <div class="login-title">🚀 Instagram Sales</div>
            <div class="login-subtitle">Dashboard de Vendas High Ticket</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Formulário de login
        with st.form("login_form", clear_on_submit=False):
            st.markdown("### 🔐 Acesso ao Sistema")
            
            username = st.text_input(
                "👤 Usuário",
                placeholder="Digite seu usuário (ana ou fernando)",
                help="Use: ana ou fernando"
            )
            
            password = st.text_input(
                "🔑 Senha",
                type="password",
                placeholder="Digite sua senha",
                help="Ana: ana2024 | Fernando: fernando2024"
            )
            
            submitted = st.form_submit_button(
                "🚀 Entrar",
                use_container_width=True,
                type="primary"
            )
            
            if submitted:
                if not username or not password:
                    st.error("❌ Por favor, preencha todos os campos")
                    return
                
                user_info = authenticate_user(username, password)
                
                if user_info:
                    st.session_state['authenticated'] = True
                    st.session_state['user_info'] = user_info
                    st.success(f"✅ Bem-vindo(a), {user_info['name']}!")
                    st.rerun()
                else:
                    st.error("❌ Usuário ou senha incorretos")
        
        # Informações de demo
        st.markdown("---")
        st.markdown("""
        **🎮 Credenciais Demo:**
        - **Ana**: usuário `ana` | senha `ana2024`
        - **Fernando**: usuário `fernando` | senha `fernando2024`
        
        **📊 Recursos:**
        - Dashboard completo com métricas
        - Sistema de vendas e leads
        - Comparativo entre vendedores
        - Análise financeira e ROI
        - Mobile responsive
        """)

def logout():
    """Realiza logout do usuário"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def get_current_user():
    """Retorna informações do usuário atual"""
    if check_authentication():
        return st.session_state.get('user_info', {})
    return None

def require_auth(func):
    """Decorator para exigir autenticação"""
    def wrapper(*args, **kwargs):
        if not check_authentication():
            login_page()
            return None
        return func(*args, **kwargs)
    return wrapper