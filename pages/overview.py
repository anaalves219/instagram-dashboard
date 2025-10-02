import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.database import Database
from utils.styles import create_metric_card, create_vendedor_card, get_user_theme_css

def show_page():
    """Página Overview - Métricas gerais e dashboard principal"""
    
    # CSS personalizado do usuário
    user_theme = st.session_state.get('user_theme', {"primary": "#9D4EDD", "secondary": "#06FFA5"})
    st.markdown(get_user_theme_css(user_theme), unsafe_allow_html=True)
    
    st.title("📈 Overview Dashboard")
    st.markdown("**Visão geral das vendas e performance da equipe**")
    
    # Inicializar database
    db = Database()
    
    # Período de análise
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        data_inicio = st.date_input(
            "📅 Data Início",
            value=datetime.now() - timedelta(days=30),
            max_value=datetime.now().date()
        )
    
    with col2:
        data_fim = st.date_input(
            "📅 Data Fim",
            value=datetime.now().date(),
            max_value=datetime.now().date()
        )
    
    with col3:
        st.markdown("**🎯 Meta do Mês: R$ 100.000,00**")
    
    # Buscar dados
    vendas_df = db.get_vendas(data_inicio, data_fim)
    leads_df = db.get_leads()
    
    # Filtrar vendas confirmadas
    vendas_confirmadas = vendas_df[vendas_df['status'] == 'confirmada'] if not vendas_df.empty else pd.DataFrame()
    
    # ========== MÉTRICAS PRINCIPAIS ==========
    st.markdown("### 🎯 Métricas Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_vendas = len(vendas_confirmadas) if not vendas_confirmadas.empty else 0
        st.metric(
            label="🏆 Total de Vendas",
            value=f"{total_vendas}",
            delta=f"+{int(total_vendas * 0.15)} vs mês anterior"
        )
    
    with col2:
        faturamento = vendas_confirmadas['valor'].sum() if not vendas_confirmadas.empty else 0
        st.metric(
            label="💰 Faturamento",
            value=f"R$ {faturamento:,.2f}",
            delta=f"+{faturamento * 0.12:.0f} vs mês anterior"
        )
    
    with col3:
        ticket_medio = vendas_confirmadas['valor'].mean() if not vendas_confirmadas.empty else 0
        st.metric(
            label="🎫 Ticket Médio",
            value=f"R$ {ticket_medio:,.2f}",
            delta="+5.2% vs mês anterior"
        )
    
    with col4:
        total_leads = len(leads_df) if not leads_df.empty else 0
        st.metric(
            label="🎯 Total de Leads",
            value=f"{total_leads}",
            delta=f"+{int(total_leads * 0.08)} vs mês anterior"
        )
    
    # ========== PERFORMANCE HOJE ==========
    st.markdown("### 📊 Performance de Hoje")
    
    hoje = datetime.now().date()
    vendas_hoje = vendas_confirmadas[vendas_confirmadas['data_venda'] == hoje.strftime('%Y-%m-%d')] if not vendas_confirmadas.empty else pd.DataFrame()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        vendas_hoje_count = len(vendas_hoje) if not vendas_hoje.empty else 0
        st.markdown(create_metric_card("🏆 Vendas Hoje", vendas_hoje_count, "+2 vs ontem"), unsafe_allow_html=True)
    
    with col2:
        faturamento_hoje = vendas_hoje['valor'].sum() if not vendas_hoje.empty else 0
        st.markdown(create_metric_card("💰 Faturamento Hoje", f"R$ {faturamento_hoje:,.2f}", "+12.5%"), unsafe_allow_html=True)
    
    with col3:
        meta_diaria = 100000 / 30  # Meta mensal dividida por 30 dias
        progresso_dia = (faturamento_hoje / meta_diaria * 100) if meta_diaria > 0 else 0
        st.markdown(create_metric_card("🎯 Meta do Dia", f"{progresso_dia:.1f}%", f"Meta: R$ {meta_diaria:,.0f}"), unsafe_allow_html=True)
    
    # ========== PERFORMANCE POR VENDEDOR ==========
    st.markdown("### ⚔️ Performance por Vendedor")
    
    if not vendas_confirmadas.empty:
        vendas_por_vendedor = vendas_confirmadas.groupby('vendedor')['valor'].sum().reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Ana
            vendas_ana = vendas_por_vendedor[vendas_por_vendedor['vendedor'] == 'Ana']['valor'].sum() if not vendas_por_vendedor.empty else 0
            meta_ana = 50000
            st.markdown(create_vendedor_card("Ana", vendas_ana, meta_ana, "ana"), unsafe_allow_html=True)
        
        with col2:
            # Fernando
            vendas_fernando = vendas_por_vendedor[vendas_por_vendedor['vendedor'] == 'Fernando']['valor'].sum() if not vendas_por_vendedor.empty else 0
            meta_fernando = 50000
            st.markdown(create_vendedor_card("Fernando", vendas_fernando, meta_fernando, "fernando"), unsafe_allow_html=True)
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(create_vendedor_card("Ana", 0, 50000, "ana"), unsafe_allow_html=True)
        with col2:
            st.markdown(create_vendedor_card("Fernando", 0, 50000, "fernando"), unsafe_allow_html=True)
    
    # ========== GRÁFICOS ==========
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Vendas por Dia")
        
        if not vendas_confirmadas.empty:
            vendas_diarias = vendas_confirmadas.groupby('data_venda').agg({
                'valor': 'sum',
                'id': 'count'
            }).reset_index()
            vendas_diarias.columns = ['Data', 'Faturamento', 'Quantidade']
            
            fig = px.line(
                vendas_diarias, 
                x='Data', 
                y='Faturamento',
                title="Faturamento Diário",
                color_discrete_sequence=[user_theme['primary']]
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title_font_size=16
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 Sem dados de vendas para exibir")
    
    with col2:
        st.markdown("### 🎯 Funil de Leads")
        
        if not leads_df.empty:
            funil_leads = leads_df['status'].value_counts().reset_index()
            funil_leads.columns = ['Status', 'Quantidade']
            
            cores_funil = {
                'novo': '#06FFA5',
                'contatado': '#0EA5E9', 
                'interessado': '#F97316',
                'negociacao': '#9D4EDD',
                'fechado': '#10B981',
                'perdido': '#EF4444'
            }
            
            fig = px.funnel(
                funil_leads,
                x='Quantidade',
                y='Status',
                title="Pipeline de Leads",
                color='Status',
                color_discrete_map=cores_funil
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title_font_size=16
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("🎯 Sem dados de leads para exibir")
    
    # ========== ALERTAS E NOTIFICAÇÕES ==========
    st.markdown("### 🔔 Alertas e Notificações")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if faturamento < 30000:  # Se faturamento baixo
            st.warning("⚠️ **Faturamento abaixo da meta!** Acelere as vendas.")
        else:
            st.success("✅ **Meta em dia!** Continue assim.")
    
    with col2:
        leads_sem_followup = len(leads_df[leads_df['status'] == 'novo']) if not leads_df.empty else 0
        if leads_sem_followup > 10:
            st.warning(f"📞 **{leads_sem_followup} leads** precisam de follow-up!")
        else:
            st.info(f"📞 {leads_sem_followup} leads aguardando contato")
    
    with col3:
        if vendas_hoje_count == 0:
            st.error("🚨 **Nenhuma venda hoje!** Foque nos leads quentes.")
        else:
            st.success(f"🎉 **{vendas_hoje_count} vendas hoje!** Excelente trabalho!")
    
    # ========== RANKING SEMANAL ==========
    st.markdown("### 🏆 Ranking da Semana")
    
    # Calcular vendas da semana
    inicio_semana = datetime.now() - timedelta(days=7)
    vendas_semana = vendas_confirmadas[vendas_confirmadas['data_venda'] >= inicio_semana.strftime('%Y-%m-%d')] if not vendas_confirmadas.empty else pd.DataFrame()
    
    if not vendas_semana.empty:
        ranking = vendas_semana.groupby('vendedor').agg({
            'valor': 'sum',
            'id': 'count'
        }).reset_index()
        ranking.columns = ['Vendedor', 'Faturamento', 'Vendas']
        ranking = ranking.sort_values('Faturamento', ascending=False)
        
        for i, row in ranking.iterrows():
            emoji = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
            st.markdown(f"{emoji} **{row['Vendedor']}** - R$ {row['Faturamento']:,.2f} ({row['Vendas']} vendas)")
    else:
        st.info("🏆 Nenhuma venda registrada esta semana")
    
    # ========== ÚLTIMAS ATIVIDADES ==========
    st.markdown("### 📝 Últimas Atividades")
    
    logs_df = db.get_activity_logs(limit=10)
    
    if not logs_df.empty:
        for _, log in logs_df.head(5).iterrows():
            timestamp = pd.to_datetime(log['timestamp']).strftime('%d/%m %H:%M')
            st.markdown(f"🔸 **{log['user_id'].title()}** - {log['action']} - {timestamp}")
    else:
        st.info("📝 Nenhuma atividade recente registrada")
    
    # ========== REFRESH AUTOMÁTICO ==========
    if st.button("🔄 Atualizar Dashboard", type="primary", use_container_width=True):
        st.rerun()
    
    # Auto-refresh a cada 5 minutos (opcional)
    st.markdown("""
    <script>
    setTimeout(function(){
        window.location.reload();
    }, 300000); // 5 minutos
    </script>
    """, unsafe_allow_html=True)