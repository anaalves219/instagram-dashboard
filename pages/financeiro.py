import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from utils.database import Database

def show_page():
    """Página Financeiro - ROI, custos e projeções"""
    
    st.title("💳 Análise Financeira")
    st.markdown("**Custos, ROI, projeções e saúde financeira do negócio**")
    
    # Inicializar database
    db = Database()
    
    # Tabs principais
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["💰 ROI", "📊 Custos", "📈 Projeções", "💸 Fluxo de Caixa", "📋 Relatórios"])
    
    # ========== TAB 1: ROI ==========
    with tab1:
        st.markdown("### 💰 Retorno sobre Investimento (ROI)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            periodo_roi = st.selectbox("📅 Período para ROI", [
                "Este Mês", "Últimos 30 dias", "Último Trimestre", "Este Ano"
            ])
        
        with col2:
            incluir_custos = st.multiselect("💸 Incluir Custos", [
                "Anúncios", "Ferramentas", "Salários", "Operacional", "Todos"
            ], default=["Todos"])
        
        # Calcular período
        hoje = datetime.now().date()
        if periodo_roi == "Este Mês":
            data_inicio = hoje.replace(day=1)
        elif periodo_roi == "Últimos 30 dias":
            data_inicio = hoje - timedelta(days=30)
        elif periodo_roi == "Último Trimestre":
            data_inicio = hoje - timedelta(days=90)
        else:  # Este Ano
            data_inicio = hoje.replace(month=1, day=1)
        
        # Buscar dados
        vendas_df = db.get_vendas(data_inicio, hoje)
        
        # Calcular receitas
        vendas_confirmadas = vendas_df[vendas_df['status'] == 'confirmada'] if not vendas_df.empty else pd.DataFrame()
        receita_total = vendas_confirmadas['valor'].sum() if not vendas_confirmadas.empty else 0
        
        # Simular custos (em produção, viria do banco)
        custos_simulados = {
            "Anúncios": 8500.00,
            "Ferramentas": 1200.00,
            "Salários": 15000.00,
            "Operacional": 3500.00
        }
        
        if "Todos" in incluir_custos:
            custo_total = sum(custos_simulados.values())
        else:
            custo_total = sum(custos_simulados[custo] for custo in incluir_custos if custo in custos_simulados)
        
        # Calcular ROI
        lucro_liquido = receita_total - custo_total
        roi_pct = (lucro_liquido / custo_total * 100) if custo_total > 0 else 0
        margem_lucro = (lucro_liquido / receita_total * 100) if receita_total > 0 else 0
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💰 Receita Total",
                f"R$ {receita_total:,.2f}",
                delta=f"+{receita_total * 0.15:.0f} vs período anterior"
            )
        
        with col2:
            st.metric(
                "💸 Custo Total",
                f"R$ {custo_total:,.2f}",
                delta=f"-{custo_total * 0.05:.0f} vs período anterior",
                delta_color="inverse"
            )
        
        with col3:
            st.metric(
                "📈 ROI",
                f"{roi_pct:.1f}%",
                delta=f"+{abs(roi_pct) * 0.1:.1f}% vs período anterior"
            )
        
        with col4:
            st.metric(
                "💎 Margem de Lucro",
                f"{margem_lucro:.1f}%",
                delta=f"+{abs(margem_lucro) * 0.08:.1f}% vs período anterior"
            )
        
        # Gráfico de ROI
        st.markdown("#### 📊 Evolução do ROI")
        
        # Simular dados históricos de ROI
        datas_roi = pd.date_range(start=data_inicio, end=hoje, freq='D')
        roi_historico = []
        
        for i, data in enumerate(datas_roi):
            # Simular ROI com tendência crescente
            roi_dia = 150 + (i * 2) + np.random.normal(0, 20)
            roi_historico.append({
                'Data': data,
                'ROI': max(roi_dia, 50),  # ROI mínimo de 50%
                'Receita': receita_total * (i + 1) / len(datas_roi),
                'Custo': custo_total * (i + 1) / len(datas_roi)
            })
        
        df_roi = pd.DataFrame(roi_historico)
        
        fig = px.line(
            df_roi,
            x='Data',
            y='ROI',
            title="Evolução do ROI (%)",
            color_discrete_sequence=['#06FFA5']
        )
        
        # Adicionar linha de meta de ROI
        fig.add_hline(
            y=200,
            line_dash="dash",
            line_color="gold",
            annotation_text="Meta ROI 200%"
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Breakdown de custos
        st.markdown("#### 💸 Breakdown de Custos")
        
        custos_df = pd.DataFrame(list(custos_simulados.items()), columns=['Categoria', 'Valor'])
        custos_df['Percentual'] = (custos_df['Valor'] / custos_df['Valor'].sum() * 100).round(1)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                custos_df,
                values='Valor',
                names='Categoria',
                title="Distribuição de Custos",
                color_discrete_sequence=['#9D4EDD', '#06FFA5', '#0EA5E9', '#F97316']
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.dataframe(
                custos_df,
                column_config={
                    'Categoria': st.column_config.TextColumn('Categoria'),
                    'Valor': st.column_config.NumberColumn('Valor (R$)', format="R$ %.2f"),
                    'Percentual': st.column_config.NumberColumn('% do Total', format="%.1f%%")
                },
                hide_index=True,
                use_container_width=True
            )
    
    # ========== TAB 2: CUSTOS ==========
    with tab2:
        st.markdown("### 📊 Gestão de Custos")
        
        # Adicionar novo custo
        with st.expander("➕ Adicionar Novo Custo", expanded=False):
            with st.form("novo_custo"):
                col1, col2 = st.columns(2)
                
                with col1:
                    descricao = st.text_input("📝 Descrição", placeholder="Ex: Facebook Ads Janeiro")
                    categoria = st.selectbox("🏷️ Categoria", [
                        "Anúncios", "Ferramentas", "Salários", "Operacional", "Treinamento", "Outros"
                    ])
                    valor = st.number_input("💰 Valor", min_value=0.0, step=10.0)
                
                with col2:
                    data_custo = st.date_input("📅 Data", value=datetime.now().date())
                    responsavel = st.selectbox("👤 Responsável", ["Ana", "Fernando", "Empresa"])
                    recorrente = st.checkbox("🔄 Custo Recorrente")
                
                if st.form_submit_button("💾 Salvar Custo", type="primary"):
                    st.success("✅ Custo adicionado com sucesso!")
        
        # Lista de custos
        st.markdown("#### 📋 Custos do Mês")
        
        # Simular dados de custos
        custos_detalhados = [
            {"Data": "2024-02-01", "Descrição": "Facebook Ads", "Categoria": "Anúncios", "Valor": 3500.00, "Responsável": "Ana"},
            {"Data": "2024-02-01", "Descrição": "Google Ads", "Categoria": "Anúncios", "Valor": 5000.00, "Responsável": "Fernando"},
            {"Data": "2024-02-05", "Descrição": "Streamlit Pro", "Categoria": "Ferramentas", "Valor": 200.00, "Responsável": "Empresa"},
            {"Data": "2024-02-05", "Descrição": "Supabase Pro", "Categoria": "Ferramentas", "Valor": 100.00, "Responsável": "Empresa"},
            {"Data": "2024-02-01", "Descrição": "Salário Ana", "Categoria": "Salários", "Valor": 7500.00, "Responsável": "Empresa"},
            {"Data": "2024-02-01", "Descrição": "Salário Fernando", "Categoria": "Salários", "Valor": 7500.00, "Responsável": "Empresa"},
            {"Data": "2024-02-10", "Descrição": "Hospedagem", "Categoria": "Operacional", "Valor": 300.00, "Responsável": "Empresa"},
            {"Data": "2024-02-15", "Descrição": "Material de Marketing", "Categoria": "Operacional", "Valor": 800.00, "Responsável": "Ana"},
        ]
        
        custos_df = pd.DataFrame(custos_detalhados)
        custos_df['Data'] = pd.to_datetime(custos_df['Data']).dt.strftime('%d/%m/%Y')
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filtro_categoria = st.selectbox("🏷️ Filtrar Categoria", 
                                          ["Todas"] + custos_df['Categoria'].unique().tolist())
        
        with col2:
            filtro_responsavel = st.selectbox("👤 Filtrar Responsável",
                                           ["Todos"] + custos_df['Responsável'].unique().tolist())
        
        with col3:
            ordenar_por = st.selectbox("🔄 Ordenar por", ["Data", "Valor", "Categoria"])
        
        # Aplicar filtros
        custos_filtrados = custos_df.copy()
        
        if filtro_categoria != "Todas":
            custos_filtrados = custos_filtrados[custos_filtrados['Categoria'] == filtro_categoria]
        
        if filtro_responsavel != "Todos":
            custos_filtrados = custos_filtrados[custos_filtrados['Responsável'] == filtro_responsavel]
        
        # Exibir tabela
        st.dataframe(
            custos_filtrados,
            column_config={
                'Data': st.column_config.TextColumn('Data'),
                'Descrição': st.column_config.TextColumn('Descrição'),
                'Categoria': st.column_config.TextColumn('Categoria'),
                'Valor': st.column_config.NumberColumn('Valor (R$)', format="R$ %.2f"),
                'Responsável': st.column_config.TextColumn('Responsável')
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Resumo de custos
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_custos = custos_filtrados['Valor'].sum()
            st.metric("💸 Total Filtrado", f"R$ {total_custos:,.2f}")
        
        with col2:
            media_custos = custos_filtrados['Valor'].mean()
            st.metric("📊 Custo Médio", f"R$ {media_custos:,.2f}")
        
        with col3:
            maior_custo = custos_filtrados['Valor'].max()
            st.metric("📈 Maior Custo", f"R$ {maior_custo:,.2f}")
    
    # ========== TAB 3: PROJEÇÕES ==========
    with tab3:
        st.markdown("### 📈 Projeções Financeiras")
        
        col1, col2 = st.columns(2)
        
        with col1:
            periodo_projecao = st.selectbox("📅 Período de Projeção", [
                "Próximos 30 dias", "Próximos 3 meses", "Próximos 6 meses", "Próximo ano"
            ])
        
        with col2:
            cenario = st.selectbox("🎯 Cenário", [
                "Conservador", "Realista", "Otimista"
            ])
        
        # Buscar dados históricos
        vendas_df = db.get_vendas()
        
        if not vendas_df.empty:
            vendas_confirmadas = vendas_df[vendas_df['status'] == 'confirmada']
            
            # Calcular médias históricas
            receita_media_dia = vendas_confirmadas['valor'].sum() / 30  # Assumindo 30 dias de dados
            crescimento_base = {
                "Conservador": 0.05,  # 5% ao mês
                "Realista": 0.15,     # 15% ao mês  
                "Otimista": 0.25      # 25% ao mês
            }
            
            crescimento = crescimento_base[cenario]
            
            # Calcular projeção
            if periodo_projecao == "Próximos 30 dias":
                dias = 30
            elif periodo_projecao == "Próximos 3 meses":
                dias = 90
            elif periodo_projecao == "Próximos 6 meses":
                dias = 180
            else:  # Próximo ano
                dias = 365
            
            # Gerar projeção
            datas_projecao = pd.date_range(start=datetime.now().date(), periods=dias, freq='D')
            projecao = []
            
            for i, data in enumerate(datas_projecao):
                # Simular crescimento progressivo
                fator_crescimento = (1 + crescimento) ** (i / 30)  # Crescimento mensal
                receita_dia = receita_media_dia * fator_crescimento * (0.8 + 0.4 * np.random.random())
                
                projecao.append({
                    'Data': data,
                    'Receita_Projetada': receita_dia,
                    'Receita_Acumulada': sum([p['Receita_Projetada'] for p in projecao]) + receita_dia,
                    'Cenario': cenario
                })
            
            df_projecao = pd.DataFrame(projecao)
            
            # Métricas da projeção
            receita_projetada_total = df_projecao['Receita_Projetada'].sum()
            receita_projetada_mensal = receita_projetada_total / (dias / 30)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    f"💰 Receita Projetada ({periodo_projecao})",
                    f"R$ {receita_projetada_total:,.2f}"
                )
            
            with col2:
                st.metric(
                    "📊 Receita Mensal Média",
                    f"R$ {receita_projetada_mensal:,.2f}"
                )
            
            with col3:
                lucro_projetado = receita_projetada_total * 0.6  # Assumindo 60% de margem
                st.metric(
                    "💎 Lucro Projetado",
                    f"R$ {lucro_projetado:,.2f}"
                )
            
            # Gráfico de projeção
            fig = px.line(
                df_projecao,
                x='Data',
                y='Receita_Acumulada',
                title=f"Projeção de Receita - Cenário {cenario}",
                color_discrete_sequence=['#06FFA5']
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Comparação de cenários
            st.markdown("#### 🎯 Comparação de Cenários")
            
            cenarios_comparacao = []
            for cent in ["Conservador", "Realista", "Otimista"]:
                cresc = crescimento_base[cent]
                receita_total = receita_media_dia * dias * (1 + cresc)
                
                cenarios_comparacao.append({
                    'Cenário': cent,
                    'Crescimento Mensal': f"{cresc*100:.0f}%",
                    'Receita Projetada': f"R$ {receita_total:,.2f}",
                    'Lucro Estimado': f"R$ {receita_total * 0.6:,.2f}"
                })
            
            st.dataframe(
                pd.DataFrame(cenarios_comparacao),
                hide_index=True,
                use_container_width=True
            )
        
        else:
            st.info("📈 Aguardando dados históricos para gerar projeções")
    
    # ========== TAB 4: FLUXO DE CAIXA ==========
    with tab4:
        st.markdown("### 💸 Fluxo de Caixa")
        
        # Simular dados de fluxo de caixa
        hoje = datetime.now().date()
        datas_fluxo = pd.date_range(start=hoje - timedelta(days=30), end=hoje + timedelta(days=30), freq='D')
        
        fluxo_caixa = []
        saldo_acumulado = 50000  # Saldo inicial
        
        for data in datas_fluxo:
            if data.date() <= hoje:
                # Dados históricos
                entrada = np.random.normal(2000, 500) if np.random.random() > 0.3 else 0
                saida = np.random.normal(800, 200)
            else:
                # Projeção futura
                entrada = np.random.normal(2500, 600) if np.random.random() > 0.2 else 0
                saida = np.random.normal(900, 250)
            
            saldo_dia = entrada - saida
            saldo_acumulado += saldo_dia
            
            fluxo_caixa.append({
                'Data': data,
                'Entradas': max(entrada, 0),
                'Saidas': max(saida, 0),
                'Saldo_Dia': saldo_dia,
                'Saldo_Acumulado': saldo_acumulado,
                'Tipo': 'Histórico' if data.date() <= hoje else 'Projeção'
            })
        
        df_fluxo = pd.DataFrame(fluxo_caixa)
        
        # Métricas do fluxo
        col1, col2, col3, col4 = st.columns(4)
        
        saldo_atual = df_fluxo[df_fluxo['Tipo'] == 'Histórico']['Saldo_Acumulado'].iloc[-1]
        entradas_mes = df_fluxo[df_fluxo['Tipo'] == 'Histórico']['Entradas'].sum()
        saidas_mes = df_fluxo[df_fluxo['Tipo'] == 'Histórico']['Saidas'].sum()
        saldo_projetado = df_fluxo['Saldo_Acumulado'].iloc[-1]
        
        with col1:
            st.metric("💰 Saldo Atual", f"R$ {saldo_atual:,.2f}")
        
        with col2:
            st.metric("📈 Entradas (30d)", f"R$ {entradas_mes:,.2f}")
        
        with col3:
            st.metric("📉 Saídas (30d)", f"R$ {saidas_mes:,.2f}")
        
        with col4:
            st.metric("🔮 Saldo Projetado", f"R$ {saldo_projetado:,.2f}")
        
        # Gráfico de fluxo de caixa
        fig = go.Figure()
        
        # Histórico
        historico = df_fluxo[df_fluxo['Tipo'] == 'Histórico']
        fig.add_trace(go.Scatter(
            x=historico['Data'],
            y=historico['Saldo_Acumulado'],
            mode='lines',
            name='Histórico',
            line=dict(color='#06FFA5', width=3)
        ))
        
        # Projeção
        projecao = df_fluxo[df_fluxo['Tipo'] == 'Projeção']
        fig.add_trace(go.Scatter(
            x=projecao['Data'],
            y=projecao['Saldo_Acumulado'],
            mode='lines',
            name='Projeção',
            line=dict(color='#9D4EDD', width=2, dash='dash')
        ))
        
        # Linha de alerta
        fig.add_hline(
            y=10000,
            line_dash="dot",
            line_color="red",
            annotation_text="Limite Mínimo R$ 10.000"
        )
        
        fig.update_layout(
            title='Evolução do Saldo - Histórico vs Projeção',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis_title='Data',
            yaxis_title='Saldo (R$)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Alertas de fluxo de caixa
        st.markdown("#### 🚨 Alertas Financeiros")
        
        if saldo_atual < 20000:
            st.error("🔴 **Atenção:** Saldo abaixo do limite recomendado!")
        elif saldo_atual < 50000:
            st.warning("🟡 **Cuidado:** Saldo próximo do limite mínimo.")
        else:
            st.success("🟢 **Situação financeira saudável.**")
        
        # Próximos vencimentos (simulado)
        st.markdown("#### 📅 Próximos Vencimentos")
        
        vencimentos = [
            {"Data": "05/03/2024", "Descrição": "Pagamento Google Ads", "Valor": "R$ 5.000,00"},
            {"Data": "10/03/2024", "Descrição": "Salários", "Valor": "R$ 15.000,00"},
            {"Data": "15/03/2024", "Descrição": "Aluguel", "Valor": "R$ 3.500,00"},
            {"Data": "20/03/2024", "Descrição": "Ferramentas SaaS", "Valor": "R$ 800,00"},
        ]
        
        for venc in vencimentos:
            st.markdown(f"📅 **{venc['Data']}** - {venc['Descrição']}: {venc['Valor']}")
    
    # ========== TAB 5: RELATÓRIOS ==========
    with tab5:
        st.markdown("### 📋 Relatórios Financeiros")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tipo_relatorio = st.selectbox("📊 Tipo de Relatório", [
                "DRE Mensal", "Análise de Margem", "Comparativo Anual", "ROI por Canal"
            ])
        
        with col2:
            formato_export = st.selectbox("📄 Formato de Export", [
                "PDF", "Excel", "CSV"
            ])
        
        if tipo_relatorio == "DRE Mensal":
            st.markdown("#### 📊 Demonstrativo de Resultado (DRE)")
            
            # Simular DRE
            dre_data = {
                'Item': [
                    'Receita Bruta',
                    '(-) Impostos',
                    '= Receita Líquida',
                    '(-) Custos Variáveis',
                    '= Margem de Contribuição',
                    '(-) Custos Fixos',
                    '= Resultado Operacional',
                    '(-) Custos Financeiros',
                    '= Resultado Líquido'
                ],
                'Valor': [
                    89750.00,
                    -8975.00,
                    80775.00,
                    -26925.00,
                    53850.00,
                    -28200.00,
                    25650.00,
                    -1200.00,
                    24450.00
                ],
                'Percentual': [
                    100.0,
                    -10.0,
                    90.0,
                    -30.0,
                    60.0,
                    -31.4,
                    28.6,
                    -1.3,
                    27.2
                ]
            }
            
            dre_df = pd.DataFrame(dre_data)
            
            st.dataframe(
                dre_df,
                column_config={
                    'Item': st.column_config.TextColumn('Item'),
                    'Valor': st.column_config.NumberColumn('Valor (R$)', format="R$ %.2f"),
                    'Percentual': st.column_config.NumberColumn('% da Receita', format="%.1f%%")
                },
                hide_index=True,
                use_container_width=True
            )
        
        elif tipo_relatorio == "Análise de Margem":
            st.markdown("#### 💎 Análise de Margem por Produto")
            
            margem_data = {
                'Produto': ['Curso High Ticket', 'Mentoria Individual', 'Consultoria Premium'],
                'Receita': [65000.00, 15000.00, 9750.00],
                'Custo': [19500.00, 6000.00, 3900.00],
                'Margem_R': [45500.00, 9000.00, 5850.00],
                'Margem_Pct': [70.0, 60.0, 60.0]
            }
            
            margem_df = pd.DataFrame(margem_data)
            
            fig = px.bar(
                margem_df,
                x='Produto',
                y=['Receita', 'Custo'],
                title="Receita vs Custo por Produto",
                color_discrete_map={'Receita': '#06FFA5', 'Custo': '#EF4444'}
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(
                margem_df,
                column_config={
                    'Produto': st.column_config.TextColumn('Produto'),
                    'Receita': st.column_config.NumberColumn('Receita (R$)', format="R$ %.2f"),
                    'Custo': st.column_config.NumberColumn('Custo (R$)', format="R$ %.2f"),
                    'Margem_R': st.column_config.NumberColumn('Margem (R$)', format="R$ %.2f"),
                    'Margem_Pct': st.column_config.NumberColumn('Margem (%)', format="%.1f%%")
                },
                hide_index=True,
                use_container_width=True
            )
        
        # Botões de export
        st.markdown("#### 💾 Exportar Relatório")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Gerar PDF", use_container_width=True):
                st.success("✅ PDF gerado com sucesso!")
                st.download_button(
                    label="💾 Download PDF",
                    data=b"PDF content here",
                    file_name=f"relatorio_financeiro_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
        
        with col2:
            if st.button("📊 Gerar Excel", use_container_width=True):
                st.success("✅ Excel gerado com sucesso!")
        
        with col3:
            if st.button("📈 Enviar por E-mail", use_container_width=True):
                st.info("📧 Funcionalidade em desenvolvimento")