import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, time
from utils.database import Database
from utils.auth import get_current_user

def show_page():
    """Página de Leads - Pipeline de vendas e follow-up"""
    
    st.title("🎯 Gestão de Leads")
    st.markdown("**Pipeline de vendas, classificação e follow-up de leads**")
    
    # Inicializar database
    db = Database()
    user_info = get_current_user()
    
    # Verificar se Supabase está configurado
    if not db.is_connected():
        st.error("""
        ### ⚠️ Supabase Não Configurado
        
        Para usar o gerenciamento de leads:
        1. **Configure o Supabase** seguindo o arquivo `SUPABASE_SETUP.md`
        2. **Adicione suas credenciais** nos secrets do Streamlit Cloud
        3. **Aguarde o restart** automático do app
        """)
        return
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs(["🆕 Novo Lead", "📋 Pipeline", "📞 Follow-up", "📊 Análises"])
    
    # ========== TAB 1: NOVO LEAD ==========
    with tab1:
        st.markdown("### 🆕 Adicionar Novo Lead")
        
        with st.form("novo_lead", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("👤 Nome Completo *", placeholder="Ex: Maria Silva")
                instagram = st.text_input("📱 Instagram", placeholder="@mariasilva")
                telefone = st.text_input("📞 Telefone *", placeholder="(11) 99999-9999")
                email = st.text_input("📧 E-mail", placeholder="maria@email.com")
                origem = st.selectbox("📍 Origem do Lead", 
                    ["Instagram", "WhatsApp", "Indicacao", "Site", "Evento", "Facebook Ads", "Google Ads", "Outros"])
            
            with col2:
                vendedor = st.selectbox("🎯 Vendedor Responsável *", ["Ana", "Fernando"],
                                      index=0 if user_info.get('name') == 'Ana' else 1)
                status = st.selectbox("📊 Status Inicial", 
                    ["novo", "contatado", "interessado", "negociacao", "fechado", "perdido"])
                score = st.slider("⭐ Score do Lead", 1, 10, 5, 
                                help="1 = Pouco interesse, 10 = Muito interessado")
                valor_estimado = st.number_input("💰 Valor Estimado", min_value=0.0, value=1997.0, step=100.0)
                
                # Data e hora de agendamento separadas
                data_agendamento = st.date_input("📅 Data Agendamento", value=None)
                hora_agendamento = st.time_input("🕐 Hora Agendamento", value=None)
            
            nota = st.text_area("📝 Anotações", placeholder="Informações importantes sobre o lead...")
            
            # Tags
            tags = st.multiselect("🏷️ Tags", 
                ["Hot Lead", "Decisor", "Orcamento OK", "Urgente", "Follow-up", 
                 "Competitor", "Networking", "Referral", "High Value"])
            
            submitted = st.form_submit_button("🚀 Adicionar Lead", type="primary", use_container_width=True)
            
            if submitted:
                if not nome or not telefone:
                    st.error("❌ Preencha todos os campos obrigatórios!")
                else:
                    # Combinar data e hora de agendamento
                    agendamento_completo = None
                    if data_agendamento and hora_agendamento:
                        agendamento_completo = datetime.combine(data_agendamento, hora_agendamento).isoformat()
                    elif data_agendamento:
                        agendamento_completo = datetime.combine(data_agendamento, time.min).isoformat()
                    
                    lead_data = {
                        'nome': nome,
                        'instagram': instagram,
                        'telefone': telefone,
                        'email': email,
                        'status': status,
                        'origem': origem,
                        'vendedor': vendedor,
                        'nota': nota,
                        'score': score,
                        'ultima_interacao': datetime.now().date().strftime('%Y-%m-%d'),
                        'data_agendamento': agendamento_completo,
                        'valor_estimado': valor_estimado,
                        'tags': tags,
                        'created_at': datetime.now().isoformat()
                    }
                    
                    if db.add_lead(lead_data):
                        st.success("✅ Lead adicionado com sucesso!")
                        db.log_activity(user_info.get('username', ''), 'Novo Lead', f"Lead {nome} adicionado")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Erro ao adicionar lead. Tente novamente.")
    
    # ========== TAB 2: PIPELINE ==========
    with tab2:
        st.markdown("### 📋 Pipeline de Leads")
        st.info("💡 **Pipeline em desenvolvimento.** Use a tab 'Novo Lead' para adicionar leads.")
    
    # ========== TAB 3: FOLLOW-UP ==========
    with tab3:
        st.markdown("### 📞 Follow-up de Leads")
        st.info("📞 **Follow-up em desenvolvimento.** Funcionalidade será adicionada em breve.")
    
    # ========== TAB 4: ANÁLISES ==========
    with tab4:
        st.markdown("### 📊 Análises de Leads")
        st.info("📈 **Análises em desenvolvimento.** Relatórios serão adicionados em breve.")