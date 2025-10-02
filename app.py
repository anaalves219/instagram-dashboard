import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import hashlib
from streamlit_option_menu import option_menu

# Configuração da página
st.set_page_config(
    page_title="Instagram Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS para sidebar - versão simplificada
st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: block !important;
}
.css-1d391kg {
    display: block !important;
}
</style>
""", unsafe_allow_html=True)

# Import das páginas
try:
    from pages import overview, vendas, batalha, financeiro, config
except Exception as e:
    st.error(f"Erro ao importar páginas: {e}")
    st.stop()
from utils.auth import check_authentication, login_page
from utils.database import Database
from utils.styles import apply_custom_css

# Inicializar banco de dados
@st.cache_resource
def init_database():
    return Database()

def main():
    # Aplicar CSS customizado
    apply_custom_css()
    
    # Verificar autenticação
    if not check_authentication():
        login_page()
        return
    
    # Inicializar database
    db = init_database()
    
    # Forçar criação da sidebar
    st.sidebar.empty()
    
    # Sidebar com menu
    with st.sidebar:
        st.title("🚀 Instagram Sales")
        
        # Info do usuário logado
        user_info = st.session_state.get('user_info', {})
        st.markdown(f"**Olá, {user_info.get('name', 'Usuário')}!** 👋")
        
        # Menu principal - versão simplificada (sem Leads temporariamente)
        pages = ["📈 Overview", "💰 Vendas", "⚔️ Batalha", "💳 Financeiro", "⚙️ Config"]
        selected = st.selectbox("Navegar para:", pages, key="main_menu")
        
        # Tema do usuário
        theme_colors = {
            "Ana": {"primary": "#9D4EDD", "secondary": "#06FFA5"},
            "Fernando": {"primary": "#0EA5E9", "secondary": "#F97316"}
        }
        
        user_theme = theme_colors.get(user_info.get('name'), theme_colors["Ana"])
        st.session_state['user_theme'] = user_theme
        
        # Botão de logout
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
    
    # Renderizar página selecionada
    if selected == "📈 Overview":
        overview.show_page()
    elif selected == "💰 Vendas":
        vendas.show_page()
    elif selected == "⚔️ Batalha":
        batalha.show_page()
    elif selected == "💳 Financeiro":
        financeiro.show_page()
    elif selected == "⚙️ Config":
        config.show_page()

if __name__ == "__main__":
    main()