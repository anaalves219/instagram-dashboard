import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.database import Database
from utils.auth import get_current_user

def show_page():
    """Página de Vendas - CRUD completo de vendas e comissões"""
    
    st.title("💰 Gestão de Vendas")
    st.markdown("**Adicione, edite e acompanhe todas as vendas da equipe**")
    
    # Inicializar database
    db = Database()
    user_info = get_current_user()
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs(["➕ Nova Venda", "📋 Histórico", "💵 Comissões", "📊 Relatórios"])
    
    # ========== TAB 1: NOVA VENDA ==========
    with tab1:
        st.markdown("### ➕ Adicionar Nova Venda")
        
        with st.form("nova_venda", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                cliente_nome = st.text_input("👤 Nome do Cliente *", placeholder="Ex: João Silva")
                cliente_instagram = st.text_input("📱 Instagram", placeholder="@joaosilva")
                cliente_email = st.text_input("📧 E-mail", placeholder="joao@email.com")
                produto = st.selectbox("🛍️ Produto *", [
                    "Curso High Ticket",
                    "Mentoria Individual", 
                    "Consultoria Premium",
                    "Workshop Intensivo"
                ])
                valor = st.number_input("💰 Valor da Venda *", min_value=0.0, value=1997.0, step=100.0)
            
            with col2:
                cliente_telefone = st.text_input("📞 Telefone", placeholder="(11) 99999-9999")
                vendedor = st.selectbox("🎯 Vendedor *", ["Ana", "Fernando"], 
                                      index=0 if user_info.get('name') == 'Ana' else 1)
                data_venda = st.date_input("📅 Data da Venda *", value=datetime.now().date())
                meio_pagamento = st.selectbox("💳 Meio de Pagamento", [
                    "PIX", "Cartão à vista", "Cartão parcelado", "Boleto", "Transferência"
                ])
                comissao_pct = st.number_input("📈 Comissão (%)", min_value=0.0, max_value=100.0, value=30.0, step=1.0) / 100
            
            observacoes = st.text_area("📝 Observações", placeholder="Detalhes adicionais sobre a venda...")
            
            # Info sobre auto-criação de lead
            st.info("🎯 **INTELIGÊNCIA AUTOMÁTICA:** Ao adicionar esta venda, um lead será criado automaticamente com status 'fechado' se a pessoa não existir na base de leads!")
            
            submitted = st.form_submit_button("🚀 Adicionar Venda + Lead Automático", type="primary", use_container_width=True)
            
            if submitted:
                if not cliente_nome or not produto or valor <= 0:
                    st.error("❌ Preencha todos os campos obrigatórios!")
                else:
                    venda_data = {
                        'cliente_nome': cliente_nome,
                        'cliente_instagram': cliente_instagram,
                        'cliente_email': cliente_email,
                        'cliente_telefone': cliente_telefone,
                        'produto': produto,
                        'valor': valor,
                        'vendedor': vendedor,
                        'data_venda': data_venda.strftime('%Y-%m-%d'),
                        'status': 'confirmada',
                        'meio_pagamento': meio_pagamento,
                        'comissao_pct': comissao_pct,
                        'observacoes': observacoes,
                        'created_at': datetime.now().isoformat()
                    }
                    
                    if db.add_venda(venda_data):
                        st.success("✅ Venda adicionada com sucesso!")
                        db.log_activity(user_info.get('username', ''), 'Nova Venda', f"Venda de R$ {valor:,.2f} para {cliente_nome}")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Erro ao adicionar venda. Tente novamente.")
    
    # ========== TAB 2: HISTÓRICO ==========
    with tab2:
        st.markdown("### 📋 Histórico de Vendas")
        
        # Filtros
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            filtro_vendedor = st.selectbox("👤 Filtrar por Vendedor", ["Todos", "Ana", "Fernando"])
        
        with col2:
            filtro_status = st.selectbox("📊 Status", ["Todos", "confirmada", "pendente", "cancelada"])
        
        with col3:
            data_inicio = st.date_input("📅 Data Início", value=datetime.now() - timedelta(days=30))
        
        with col4:
            data_fim = st.date_input("📅 Data Fim", value=datetime.now().date())
        
        # Buscar vendas
        vendas_df = db.get_vendas(data_inicio, data_fim)
        
        if not vendas_df.empty:
            # Aplicar filtros
            if filtro_vendedor != "Todos":
                vendas_df = vendas_df[vendas_df['vendedor'] == filtro_vendedor]
            
            if filtro_status != "Todos":
                vendas_df = vendas_df[vendas_df['status'] == filtro_status]
            
            # Estatísticas do período
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🏆 Total de Vendas", len(vendas_df))
            
            with col2:
                total_faturamento = vendas_df['valor'].sum()
                st.metric("💰 Faturamento", f"R$ {total_faturamento:,.2f}")
            
            with col3:
                ticket_medio = vendas_df['valor'].mean()
                st.metric("🎫 Ticket Médio", f"R$ {ticket_medio:,.2f}")
            
            with col4:
                total_comissoes = vendas_df['valor'].sum() * 0.3  # Assumindo 30% de comissão
                st.metric("💵 Comissões", f"R$ {total_comissoes:,.2f}")
            
            # Tabela de vendas
            st.markdown("### 📊 Lista de Vendas")
            
            # Preparar dados para exibição
            vendas_display = vendas_df.copy()
            vendas_display['valor'] = vendas_display['valor'].apply(lambda x: f"R$ {x:,.2f}")
            vendas_display['data_venda'] = pd.to_datetime(vendas_display['data_venda']).dt.strftime('%d/%m/%Y')
            
            # Configurar colunas
            column_config = {
                'cliente_nome': st.column_config.TextColumn('Cliente', width='medium'),
                'produto': st.column_config.TextColumn('Produto', width='medium'),
                'valor': st.column_config.TextColumn('Valor', width='small'),
                'vendedor': st.column_config.TextColumn('Vendedor', width='small'),
                'data_venda': st.column_config.TextColumn('Data', width='small'),
                'status': st.column_config.TextColumn('Status', width='small'),
                'meio_pagamento': st.column_config.TextColumn('Pagamento', width='medium'),
            }
            
            # Exibir tabela editável
            edited_df = st.data_editor(
                vendas_display[['cliente_nome', 'produto', 'valor', 'vendedor', 'data_venda', 'status', 'meio_pagamento']],
                column_config=column_config,
                hide_index=True,
                use_container_width=True,
                height=400
            )
            
            # Opções de ação em massa
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("📥 Exportar CSV", use_container_width=True):
                    csv = vendas_df.to_csv(index=False)
                    st.download_button(
                        label="💾 Download CSV",
                        data=csv,
                        file_name=f"vendas_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
            
            with col2:
                if st.button("📊 Exportar Excel", use_container_width=True):
                    # Implementar export Excel
                    st.success("✅ Funcionalidade em desenvolvimento")
        
        else:
            st.info("📊 Nenhuma venda encontrada no período selecionado")
    
    # ========== TAB 3: COMISSÕES ==========
    with tab3:
        st.markdown("### 💵 Relatório de Comissões")
        
        col1, col2 = st.columns(2)
        
        with col1:
            mes_comissao = st.selectbox("📅 Mês", [
                datetime.now().strftime('%Y-%m'),
                (datetime.now() - timedelta(days=30)).strftime('%Y-%m'),
                (datetime.now() - timedelta(days=60)).strftime('%Y-%m')
            ])
        
        with col2:
            st.markdown("**🎯 Meta de Comissão: R$ 15.000,00**")
        
        # Calcular comissões
        vendas_df = db.get_vendas()
        
        if not vendas_df.empty:
            # Filtrar por mês
            vendas_df['data_venda'] = pd.to_datetime(vendas_df['data_venda'])
            vendas_mes = vendas_df[vendas_df['data_venda'].dt.strftime('%Y-%m') == mes_comissao]
            
            if not vendas_mes.empty:
                comissoes = vendas_mes.groupby('vendedor').agg({
                    'valor': ['sum', 'count'],
                }).round(2)
                
                comissoes.columns = ['Total_Vendas', 'Qtd_Vendas']
                comissoes['Comissao_30pct'] = comissoes['Total_Vendas'] * 0.3
                comissoes = comissoes.reset_index()
                
                # Cards de comissão
                for _, row in comissoes.iterrows():
                    with st.container():
                        if row['vendedor'] == 'Ana':
                            st.markdown(f"""
                            <div class="vendedor-ana">
                                <h3>👤 {row['vendedor']}</h3>
                                <div style="display: flex; justify-content: space-between;">
                                    <div>
                                        <p><strong>Vendas:</strong> {row['Qtd_Vendas']:.0f}</p>
                                        <p><strong>Faturamento:</strong> R$ {row['Total_Vendas']:,.2f}</p>
                                    </div>
                                    <div style="text-align: right;">
                                        <p style="font-size: 1.5rem;"><strong>R$ {row['Comissao_30pct']:,.2f}</strong></p>
                                        <p>Comissão (30%)</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="vendedor-fernando">
                                <h3>👤 {row['vendedor']}</h3>
                                <div style="display: flex; justify-content: space-between;">
                                    <div>
                                        <p><strong>Vendas:</strong> {row['Qtd_Vendas']:.0f}</p>
                                        <p><strong>Faturamento:</strong> R$ {row['Total_Vendas']:,.2f}</p>
                                    </div>
                                    <div style="text-align: right;">
                                        <p style="font-size: 1.5rem;"><strong>R$ {row['Comissao_30pct']:,.2f}</strong></p>
                                        <p>Comissão (30%)</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
            else:
                st.info("💵 Nenhuma venda registrada no mês selecionado")
        else:
            st.info("💵 Nenhum dado de venda disponível")
    
    # ========== TAB 4: RELATÓRIOS ==========
    with tab4:
        st.markdown("### 📊 Relatórios e Análises")
        
        vendas_df = db.get_vendas()
        
        if not vendas_df.empty:
            vendas_df['data_venda'] = pd.to_datetime(vendas_df['data_venda'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Gráfico de vendas por mês
                st.markdown("#### 📈 Vendas por Mês")
                vendas_mensais = vendas_df.groupby([
                    vendas_df['data_venda'].dt.to_period('M'),
                    'vendedor'
                ])['valor'].sum().reset_index()
                vendas_mensais['data_venda'] = vendas_mensais['data_venda'].astype(str)
                
                fig = px.bar(
                    vendas_mensais,
                    x='data_venda',
                    y='valor',
                    color='vendedor',
                    title="Faturamento Mensal por Vendedor",
                    color_discrete_map={'Ana': '#9D4EDD', 'Fernando': '#0EA5E9'}
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Gráfico de conversão por produto
                st.markdown("#### 🛍️ Vendas por Produto")
                vendas_produto = vendas_df['produto'].value_counts().reset_index()
                vendas_produto.columns = ['Produto', 'Quantidade']
                
                fig = px.pie(
                    vendas_produto,
                    values='Quantidade',
                    names='Produto',
                    title="Distribuição de Vendas por Produto"
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Análise de performance
            st.markdown("#### 🎯 Análise de Performance")
            
            performance = vendas_df.groupby('vendedor').agg({
                'valor': ['sum', 'mean', 'count'],
                'data_venda': lambda x: (datetime.now().date() - x.max().date()).days
            }).round(2)
            
            performance.columns = ['Total', 'Ticket_Medio', 'Qtd_Vendas', 'Dias_Ultima_Venda']
            performance = performance.reset_index()
            
            st.dataframe(
                performance,
                column_config={
                    'vendedor': st.column_config.TextColumn('Vendedor'),
                    'Total': st.column_config.NumberColumn('Total (R$)', format="R$ %.2f"),
                    'Ticket_Medio': st.column_config.NumberColumn('Ticket Médio (R$)', format="R$ %.2f"),
                    'Qtd_Vendas': st.column_config.NumberColumn('Quantidade'),
                    'Dias_Ultima_Venda': st.column_config.NumberColumn('Dias desde última venda')
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("📊 Nenhum dado disponível para relatórios")