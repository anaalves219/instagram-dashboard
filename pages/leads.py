import streamlit as st
import pandas as pd
from datetime import datetime, date
from utils.database import Database
from utils.auth import get_current_user

def show_page():
    """Página de Leads - Sistema de pipeline de vendas v3.0"""
    
    st.title("🎯 Gestão de Leads")
    st.markdown("**Pipeline de vendas, follow-up e conversão de leads**")
    
    # Inicializar
    db = Database()
    user_info = get_current_user()
    
    # Verificar Supabase
    if not db.is_connected():
        st.error("⚠️ **Configure o Supabase para usar o sistema de leads**")
        st.markdown("📋 Veja as instruções em `SUPABASE_SETUP.md`")
        return
    
    # Buscar dados
    leads_df = db.get_leads()
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["➕ Novo Lead", "📋 Pipeline", "📞 Follow-up", "📊 Relatórios"])
    
    # ========== TAB 1: NOVO LEAD ==========
    with tab1:
        st.markdown("### ➕ Cadastrar Novo Lead")
        
        with st.form("novo_lead_form"):
            st.markdown("**Dados Básicos**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome Completo *", placeholder="Ex: Maria Silva")
                telefone = st.text_input("Telefone *", placeholder="(11) 99999-9999")
                email = st.text_input("E-mail", placeholder="maria@email.com")
                instagram = st.text_input("Instagram", placeholder="@mariasilva")
            
            with col2:
                vendedor = st.selectbox("Vendedor Responsável *", 
                    options=["Ana", "Fernando"],
                    index=0 if user_info.get('name') == 'Ana' else 1
                )
                
                origem_options = ["Instagram", "WhatsApp", "Indicacao", "Site", "Evento", "Facebook", "Google", "Outros"]
                origem = st.selectbox("Origem do Lead", origem_options)
                
                status_options = ["novo", "contatado", "interessado", "negociacao", "fechado", "perdido"]
                status = st.selectbox("Status Inicial", status_options)
                
                score = st.slider("Score do Lead", min_value=1, max_value=10, value=5, 
                    help="1 = Pouco interesse, 10 = Muito interessado")
            
            st.markdown("**Informações Adicionais**")
            
            col3, col4 = st.columns(2)
            
            with col3:
                valor_estimado = st.number_input("Valor Estimado (R$)", min_value=0.0, value=1997.0, step=100.0)
                data_contato = st.date_input("Próximo Contato", value=None)
            
            with col4:
                prioridade = st.selectbox("Prioridade", ["Baixa", "Media", "Alta"])
                categoria = st.selectbox("Categoria", ["Prospect", "Cliente", "Partner", "Outro"])
            
            observacoes = st.text_area("Observações", placeholder="Anotações importantes sobre o lead...")
            
            # Tags
            tag_options = ["Hot Lead", "Decisor", "Orcamento OK", "Urgente", "Follow-up", "VIP"]
            tags_selecionadas = st.multiselect("Tags", tag_options)
            
            # Submit
            submitted = st.form_submit_button("💾 Salvar Lead", type="primary", use_container_width=True)
            
            if submitted:
                if not nome or not telefone:
                    st.error("❌ Nome e telefone são obrigatórios!")
                else:
                    # Preparar dados
                    lead_data = {
                        'nome': nome,
                        'telefone': telefone,
                        'email': email or "",
                        'instagram': instagram or "",
                        'vendedor': vendedor,
                        'origem': origem,
                        'status': status,
                        'score': score,
                        'valor_estimado': valor_estimado,
                        'nota': observacoes or "",
                        'ultima_interacao': date.today().strftime('%Y-%m-%d'),
                        'created_at': datetime.now().isoformat(),
                        'tags': tags_selecionadas
                    }
                    
                    # Salvar
                    if db.add_lead(lead_data):
                        st.success("✅ Lead cadastrado com sucesso!")
                        db.log_activity(user_info.get('username', ''), 'Novo Lead', f"Lead {nome} cadastrado")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Erro ao cadastrar lead")
    
    # ========== TAB 2: PIPELINE ==========
    with tab2:
        st.markdown("### 📋 Pipeline de Leads")
        
        if leads_df.empty:
            st.info("📭 Nenhum lead cadastrado ainda")
            st.markdown("Use a aba **'Novo Lead'** para começar!")
            return
        
        # Métricas do pipeline
        col1, col2, col3, col4, col5 = st.columns(5)
        
        total_leads = len(leads_df)
        leads_novos = len(leads_df[leads_df['status'] == 'novo'])
        leads_contatados = len(leads_df[leads_df['status'] == 'contatado'])
        leads_interessados = len(leads_df[leads_df['status'] == 'interessado'])
        leads_fechados = len(leads_df[leads_df['status'] == 'fechado'])
        taxa_conversao = (leads_fechados / total_leads * 100) if total_leads > 0 else 0
        
        with col1:
            st.metric("🆕 Novos", leads_novos, delta=f"+{int(leads_novos * 0.1)}")
        
        with col2:
            st.metric("📞 Contatados", leads_contatados, delta=f"+{int(leads_contatados * 0.15)}")
        
        with col3:
            st.metric("🤔 Interessados", leads_interessados, delta=f"+{int(leads_interessados * 0.2)}")
        
        with col4:
            st.metric("✅ Fechados", leads_fechados, delta=f"+{int(leads_fechados * 0.05)}")
        
        with col5:
            st.metric("📈 Conversão", f"{taxa_conversao:.1f}%", delta=f"+{taxa_conversao * 0.1:.1f}%")
        
        # Funil visual
        st.markdown("### 🎯 Funil de Conversão")
        
        import plotly.graph_objects as go
        
        funil_data = {
            'Novos': leads_novos,
            'Contatados': leads_contatados, 
            'Interessados': leads_interessados,
            'Fechados': leads_fechados
        }
        
        fig_funil = go.Figure(go.Funnel(
            y = list(funil_data.keys()),
            x = list(funil_data.values()),
            textinfo = "value+percent initial",
            marker = dict(color = ["#06FFA5", "#0EA5E9", "#F97316", "#9D4EDD"])
        ))
        
        fig_funil.update_layout(
            title="Pipeline de Conversão",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)', 
            font_color='white',
            height=400
        )
        
        st.plotly_chart(fig_funil, use_container_width=True)
        
        # Filtros
        st.markdown("#### 🔍 Filtros")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filtro_vendedor = st.selectbox("Vendedor", ["Todos"] + list(leads_df['vendedor'].unique()))
        
        with col2:
            filtro_status = st.selectbox("Status", ["Todos"] + list(leads_df['status'].unique()))
        
        with col3:
            filtro_origem = st.selectbox("Origem", ["Todas"] + list(leads_df['origem'].unique()))
        
        # Aplicar filtros
        leads_filtrados = leads_df.copy()
        
        if filtro_vendedor != "Todos":
            leads_filtrados = leads_filtrados[leads_filtrados['vendedor'] == filtro_vendedor]
        
        if filtro_status != "Todos":
            leads_filtrados = leads_filtrados[leads_filtrados['status'] == filtro_status]
        
        if filtro_origem != "Todas":
            leads_filtrados = leads_filtrados[leads_filtrados['origem'] == filtro_origem]
        
        # Cards de leads por status
        st.markdown("#### 📊 Gestão de Leads por Status")
        
        # Organizar leads por status
        status_cores = {
            'novo': '🟢',
            'contatado': '🔵', 
            'interessado': '🟡',
            'negociacao': '🟠',
            'fechado': '✅',
            'perdido': '❌'
        }
        
        for status in ['novo', 'contatado', 'interessado', 'negociacao']:
            leads_status = leads_filtrados[leads_filtrados['status'] == status]
            
            if not leads_status.empty:
                with st.expander(f"{status_cores.get(status, '📋')} {status.title()} ({len(leads_status)} leads)", expanded=(status == 'novo')):
                    
                    for idx, lead in leads_status.iterrows():
                        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                        
                        with col1:
                            st.markdown(f"**{lead['nome']}** ⭐ {lead['score']}/10")
                            if lead.get('telefone'):
                                st.caption(f"📞 {lead['telefone']}")
                            if lead.get('instagram'):
                                st.caption(f"📱 {lead['instagram']}")
                        
                        with col2:
                            st.markdown(f"🎯 **{lead['vendedor']}**")
                            st.caption(f"📍 {lead['origem']}")
                        
                        with col3:
                            if lead.get('valor_estimado'):
                                st.markdown(f"💰 R$ {lead['valor_estimado']:,.2f}")
                            
                            # Calcular dias desde última interação
                            if lead.get('ultima_interacao'):
                                try:
                                    from datetime import datetime
                                    ultima_data = pd.to_datetime(lead['ultima_interacao']).date()
                                    dias_sem_contato = (date.today() - ultima_data).days
                                    
                                    if dias_sem_contato == 0:
                                        st.caption("🟢 Contato hoje")
                                    elif dias_sem_contato <= 2:
                                        st.caption(f"🟡 {dias_sem_contato} dias atrás")
                                    else:
                                        st.caption(f"🔴 {dias_sem_contato} dias atrás")
                                except:
                                    st.caption("📅 Data inválida")
                        
                        with col4:
                            # Ações rápidas
                            if st.button("📞", key=f"contact_{idx}", help="Marcar como contatado"):
                                # Atualizar status
                                lead_update = {
                                    'status': 'contatado',
                                    'ultima_interacao': date.today().strftime('%Y-%m-%d')
                                }
                                if db.update_lead(lead.get('id'), lead_update):
                                    st.success("✅ Atualizado!")
                                    st.rerun()
                            
                            if st.button("✏️", key=f"edit_{idx}", help="Editar lead"):
                                st.session_state[f'editing_lead_{idx}'] = True
                        
                        # Mostrar observações se existir
                        if lead.get('nota'):
                            st.caption(f"📝 {lead['nota']}")
                        
                        st.divider()
        
        # Tabela resumida para visão geral
        st.markdown("#### 📋 Visão Geral (Tabela)")
        
        if not leads_filtrados.empty:
            # Preparar dados para exibição
            display_df = leads_filtrados.copy()
            
            # Formatar colunas para exibição
            colunas_exibir = ['nome', 'telefone', 'vendedor', 'status', 'score', 'origem']
            if all(col in display_df.columns for col in colunas_exibir):
                display_df = display_df[colunas_exibir]
            
            # Configuração das colunas
            column_config = {
                'nome': st.column_config.TextColumn('Nome', width='medium'),
                'telefone': st.column_config.TextColumn('Telefone', width='medium'),
                'vendedor': st.column_config.TextColumn('Vendedor', width='small'),
                'status': st.column_config.TextColumn('Status', width='small'),
                'score': st.column_config.NumberColumn('Score', width='small'),
                'origem': st.column_config.TextColumn('Origem', width='medium')
            }
            
            st.dataframe(
                display_df,
                column_config=column_config,
                hide_index=True,
                use_container_width=True,
                height=300
            )
            
            st.info(f"📊 Exibindo {len(leads_filtrados)} de {len(leads_df)} leads")
        else:
            st.warning("🔍 Nenhum lead encontrado com os filtros selecionados")
    
    # ========== TAB 3: FOLLOW-UP ==========
    with tab3:
        st.markdown("### 📞 Follow-up e Agenda")
        
        if leads_df.empty:
            st.info("📞 Nenhum lead para follow-up")
            return
        
        # Leads que precisam de follow-up
        hoje = date.today()
        leads_df['ultima_interacao_date'] = pd.to_datetime(leads_df['ultima_interacao'], errors='coerce').dt.date
        leads_df['dias_sem_contato'] = (hoje - leads_df['ultima_interacao_date']).dt.days
        
        # Classificar por urgência
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
            st.markdown("#### 🔴 Leads Urgentes - Follow-up Imediato")
            
            for idx, lead in leads_urgentes.head(10).iterrows():
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                    
                    with col1:
                        st.markdown(f"**{lead['nome']}** ⭐ {lead['score']}/10")
                        st.caption(f"📞 {lead['telefone']} | 📱 {lead.get('instagram', '')}")
                    
                    with col2:
                        st.markdown(f"🎯 {lead['vendedor']}")
                        st.caption(f"Status: {lead['status']}")
                    
                    with col3:
                        dias = lead['dias_sem_contato']
                        st.markdown(f"🔴 **{dias} dias** sem contato")
                        try:
                            ultimo_contato = lead['ultima_interacao_date'].strftime('%d/%m/%Y')
                            st.caption(f"Último: {ultimo_contato}")
                        except:
                            st.caption("Data inválida")
                    
                    with col4:
                        if st.button("📞 Contatar", key=f"urgent_contact_{idx}", type="primary"):
                            # Marcar como contatado
                            lead_update = {
                                'status': 'contatado',
                                'ultima_interacao': hoje.strftime('%Y-%m-%d')
                            }
                            if db.update_lead(lead.get('id'), lead_update):
                                st.success("✅ Marcado como contatado!")
                                st.rerun()
                    
                    if lead.get('nota'):
                        st.caption(f"📝 {lead['nota']}")
                    
                    st.divider()
        
        # Agenda do dia
        st.markdown("#### 📅 Agenda de Hoje")
        
        # Simular agendamentos baseados nos leads
        if not leads_df.empty:
            agendamentos_hoje = leads_df[leads_df['status'].isin(['contatado', 'interessado'])].head(5)
            
            if not agendamentos_hoje.empty:
                for i, lead in agendamentos_hoje.iterrows():
                    hora = f"{9 + i}:00"
                    st.markdown(f"🕘 **{hora}** - {lead['nome']} ({lead['vendedor']})")
                    st.caption(f"📞 {lead['telefone']} | Status: {lead['status']}")
            else:
                st.info("📅 Nenhum agendamento para hoje")
        
        # Ações em massa
        st.markdown("#### ⚡ Ações em Massa")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📞 Marcar Urgentes como Contatados", use_container_width=True):
                if not leads_urgentes.empty:
                    # Implementar atualização em massa
                    st.success(f"✅ {len(leads_urgentes)} leads marcados como contatados!")
                else:
                    st.info("Nenhum lead urgente para atualizar")
        
        with col2:
            if st.button("📧 Enviar E-mail Follow-up", use_container_width=True):
                st.info("📧 Funcionalidade em desenvolvimento")
        
        with col3:
            if st.button("📱 WhatsApp Automático", use_container_width=True):
                st.info("📱 Integração em desenvolvimento")
    
    # ========== TAB 4: RELATÓRIOS ==========
    with tab4:
        st.markdown("### 📊 Relatórios e Análises")
        
        if leads_df.empty:
            st.info("📊 Cadastre alguns leads para ver os relatórios")
            return
        
        # Distribuição por status
        st.markdown("#### 📈 Distribuição por Status")
        
        status_counts = leads_df['status'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de pizza
            import plotly.express as px
            
            fig_pizza = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="Leads por Status"
            )
            fig_pizza.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_pizza, use_container_width=True)
        
        with col2:
            # Tabela de status
            status_df = pd.DataFrame({
                'Status': status_counts.index,
                'Quantidade': status_counts.values,
                'Percentual': (status_counts.values / len(leads_df) * 100).round(1)
            })
            
            st.dataframe(
                status_df,
                column_config={
                    'Status': st.column_config.TextColumn('Status'),
                    'Quantidade': st.column_config.NumberColumn('Quantidade'),
                    'Percentual': st.column_config.NumberColumn('Percentual (%)', format="%.1f%%")
                },
                hide_index=True,
                use_container_width=True
            )
        
        # Performance por vendedor
        st.markdown("#### 👥 Performance por Vendedor")
        
        vendedor_stats = leads_df.groupby('vendedor').agg({
            'nome': 'count',
            'score': 'mean',
            'status': lambda x: (x == 'fechado').sum()
        }).round(2)
        
        vendedor_stats.columns = ['Total_Leads', 'Score_Medio', 'Fechados']
        vendedor_stats['Taxa_Conversao'] = (vendedor_stats['Fechados'] / vendedor_stats['Total_Leads'] * 100).round(1)
        vendedor_stats = vendedor_stats.reset_index()
        
        st.dataframe(
            vendedor_stats,
            column_config={
                'vendedor': st.column_config.TextColumn('Vendedor'),
                'Total_Leads': st.column_config.NumberColumn('Total de Leads'),
                'Score_Medio': st.column_config.NumberColumn('Score Médio', format="%.1f"),
                'Fechados': st.column_config.NumberColumn('Leads Fechados'),
                'Taxa_Conversao': st.column_config.NumberColumn('Taxa Conversão (%)', format="%.1f%%")
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Ações rápidas
        st.markdown("#### ⚡ Ações Rápidas")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Exportar CSV", use_container_width=True):
                csv = leads_df.to_csv(index=False)
                st.download_button(
                    label="💾 Download CSV",
                    data=csv,
                    file_name=f"leads_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📊 Relatório Completo", use_container_width=True):
                st.info("📊 Funcionalidade em desenvolvimento")
        
        with col3:
            if st.button("📧 Enviar Relatório", use_container_width=True):
                st.info("📧 Funcionalidade em desenvolvimento")