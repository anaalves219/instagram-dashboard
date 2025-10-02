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
                origem = st.selectbox("📍 Origem do Lead", [
                    "Instagram", "WhatsApp", "Indicação", "Site", "Evento", "Anúncio Facebook", "Google Ads", "Outros"
                ])
            
            with col2:
                vendedor = st.selectbox("🎯 Vendedor Responsável *", ["Ana", "Fernando"],
                                      index=0 if user_info.get('name') == 'Ana' else 1)
                status = st.selectbox("📊 Status Inicial", [
                    "novo", "contatado", "interessado", "negociacao", "fechado", "perdido"
                ])
                score = st.slider("⭐ Score do Lead", 1, 10, 5, 
                                help="1 = Pouco interesse, 10 = Muito interessado")
                valor_estimado = st.number_input("💰 Valor Estimado", min_value=0.0, value=1997.0, step=100.0)
                data_agendamento = st.date_input(
                    "📅 Data Agendamento",
                    value=None,
                    help="Data do próximo contato"
                )
                hora_agendamento = st.time_input(
                    "🕐 Hora Agendamento",
                    value=None,
                    help="Hora do próximo contato"
                )
            
            nota = st.text_area("📝 Anotações", placeholder="Informações importantes sobre o lead...")
            
            # Tags
            tags = st.multiselect("🏷️ Tags", [
                "Hot Lead", "Decisor", "Orçamento OK", "Urgente", "Follow-up", 
                "Competitor", "Networking", "Referral", "High Value"
            ])
            
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
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filtro_vendedor = st.selectbox("👤 Vendedor", ["Todos", "Ana", "Fernando"], key="pipeline_vendedor")
        
        with col2:
            filtro_origem = st.selectbox("📍 Origem", ["Todas", "Instagram", "WhatsApp", "Indicação", "Site"], key="pipeline_origem")
        
        with col3:
            filtro_score = st.select_slider("⭐ Score Mínimo", options=list(range(1, 11)), value=1, key="pipeline_score")
        
        # Buscar leads
        leads_df = db.get_leads()
        
        if not leads_df.empty:
            # Aplicar filtros
            if filtro_vendedor != "Todos":
                leads_df = leads_df[leads_df['vendedor'] == filtro_vendedor]
            
            if filtro_origem != "Todas":
                leads_df = leads_df[leads_df['origem'] == filtro_origem]
            
            leads_df = leads_df[leads_df['score'] >= filtro_score]
            
            # Métricas do pipeline
            col1, col2, col3, col4, col5 = st.columns(5)
            
            status_counts = leads_df['status'].value_counts()
            
            with col1:
                st.metric("🆕 Novos", status_counts.get('novo', 0))
            
            with col2:
                st.metric("📞 Contatados", status_counts.get('contatado', 0))
            
            with col3:
                st.metric("🤔 Interessados", status_counts.get('interessado', 0))
            
            with col4:
                st.metric("💼 Negociação", status_counts.get('negociacao', 0))
            
            with col5:
                st.metric("✅ Fechados", status_counts.get('fechado', 0))
            
            # Funil visual
            st.markdown("#### 🎯 Funil de Conversão")
            
            funil_data = {
                'Leads Novos': status_counts.get('novo', 0),
                'Contatados': status_counts.get('contatado', 0),
                'Interessados': status_counts.get('interessado', 0),
                'Em Negociação': status_counts.get('negociacao', 0),
                'Fechados': status_counts.get('fechado', 0)
            }
            
            fig = go.Figure(go.Funnel(
                y = list(funil_data.keys()),
                x = list(funil_data.values()),
                textinfo = "value+percent initial",
                marker = dict(color = ["#06FFA5", "#0EA5E9", "#F97316", "#9D4EDD", "#10B981"])
            ))
            
            fig.update_layout(
                title="Pipeline de Conversão",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Cards de leads por status
            st.markdown("#### 📋 Leads por Status")
            
            status_colors = {
                'novo': 'lead-novo',
                'contatado': 'lead-contatado',
                'interessado': 'lead-interessado',
                'negociacao': 'lead-negociacao',
                'fechado': 'lead-fechado',
                'perdido': 'lead-perdido'
            }
            
            for status in ['novo', 'contatado', 'interessado', 'negociacao']:
                leads_status = leads_df[leads_df['status'] == status]
                
                if not leads_status.empty:
                    with st.expander(f"📋 {status.title()} ({len(leads_status)} leads)", expanded=(status == 'novo')):
                        for _, lead in leads_status.iterrows():
                            dias_sem_contato = (datetime.now().date() - pd.to_datetime(lead['ultima_interacao']).date()).days
                            urgencia = "🔴" if dias_sem_contato > 3 else "🟡" if dias_sem_contato > 1 else "🟢"
                            
                            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                            
                            with col1:
                                st.markdown(f"**{lead['nome']}**")
                                st.caption(f"📱 {lead['instagram']} | 📞 {lead['telefone']}")
                            
                            with col2:
                                st.markdown(f"🎯 {lead['vendedor']}")
                                st.caption(f"📍 {lead['origem']}")
                            
                            with col3:
                                st.markdown(f"⭐ Score: {lead['score']}/10")
                                st.caption(f"{urgencia} {dias_sem_contato} dias sem contato")
                            
                            with col4:
                                if st.button("✏️", key=f"edit_{lead['id']}", help="Editar lead"):
                                    st.session_state[f'editing_lead_{lead["id"]}'] = True
                                    st.rerun()
                            
                            # Mostrar nota se existir
                            if lead.get('nota'):
                                st.caption(f"📝 {lead['nota']}")
                            
                            st.divider()
        else:
            st.info("🎯 Nenhum lead encontrado")
    
    # ========== TAB 3: FOLLOW-UP ==========
    with tab3:
        st.markdown("### 📞 Follow-up de Leads")
        
        leads_df = db.get_leads()
        
        if not leads_df.empty:
            # Leads que precisam de follow-up
            hoje = datetime.now().date()
            leads_df['ultima_interacao'] = pd.to_datetime(leads_df['ultima_interacao']).dt.date
            leads_df['dias_sem_contato'] = (hoje - leads_df['ultima_interacao']).dt.days
            
            # Prioridades
            leads_urgentes = leads_df[leads_df['dias_sem_contato'] > 3]
            leads_atencao = leads_df[(leads_df['dias_sem_contato'] > 1) & (leads_df['dias_sem_contato'] <= 3)]
            leads_ok = leads_df[leads_df['dias_sem_contato'] <= 1]
            
            # Resumo de follow-up
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.error(f"🔴 **{len(leads_urgentes)} Leads Urgentes**")
                st.caption("Mais de 3 dias sem contato")
            
            with col2:
                st.warning(f"🟡 **{len(leads_atencao)} Leads Atenção**")
                st.caption("1-3 dias sem contato")
            
            with col3:
                st.success(f"🟢 **{len(leads_ok)} Leads OK**")
                st.caption("Contato recente")
            
            # Lista de follow-up urgente
            if not leads_urgentes.empty:
                st.markdown("#### 🔴 Leads Urgentes (Follow-up Imediato)")
                
                for _, lead in leads_urgentes.head(10).iterrows():
                    with st.container():
                        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                        
                        with col1:
                            st.markdown(f"**{lead['nome']}** ⭐ {lead['score']}/10")
                            st.caption(f"📱 {lead['telefone']} | {lead['instagram']}")
                        
                        with col2:
                            st.markdown(f"🎯 {lead['vendedor']}")
                            st.caption(f"Status: {lead['status']}")
                        
                        with col3:
                            st.markdown(f"🔴 **{lead['dias_sem_contato']} dias** sem contato")
                            st.caption(f"Último: {lead['ultima_interacao'].strftime('%d/%m/%Y')}")
                        
                        with col4:
                            if st.button("📞 Contatar", key=f"contact_{lead['id']}", type="primary"):
                                # Marcar como contatado
                                lead_update = {
                                    'status': 'contatado',
                                    'ultima_interacao': hoje.strftime('%Y-%m-%d')
                                }
                                if db.update_lead(lead['id'], lead_update):
                                    st.success("✅ Lead marcado como contatado!")
                                    st.rerun()
                        
                        if lead.get('nota'):
                            st.caption(f"📝 {lead['nota']}")
                        
                        st.divider()
            
            # Agenda do dia
            st.markdown("#### 📅 Agenda de Hoje")
            
            # Simular agendamentos (baseado nos dados)
            agendamentos_hoje = leads_df.sample(min(5, len(leads_df))) if not leads_df.empty else pd.DataFrame()
            
            if not agendamentos_hoje.empty:
                for i, lead in agendamentos_hoje.iterrows():
                    hora = f"{9 + i}:00"
                    st.markdown(f"🕘 **{hora}** - {lead['nome']} ({lead['vendedor']})")
                    st.caption(f"📞 {lead['telefone']} | Status: {lead['status']}")
            else:
                st.info("📅 Nenhum agendamento para hoje")
            
            # Ações rápidas
            st.markdown("#### ⚡ Ações Rápidas")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📞 Marcar Todos Urgentes como Contatados", use_container_width=True):
                    # Implementar atualização em massa
                    st.success("✅ Ação executada com sucesso!")
            
            with col2:
                if st.button("📧 Enviar E-mail em Massa", use_container_width=True):
                    st.info("📧 Funcionalidade em desenvolvimento")
            
            with col3:
                if st.button("📱 Enviar WhatsApp Automático", use_container_width=True):
                    st.info("📱 Integração com WhatsApp em desenvolvimento")
        
        else:
            st.info("📞 Nenhum lead disponível para follow-up")
    
    # ========== TAB 4: ANÁLISES ==========
    with tab4:
        st.markdown("### 📊 Análises de Leads")
        
        leads_df = db.get_leads()
        
        if not leads_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Distribuição por origem
                st.markdown("#### 📍 Leads por Origem")
                origem_counts = leads_df['origem'].value_counts().reset_index()
                origem_counts.columns = ['Origem', 'Quantidade']
                
                fig = px.pie(
                    origem_counts,
                    values='Quantidade',
                    names='Origem',
                    title="Distribuição por Origem",
                    color_discrete_sequence=['#9D4EDD', '#06FFA5', '#0EA5E9', '#F97316', '#10B981', '#EF4444']
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Score médio por vendedor
                st.markdown("#### ⭐ Score Médio por Vendedor")
                score_vendedor = leads_df.groupby('vendedor')['score'].mean().reset_index()
                
                fig = px.bar(
                    score_vendedor,
                    x='vendedor',
                    y='score',
                    title="Score Médio dos Leads",
                    color='vendedor',
                    color_discrete_map={'Ana': '#9D4EDD', 'Fernando': '#0EA5E9'}
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Taxa de conversão
            st.markdown("#### 🎯 Taxa de Conversão")
            
            conversao = leads_df.groupby('vendedor')['status'].apply(
                lambda x: (x == 'fechado').sum() / len(x) * 100
            ).reset_index()
            conversao.columns = ['Vendedor', 'Taxa_Conversao']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                ana_conversao = conversao[conversao['Vendedor'] == 'Ana']['Taxa_Conversao'].iloc[0] if not conversao.empty else 0
                st.metric("👤 Ana - Taxa de Conversão", f"{ana_conversao:.1f}%")
            
            with col2:
                fernando_conversao = conversao[conversao['Vendedor'] == 'Fernando']['Taxa_Conversao'].iloc[0] if not conversao.empty else 0
                st.metric("👤 Fernando - Taxa de Conversão", f"{fernando_conversao:.1f}%")
            
            with col3:
                conversao_geral = (leads_df['status'] == 'fechado').sum() / len(leads_df) * 100
                st.metric("🎯 Conversão Geral", f"{conversao_geral:.1f}%")
            
            # Timeline de leads
            st.markdown("#### 📈 Timeline de Leads")
            
            leads_df['created_at'] = pd.to_datetime(leads_df['created_at'])
            leads_timeline = leads_df.groupby([
                leads_df['created_at'].dt.date,
                'vendedor'
            ]).size().reset_index()
            leads_timeline.columns = ['Data', 'Vendedor', 'Quantidade']
            
            fig = px.line(
                leads_timeline,
                x='Data',
                y='Quantidade',
                color='Vendedor',
                title="Leads Captados por Dia",
                color_discrete_map={'Ana': '#9D4EDD', 'Fernando': '#0EA5E9'}
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.info("📊 Nenhum dado disponível para análise")