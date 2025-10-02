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

# CSS para forçar sidebar sempre visível
st.markdown("""
<style>
/* Forçar sidebar sempre visível */
.css-1d391kg, [data-testid="stSidebar"] {
    display: block !important;
    visibility: visible !important;
    width: 300px !important;
}

/* Botão de colapsar sidebar */
[data-testid="collapsedControl"] {
    display: none !important;
}

/* Container principal */
.main .block-container {
    padding-left: 1rem !important;
    max-width: none !important;
}
</style>
""", unsafe_allow_html=True)

# Import das páginas
from pages import overview, vendas, leads, batalha, financeiro, config
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
    
    # Sidebar com menu
    with st.sidebar:
        st.title("🚀 Instagram Sales")
        
        # Info do usuário logado
        user_info = st.session_state.get('user_info', {})
        st.markdown(f"**Olá, {user_info.get('name', 'Usuário')}!** 👋")
        
        # Menu principal
        selected = option_menu(
            menu_title=None,
            options=["📈 Overview", "💰 Vendas", "🎯 Leads", "⚔️ Batalha", "💳 Financeiro", "⚙️ Config"],
            icons=["graph-up", "currency-dollar", "bullseye", "lightning", "credit-card", "gear"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#0E1117"},
                "icon": {"color": "#FAFAFA", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#262730",
                    "color": "#FAFAFA"
                },
                "nav-link-selected": {"background-color": "#9D4EDD"},
            }
        )
        
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
    elif selected == "🎯 Leads":
        leads.show_page()
    elif selected == "⚔️ Batalha":
        batalha.show_page()
    elif selected == "💳 Financeiro":
        financeiro.show_page()
    elif selected == "⚙️ Config":
        config.show_page()

if __name__ == "__main__":
    main()