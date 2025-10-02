import streamlit as st
import pandas as pd
from datetime import datetime, date
from utils.database import Database
from utils.auth import get_current_user

def show_page():
    """Página de Leads - Sistema de pipeline de vendas"""
    
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
    tab1, tab2, tab3 = st.tabs(["➕ Novo Lead", "📋 Pipeline", "📊 Relatórios"])
    
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
        col1, col2, col3, col4 = st.columns(4)
        
        total_leads = len(leads_df)
        leads_novos = len(leads_df[leads_df['status'] == 'novo'])
        leads_fechados = len(leads_df[leads_df['status'] == 'fechado'])
        taxa_conversao = (leads_fechados / total_leads * 100) if total_leads > 0 else 0
        
        with col1:
            st.metric("Total de Leads", total_leads)
        
        with col2:
            st.metric("Leads Novos", leads_novos)
        
        with col3:
            st.metric("Leads Fechados", leads_fechados)
        
        with col4:
            st.metric("Taxa de Conversão", f"{taxa_conversao:.1f}%")
        
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
        
        # Tabela de leads
        st.markdown("#### 📊 Lista de Leads")
        
        if not leads_filtrados.empty:
            # Preparar dados para exibição
            display_df = leads_filtrados.copy()
            
            # Formatar colunas para exibição
            colunas_exibir = ['nome', 'telefone', 'vendedor', 'status', 'score', 'origem']
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
                height=400
            )
            
            st.info(f"📊 Exibindo {len(leads_filtrados)} de {len(leads_df)} leads")
        else:
            st.warning("🔍 Nenhum lead encontrado com os filtros selecionados")
    
    # ========== TAB 3: RELATÓRIOS ==========
    with tab3:
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