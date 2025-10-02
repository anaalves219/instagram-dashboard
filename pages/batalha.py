import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.database import Database
from utils.styles import create_vendedor_card

def show_page():
    """Página Batalha - Comparativo entre vendedores"""
    
    st.title("⚔️ Batalha dos Vendedores")
    st.markdown("**Competição saudável entre Ana e Fernando - Que vença o melhor!**")
    
    # Inicializar database
    db = Database()
    
    # Período de análise
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        periodo = st.selectbox("📅 Período", [
            "Hoje", "Esta Semana", "Este Mês", "Últimos 30 dias", "Último Trimestre"
        ])
    
    with col2:
        metrica_principal = st.selectbox("🎯 Métrica Principal", [
            "Faturamento", "Quantidade de Vendas", "Ticket Médio", "Leads Convertidos", "Score Médio"
        ])
    
    with col3:
        st.markdown("### 🏆 Placar Geral do Mês")
        st.markdown("**Ana 👤 2 x 3 👤 Fernando**")
    
    # Calcular período
    hoje = datetime.now().date()
    if periodo == "Hoje":
        data_inicio = hoje
        data_fim = hoje
    elif periodo == "Esta Semana":
        data_inicio = hoje - timedelta(days=hoje.weekday())
        data_fim = hoje
    elif periodo == "Este Mês":
        data_inicio = hoje.replace(day=1)
        data_fim = hoje
    elif periodo == "Últimos 30 dias":
        data_inicio = hoje - timedelta(days=30)
        data_fim = hoje
    else:  # Último Trimestre
        data_inicio = hoje - timedelta(days=90)
        data_fim = hoje
    
    # Buscar dados
    vendas_df = db.get_vendas(data_inicio, data_fim)
    leads_df = db.get_leads()
    
    # Filtrar vendas confirmadas
    vendas_confirmadas = vendas_df[vendas_df['status'] == 'confirmada'] if not vendas_df.empty else pd.DataFrame()
    
    # ========== PLACAR PRINCIPAL ==========
    st.markdown("### 🥊 Arena de Batalha")
    
    if not vendas_confirmadas.empty:
        # Calcular métricas por vendedor
        metricas_ana = calcular_metricas_vendedor(vendas_confirmadas, leads_df, "Ana")
        metricas_fernando = calcular_metricas_vendedor(vendas_confirmadas, leads_df, "Fernando")
        
        # Determinar vencedor
        if metrica_principal == "Faturamento":
            vencedor = "Ana" if metricas_ana['faturamento'] > metricas_fernando['faturamento'] else "Fernando"
            valor_ana = metricas_ana['faturamento']
            valor_fernando = metricas_fernando['faturamento']
        elif metrica_principal == "Quantidade de Vendas":
            vencedor = "Ana" if metricas_ana['vendas'] > metricas_fernando['vendas'] else "Fernando"
            valor_ana = metricas_ana['vendas']
            valor_fernando = metricas_fernando['vendas']
        elif metrica_principal == "Ticket Médio":
            vencedor = "Ana" if metricas_ana['ticket_medio'] > metricas_fernando['ticket_medio'] else "Fernando"
            valor_ana = metricas_ana['ticket_medio']
            valor_fernando = metricas_fernando['ticket_medio']
        
        # Display do vencedor
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if vencedor == "Ana":
                st.markdown("""
                <div style="text-align: center; padding: 2rem; background: linear-gradient(45deg, #9D4EDD, #06FFA5); border-radius: 20px; margin: 1rem 0;">
                    <h1 style="margin: 0; color: white;">🏆 ANA VENCEU! 🏆</h1>
                    <p style="margin: 0.5rem 0 0 0; color: white; font-size: 1.2rem;">Parabéns pela liderança!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="text-align: center; padding: 2rem; background: linear-gradient(45deg, #0EA5E9, #F97316); border-radius: 20px; margin: 1rem 0;">
                    <h1 style="margin: 0; color: white;">🏆 FERNANDO VENCEU! 🏆</h1>
                    <p style="margin: 0.5rem 0 0 0; color: white; font-size: 1.2rem;">Parabéns pela liderança!</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Cards de performance detalhada
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(create_vendedor_card_detalhado("Ana", metricas_ana, vencedor == "Ana"), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_vendedor_card_detalhado("Fernando", metricas_fernando, vencedor == "Fernando"), unsafe_allow_html=True)
    
    else:
        st.info("⚔️ Aguardando dados para iniciar a batalha!")
    
    # ========== GRÁFICOS COMPARATIVOS ==========
    st.markdown("### 📊 Comparativo Detalhado")
    
    if not vendas_confirmadas.empty:
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Vendas Diárias", "💰 Faturamento", "🎯 Leads", "🏆 Rankings"])
        
        with tab1:
            # Vendas por dia
            vendas_diarias = vendas_confirmadas.groupby(['data_venda', 'vendedor']).size().reset_index()
            vendas_diarias.columns = ['Data', 'Vendedor', 'Vendas']
            
            fig = px.line(
                vendas_diarias,
                x='Data',
                y='Vendas',
                color='Vendedor',
                title="Vendas Diárias - Ana vs Fernando",
                color_discrete_map={'Ana': '#9D4EDD', 'Fernando': '#0EA5E9'},
                markers=True
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela de performance diária
            performance_diaria = vendas_confirmadas.groupby(['data_venda', 'vendedor']).agg({
                'valor': ['sum', 'count']
            }).round(2)
            performance_diaria.columns = ['Faturamento', 'Vendas']
            performance_diaria = performance_diaria.reset_index()
            
            st.dataframe(
                performance_diaria,
                column_config={
                    'data_venda': st.column_config.DateColumn('Data'),
                    'vendedor': st.column_config.TextColumn('Vendedor'),
                    'Faturamento': st.column_config.NumberColumn('Faturamento (R$)', format="R$ %.2f"),
                    'Vendas': st.column_config.NumberColumn('Vendas')
                },
                hide_index=True,
                use_container_width=True
            )
        
        with tab2:
            # Faturamento acumulado
            vendas_confirmadas['data_venda'] = pd.to_datetime(vendas_confirmadas['data_venda'])
            vendas_ordenadas = vendas_confirmadas.sort_values('data_venda')
            
            faturamento_acumulado = vendas_ordenadas.groupby('vendedor')['valor'].cumsum().reset_index()
            faturamento_acumulado['data_venda'] = vendas_ordenadas['data_venda'].values
            
            fig = px.line(
                faturamento_acumulado,
                x='data_venda',
                y='valor',
                color='vendedor',
                title="Faturamento Acumulado - Corrida pela Meta",
                color_discrete_map={'Ana': '#9D4EDD', 'Fernando': '#0EA5E9'}
            )
            
            # Adicionar linha da meta
            meta_mensal = 50000
            fig.add_hline(
                y=meta_mensal,
                line_dash="dash",
                line_color="gold",
                annotation_text="Meta R$ 50.000"
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Análise de leads
            if not leads_df.empty:
                leads_por_vendedor = leads_df.groupby('vendedor').agg({
                    'id': 'count',
                    'score': 'mean',
                    'status': lambda x: (x == 'fechado').sum()
                }).round(2)
                leads_por_vendedor.columns = ['Total_Leads', 'Score_Medio', 'Convertidos']
                leads_por_vendedor['Taxa_Conversao'] = (leads_por_vendedor['Convertidos'] / leads_por_vendedor['Total_Leads'] * 100).round(1)
                leads_por_vendedor = leads_por_vendedor.reset_index()
                
                # Gráfico de performance de leads
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    name='Total de Leads',
                    x=leads_por_vendedor['vendedor'],
                    y=leads_por_vendedor['Total_Leads'],
                    marker_color=['#9D4EDD', '#0EA5E9']
                ))
                
                fig.add_trace(go.Scatter(
                    name='Taxa de Conversão (%)',
                    x=leads_por_vendedor['vendedor'],
                    y=leads_por_vendedor['Taxa_Conversao'],
                    mode='markers+text',
                    marker=dict(size=15, color='gold'),
                    text=leads_por_vendedor['Taxa_Conversao'].astype(str) + '%',
                    textposition='top center',
                    yaxis='y2'
                ))
                
                fig.update_layout(
                    title='Performance de Leads',
                    yaxis=dict(title='Quantidade de Leads'),
                    yaxis2=dict(title='Taxa de Conversão (%)', overlaying='y', side='right'),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Tabela de leads
                st.dataframe(
                    leads_por_vendedor,
                    column_config={
                        'vendedor': st.column_config.TextColumn('Vendedor'),
                        'Total_Leads': st.column_config.NumberColumn('Total de Leads'),
                        'Score_Medio': st.column_config.NumberColumn('Score Médio', format="%.1f"),
                        'Convertidos': st.column_config.NumberColumn('Convertidos'),
                        'Taxa_Conversao': st.column_config.NumberColumn('Taxa de Conversão (%)', format="%.1f%%")
                    },
                    hide_index=True,
                    use_container_width=True
                )
            else:
                st.info("🎯 Nenhum dado de leads disponível")
        
        with tab4:
            # Rankings históricos
            st.markdown("#### 🏆 Hall da Fama")
            
            rankings = [
                {"Período": "Janeiro 2024", "Vencedor": "Fernando", "Métrica": "R$ 67.890", "Diferença": "+R$ 12.340"},
                {"Período": "Dezembro 2023", "Vencedor": "Ana", "Métrica": "R$ 71.250", "Diferença": "+R$ 8.900"},
                {"Período": "Novembro 2023", "Vencedor": "Ana", "Métrica": "R$ 63.120", "Diferença": "+R$ 5.670"},
                {"Período": "Outubro 2023", "Vencedor": "Fernando", "Métrica": "R$ 59.800", "Diferença": "+R$ 3.450"},
            ]
            
            for i, ranking in enumerate(rankings):
                emoji = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🏅"
                cor = "#FFD700" if ranking["Vencedor"] == "Ana" else "#C0C0C0"
                
                st.markdown(f"""
                <div style="background: linear-gradient(45deg, {'#9D4EDD' if ranking['Vencedor'] == 'Ana' else '#0EA5E9'}, rgba(255,255,255,0.1)); 
                            border-radius: 10px; padding: 1rem; margin: 0.5rem 0; border-left: 5px solid {cor};">
                    <strong>{emoji} {ranking['Período']}</strong><br>
                    🏆 Vencedor: <strong>{ranking['Vencedor']}</strong><br>
                    💰 Faturamento: <strong>{ranking['Métrica']}</strong><br>
                    📈 Diferença: <strong>{ranking['Diferença']}</strong>
                </div>
                """, unsafe_allow_html=True)
            
            # Estatísticas gerais
            st.markdown("#### 📊 Estatísticas Gerais")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("🏆 Vitórias Ana", "8", "+2 vs ano passado")
            
            with col2:
                st.metric("🏆 Vitórias Fernando", "7", "+3 vs ano passado")
            
            with col3:
                st.metric("🤝 Empates", "1", "Dezembro 2023")
    
    # ========== DESAFIOS E METAS ==========
    st.markdown("### 🎯 Desafios e Metas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔥 Desafio da Semana")
        st.info("**Meta:** Primeiro a atingir 10 vendas ganha R$ 500 de bônus!")
        
        progresso_ana = 7  # Simular progresso
        progresso_fernando = 6
        
        st.markdown(f"**Ana:** {progresso_ana}/10 vendas")
        st.progress(progresso_ana / 10)
        
        st.markdown(f"**Fernando:** {progresso_fernando}/10 vendas")
        st.progress(progresso_fernando / 10)
    
    with col2:
        st.markdown("#### 🎖️ Conquistas")
        
        conquistas = [
            "🎯 Ana: Maior ticket médio (R$ 2.100)",
            "⚡ Fernando: Mais vendas em um dia (8)",
            "🔥 Ana: Streak de 5 dias consecutivos",
            "💎 Fernando: Primeiro a atingir meta mensal",
        ]
        
        for conquista in conquistas:
            st.markdown(f"• {conquista}")
    
    # ========== PRÓXIMOS DESAFIOS ==========
    st.markdown("### 🚀 Próximos Desafios")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🎪 Desafio Carnaval**  
        Meta: R$ 25.000 em 7 dias  
        Prêmio: Viagem para o Rio  
        📅 15-21 de Fevereiro
        """)
    
    with col2:
        st.markdown("""
        **🌟 Desafio Score Alto**  
        Meta: 20 leads com score 9+  
        Prêmio: Jantar no melhor restaurante  
        📅 Março 2024
        """)
    
    with col3:
        st.markdown("""
        **💎 Desafio Trimestral**  
        Meta: R$ 150.000 no Q1  
        Prêmio: iPhone 15 Pro Max  
        📅 Q1 2024
        """)

