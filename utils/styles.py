import streamlit as st

def apply_custom_css():
    """Aplica CSS customizado para o dashboard"""
    
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Reset e configurações gerais */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Ocultar elementos do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Configuração da sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #0E1117 0%, #1E1E2E 100%);
    }
    
    /* Cards principais */
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        border-color: #9D4EDD;
    }
    
    /* Métricas de vendas */
    .sales-metric {
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        background: linear-gradient(45deg, #9D4EDD, #06FFA5);
        color: white;
        font-weight: bold;
    }
    
    .sales-metric h3 {
        margin: 0;
        font-size: 2rem;
    }
    
    .sales-metric p {
        margin: 0;
        opacity: 0.9;
    }
    
    /* Cards de vendedores */
    .vendedor-ana {
        background: linear-gradient(135deg, #9D4EDD 0%, #06FFA5 100%);
        border-radius: 15px;
        padding: 1.5rem;
        color: white;
        margin: 1rem 0;
    }
    
    .vendedor-fernando {
        background: linear-gradient(135deg, #0EA5E9 0%, #F97316 100%);
        border-radius: 15px;
        padding: 1.5rem;
        color: white;
        margin: 1rem 0;
    }
    
    /* Tabelas customizadas */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Botões personalizados */
    .stButton > button {
        border-radius: 10px;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
        background: linear-gradient(45deg, #9D4EDD, #06FFA5);
        color: white;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(157, 78, 221, 0.4);
    }
    
    /* Selectbox e inputs */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.2);
        background-color: rgba(255,255,255,0.05);
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.2);
        background-color: rgba(255,255,255,0.05);
    }
    
    /* Alertas customizados */
    .stAlert {
        border-radius: 10px;
        border: none;
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #9D4EDD, #06FFA5);
        border-radius: 10px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        background-color: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(45deg, #9D4EDD, #06FFA5);
        color: white;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        border-radius: 10px;
        background-color: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Containers de métricas */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 1rem;
        backdrop-filter: blur(10px);
    }
    
    /* Dark mode específico */
    .dark-mode {
        background: linear-gradient(135deg, #0E1117 0%, #1E1E2E 100%);
        color: #FAFAFA;
    }
    
    /* Animações */
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translate3d(0, 30px, 0);
        }
        to {
            opacity: 1;
            transform: translate3d(0, 0, 0);
        }
    }
    
    .slide-in {
        animation: slideInUp 0.5s ease-out;
    }
    
    /* Responsividade mobile */
    @media (max-width: 768px) {
        .metric-card {
            margin: 0.25rem 0;
            padding: 1rem;
        }
        
        .sales-metric h3 {
            font-size: 1.5rem;
        }
        
        .vendedor-ana, .vendedor-fernando {
            padding: 1rem;
            margin: 0.5rem 0;
        }
    }
    
    /* Scrollbar customizada */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #9D4EDD, #06FFA5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #06FFA5, #9D4EDD);
    }
    
    /* Tooltips */
    .tooltip {
        position: relative;
        cursor: help;
    }
    
    .tooltip:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0,0,0,0.9);
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        white-space: nowrap;
        z-index: 1000;
    }
    
    /* Cards de status de leads */
    .lead-novo { border-left: 5px solid #06FFA5; }
    .lead-contatado { border-left: 5px solid #0EA5E9; }
    .lead-interessado { border-left: 5px solid #F97316; }
    .lead-negociacao { border-left: 5px solid #9D4EDD; }
    .lead-fechado { border-left: 5px solid #10B981; }
    .lead-perdido { border-left: 5px solid #EF4444; }
    
    /* Indicadores de performance */
    .performance-high {
        background: linear-gradient(45deg, #10B981, #06FFA5);
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .performance-medium {
        background: linear-gradient(45deg, #F97316, #FCD34D);
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .performance-low {
        background: linear-gradient(45deg, #EF4444, #F87171);
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def get_user_theme_css(theme_colors):
    """Retorna CSS personalizado baseado no tema do usuário"""
    return f"""
    <style>
    .user-theme-primary {{
        background: linear-gradient(45deg, {theme_colors['primary']}, {theme_colors['secondary']});
    }}
    
    .user-theme-card {{
        border-left: 4px solid {theme_colors['primary']};
        background: linear-gradient(135deg, {theme_colors['primary']}15, {theme_colors['secondary']}10);
    }}
    
    .user-theme-button {{
        background: linear-gradient(45deg, {theme_colors['primary']}, {theme_colors['secondary']});
        border: none;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    
    .user-theme-button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 5px 15px {theme_colors['primary']}40;
    }}
    </style>
    """

def create_metric_card(title, value, delta=None, delta_color="normal"):
    """Cria um card de métrica customizado"""
    delta_html = ""
    if delta:
        color = "#10B981" if delta_color == "normal" else "#EF4444"
        delta_html = f'<p style="color: {color}; margin: 0; font-size: 0.9rem;">📈 {delta}</p>'
    
    return f"""
    <div class="metric-card">
        <h3 style="margin: 0; color: #FAFAFA; font-size: 2rem;">{value}</h3>
        <p style="margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.8);">{title}</p>
        {delta_html}
    </div>
    """

def create_vendedor_card(nome, vendas, meta, tema="ana"):
    """Cria card específico do vendedor"""
    classe = f"vendedor-{nome.lower()}"
    progresso = min((vendas / meta) * 100, 100) if meta > 0 else 0
    
    return f"""
    <div class="{classe}">
        <h3 style="margin: 0 0 1rem 0;">👤 {nome}</h3>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <p style="margin: 0; font-size: 1.5rem; font-weight: bold;">R$ {vendas:,.2f}</p>
                <p style="margin: 0; opacity: 0.9;">Meta: R$ {meta:,.2f}</p>
            </div>
            <div style="text-align: right;">
                <p style="margin: 0; font-size: 1.2rem; font-weight: bold;">{progresso:.1f}%</p>
                <p style="margin: 0; opacity: 0.9;">da meta</p>
            </div>
        </div>
        <div style="background: rgba(255,255,255,0.2); border-radius: 10px; height: 8px; margin-top: 1rem;">
            <div style="background: white; height: 100%; border-radius: 10px; width: {progresso}%; transition: width 0.3s ease;"></div>
        </div>
    </div>
    """