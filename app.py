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
    from pages import overview, vendas, leads, financeiro, config, instagram_analytics
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
    
    # Forçar criação e visibilidade da sidebar
    st.sidebar.empty()
    
    # CSS e JS para BLOQUEAR completamente colapso da sidebar
    st.markdown("""
    <style>
    /* Sidebar SEMPRE visível e sem colapso */
    [data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
        min-width: 21rem !important;
        width: 21rem !important;
        position: relative !important;
    }
    [data-testid="stSidebar"] > div {
        min-width: 21rem !important;
        width: 21rem !important;
        display: block !important;
    }
    
    /* REMOVER todos os controles de colapso */
    [data-testid="collapsedControl"],
    button[kind="header"],
    .css-1q8dd3e,
    [aria-label*="collapse"],
    [aria-label*="expand"] {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
        opacity: 0 !important;
    }
    
    /* OCULTAR navegação automática de arquivos */
    [data-testid="stSidebarNav"],
    .css-1544g2n,
    .css-17eq0hr,
    section[data-testid="stSidebar"] > div:first-child > div:first-child {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        overflow: hidden !important;
    }
    
    /* OCULTAR links de arquivos .py/.md na sidebar */
    [data-testid="stSidebar"] a[href*=".py"],
    [data-testid="stSidebar"] a[href*=".md"],
    [data-testid="stSidebar"] [class*="nav"] {
        display: none !important;
    }
    </style>
    
    <script>
    // JavaScript para bloquear colapso e remover navegação
    setTimeout(function() {
        // Remover todos os botões de colapso
        const collapseButtons = document.querySelectorAll('[data-testid="collapsedControl"], button[kind="header"]');
        collapseButtons.forEach(btn => {
            btn.style.display = 'none';
            btn.remove();
        });
        
        // Remover navegação automática de arquivos
        const sidebarNav = document.querySelectorAll('[data-testid="stSidebarNav"], .css-1544g2n, .css-17eq0hr');
        sidebarNav.forEach(nav => {
            nav.style.display = 'none';
            nav.remove();
        });
        
        // Remover links de arquivos .py/.md
        const fileLinks = document.querySelectorAll('[data-testid="stSidebar"] a[href*=".py"], [data-testid="stSidebar"] a[href*=".md"]');
        fileLinks.forEach(link => {
            link.style.display = 'none';
            link.remove();
        });
        
        // Forçar sidebar sempre aberta
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        if (sidebar) {
            sidebar.style.transform = 'none';
            sidebar.style.width = '21rem';
            sidebar.style.minWidth = '21rem';
        }
    }, 100);
    </script>
    """, unsafe_allow_html=True)
    
    # Sidebar com menu
    with st.sidebar:
        st.title("🚀 Instagram Sales")
        
        # Info do usuário logado
        user_info = st.session_state.get('user_info', {})
        st.markdown(f"**Olá, {user_info.get('name', 'Usuário')}!** 👋")
        
        # Menu principal - versão simplificada
        pages = ["📈 Overview", "💰 Vendas", "🎯 Leads", "📱 Instagram Analytics", "💳 Financeiro", "⚙️ Config"]
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
    elif selected == "🎯 Leads":
        leads.show_page()
    elif selected == "📱 Instagram Analytics":
        instagram_analytics.show_page()
    elif selected == "💳 Financeiro":
        financeiro.show_page()
    elif selected == "⚙️ Config":
        config.show_page()

if __name__ == "__main__":
    main()