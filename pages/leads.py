import streamlit as st
import pandas as pd
from datetime import datetime
from utils.database import Database
from utils.auth import get_current_user

def show_page():
    """Página de Leads - Versão simplificada v2.0"""
    
    st.title("🎯 Gestão de Leads")
    st.markdown("**Pipeline de vendas e classificação de leads**")
    
    # Inicializar database
    db = Database()
    user_info = get_current_user()
    
    # Verificar se Supabase está configurado
    if not db.is_connected():
        st.error("⚠️ **Configure o Supabase para usar o sistema de leads.**")
        st.markdown("Veja as instruções no arquivo `SUPABASE_SETUP.md`")
        return
    
    # Buscar leads existentes
    leads_df = db.get_leads()
    
    # Tabs
    tab1, tab2 = st.tabs(["➕ Novo Lead", "📋 Lista de Leads"])
    
    # TAB 1: NOVO LEAD
    with tab1:
        st.markdown("### ➕ Adicionar Novo Lead")
        
        with st.form("form_lead"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome *")
                telefone = st.text_input("Telefone *")
                email = st.text_input("E-mail")
            
            with col2:
                instagram = st.text_input("Instagram")
                vendedor = st.selectbox("Vendedor", ["Ana", "Fernando"])
                score = st.slider("Score", 1, 10, 5)
            
            origem = st.selectbox("Origem", ["Instagram", "WhatsApp", "Site", "Indicacao", "Outros"])
            status = st.selectbox("Status", ["novo", "contatado", "interessado", "negociacao", "fechado", "perdido"])
            nota = st.text_area("Observações")
            
            submitted = st.form_submit_button("Salvar Lead", type="primary")
            
            if submitted:
                if nome and telefone:
                    lead_data = {
                        'nome': nome,
                        'telefone': telefone,
                        'email': email,
                        'instagram': instagram,
                        'vendedor': vendedor,
                        'score': score,
                        'origem': origem,
                        'status': status,
                        'nota': nota,
                        'ultima_interacao': datetime.now().date().strftime('%Y-%m-%d'),
                        'created_at': datetime.now().isoformat()
                    }
                    
                    if db.add_lead(lead_data):
                        st.success("✅ Lead adicionado!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao salvar")
                else:
                    st.error("❌ Nome e telefone são obrigatórios")
    
    # TAB 2: LISTA
    with tab2:
        st.markdown("### 📋 Lista de Leads")
        
        if not leads_df.empty:
            st.dataframe(leads_df, use_container_width=True)
            st.info(f"📊 Total: {len(leads_df)} leads")
        else:
            st.info("📭 Nenhum lead cadastrado ainda")
            st.markdown("Use a aba **'Novo Lead'** para adicionar o primeiro!")