def calcular_metricas_vendedor(vendas_df, leads_df, vendedor):
    """Calcula métricas específicas de um vendedor"""
    vendas_vendedor = vendas_df[vendas_df['vendedor'] == vendedor]
    leads_vendedor = leads_df[leads_df['vendedor'] == vendedor] if not leads_df.empty else pd.DataFrame()
    
    return {
        'faturamento': vendas_vendedor['valor'].sum() if not vendas_vendedor.empty else 0,
        'vendas': len(vendas_vendedor),
        'ticket_medio': vendas_vendedor['valor'].mean() if not vendas_vendedor.empty else 0,
        'leads_total': len(leads_vendedor) if not leads_vendedor.empty else 0,
        'leads_convertidos': len(leads_vendedor[leads_vendedor['status'] == 'fechado']) if not leads_vendedor.empty else 0,
        'score_medio': leads_vendedor['score'].mean() if not leads_vendedor.empty else 0
    }

def create_vendedor_card_detalhado(nome, metricas, is_vencedor):
    """Cria card detalhado do vendedor para a batalha"""
    
    tema = "Ana" if nome == "Ana" else "Fernando"
    classe = f"vendedor-{nome.lower()}"
    coroa = "👑" if is_vencedor else ""
    
    return f"""
    <div class="{classe}" style="position: relative;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h3 style="margin: 0;">👤 {nome} {coroa}</h3>
            {f'<div style="background: gold; color: black; padding: 0.2rem 0.5rem; border-radius: 15px; font-size: 0.8rem; font-weight: bold;">🏆 LÍDER</div>' if is_vencedor else ''}
        </div>
        
        <div style="margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between;">
                <span>💰 Faturamento:</span>
                <strong>R$ {metricas['faturamento']:,.2f}</strong>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>🏆 Vendas:</span>
                <strong>{metricas['vendas']}</strong>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>🎫 Ticket Médio:</span>
                <strong>R$ {metricas['ticket_medio']:,.2f}</strong>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>🎯 Leads:</span>
                <strong>{metricas['leads_total']}</strong>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>✅ Convertidos:</span>
                <strong>{metricas['leads_convertidos']}</strong>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>⭐ Score Médio:</span>
                <strong>{metricas['score_medio']:.1f}/10</strong>
            </div>
        </div>
        
        <div style="background: rgba(255,255,255,0.2); border-radius: 10px; padding: 0.5rem; text-align: center;">
            <strong>Performance: {'🔥 EXCELENTE' if is_vencedor else '💪 MUITO BOM'}</strong>
        </div>
    </div>
    """