"""
🔥 Instagram Insights Matadores
Sistema avançado de correlações e insights automáticos para vendas
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class InstagramSalesCorrelator:
    """Correlaciona dados do Instagram com vendas e leads"""
    
    def __init__(self, posts_df: pd.DataFrame, vendas_df: pd.DataFrame, leads_df: pd.DataFrame):
        self.posts_df = posts_df.copy()
        self.vendas_df = vendas_df.copy() 
        self.leads_df = leads_df.copy()
        
        # Preparar dados
        self._prepare_data()
        
    def _prepare_data(self):
        """Prepara e limpa os dados para análise"""
        
        # Verificar se DataFrames não estão vazios
        if self.posts_df.empty or self.vendas_df.empty or self.leads_df.empty:
            return
        
        # Converter datas de forma segura
        try:
            if 'date' in self.posts_df.columns:
                self.posts_df['date'] = pd.to_datetime(self.posts_df['date'])
            
            # Verificar qual coluna de data usar para vendas
            if 'data' in self.vendas_df.columns:
                self.vendas_df['data'] = pd.to_datetime(self.vendas_df['data'])
            elif 'created_at' in self.vendas_df.columns:
                self.vendas_df['data'] = pd.to_datetime(self.vendas_df['created_at'])
                
            # Verificar qual coluna de data usar para leads
            if 'created_at' in self.leads_df.columns:
                self.leads_df['created_at'] = pd.to_datetime(self.leads_df['created_at'])
            elif 'data' in self.leads_df.columns:
                self.leads_df['created_at'] = pd.to_datetime(self.leads_df['data'])
        except Exception as e:
            print(f"Erro ao converter datas: {e}")
            return
        
        # Adicionar métricas calculadas de forma segura
        if not self.posts_df.empty and all(col in self.posts_df.columns for col in ['saves', 'reach']):
            self.posts_df['viral_score'] = self._calculate_viral_score()
            self.posts_df['save_rate'] = (self.posts_df['saves'] / self.posts_df['reach'] * 100).round(2)
            
            if 'date' in self.posts_df.columns:
                self.posts_df['hour'] = self.posts_df['date'].dt.hour
                self.posts_df['weekday'] = self.posts_df['date'].dt.day_name()
        
        # Agrupar vendas e leads por dia de forma segura
        try:
            if not self.vendas_df.empty and 'data' in self.vendas_df.columns:
                valor_col = 'valor' if 'valor' in self.vendas_df.columns else 'preco'
                cliente_col = 'cliente' if 'cliente' in self.vendas_df.columns else 'nome'
                
                self.vendas_daily = self.vendas_df.groupby('data').agg({
                    valor_col: 'sum',
                    cliente_col: 'count'
                }).rename(columns={cliente_col: 'vendas_count', valor_col: 'valor'}).reset_index()
            else:
                self.vendas_daily = pd.DataFrame()
            
            if not self.leads_df.empty and 'created_at' in self.leads_df.columns:
                nome_col = 'nome' if 'nome' in self.leads_df.columns else 'cliente'
                
                agg_dict = {nome_col: 'count'}
                if 'origem' in self.leads_df.columns:
                    agg_dict['origem'] = lambda x: (x == 'Instagram').sum()
                
                self.leads_daily = self.leads_df.groupby(self.leads_df['created_at'].dt.date).agg(agg_dict)
                
                # Renomear colunas
                rename_dict = {nome_col: 'leads_count'}
                if 'origem' in agg_dict:
                    rename_dict['origem'] = 'leads_instagram'
                
                self.leads_daily = self.leads_daily.rename(columns=rename_dict).reset_index()
                self.leads_daily['created_at'] = pd.to_datetime(self.leads_daily['created_at'])
            else:
                self.leads_daily = pd.DataFrame()
                
        except Exception as e:
            print(f"Erro ao agrupar dados: {e}")
            self.vendas_daily = pd.DataFrame()
            self.leads_daily = pd.DataFrame()
        
    def _calculate_viral_score(self) -> pd.Series:
        """Calcula score viral baseado em múltiplas métricas"""
        
        if self.posts_df.empty:
            return pd.Series([])
        
        try:
            # Verificar se as colunas necessárias existem
            required_cols = ['reach', 'engagement_rate', 'saves', 'comments']
            missing_cols = [col for col in required_cols if col not in self.posts_df.columns]
            
            if missing_cols:
                print(f"Colunas ausentes para viral score: {missing_cols}")
                return pd.Series([50.0] * len(self.posts_df))  # Score padrão
            
            # Normalizar métricas (0-100) com proteção contra divisão por zero
            reach_max = self.posts_df['reach'].max()
            engagement_max = self.posts_df['engagement_rate'].max()
            saves_max = self.posts_df['saves'].max()
            comments_max = self.posts_df['comments'].max()
            
            reach_norm = (self.posts_df['reach'] / reach_max * 100) if reach_max > 0 else 0
            engagement_norm = (self.posts_df['engagement_rate'] / engagement_max * 100) if engagement_max > 0 else 0
            saves_norm = (self.posts_df['saves'] / saves_max * 100) if saves_max > 0 else 0
            comments_norm = (self.posts_df['comments'] / comments_max * 100) if comments_max > 0 else 0
            
            # Peso para cada métrica
            viral_score = (
                reach_norm * 0.3 +           # 30% reach
                engagement_norm * 0.25 +     # 25% engagement
                saves_norm * 0.25 +          # 25% saves (indicador forte)
                comments_norm * 0.20         # 20% comments
            ).round(1)
            
            return viral_score
            
        except Exception as e:
            print(f"Erro ao calcular viral score: {e}")
            return pd.Series([50.0] * len(self.posts_df))  # Score padrão
    
    def analyze_saves_to_sales(self) -> Dict[str, Any]:
        """Correlação: Posts com mais Saves → Dias com mais vendas"""
        
        try:
            if self.posts_df.empty or self.vendas_daily.empty:
                return {
                    'correlation': 0, 
                    'insight': 'Dados insuficientes para análise de correlação',
                    'data': pd.DataFrame(),
                    'top_saves_posts': pd.DataFrame(),
                    'best_save_rate': 0,
                    'avg_save_rate': 0
                }
            
            # Verificar se as colunas necessárias existem
            if 'date' not in self.posts_df.columns or 'saves' not in self.posts_df.columns:
                return {
                    'correlation': 0, 
                    'insight': 'Colunas necessárias não encontradas nos dados de posts',
                    'data': pd.DataFrame(),
                    'top_saves_posts': pd.DataFrame(),
                    'best_save_rate': 0,
                    'avg_save_rate': 0
                }
            
            # Posts por dia com save rate
            posts_daily = self.posts_df.groupby(self.posts_df['date'].dt.date).agg({
                'saves': 'sum',
                'reach': 'sum',
                'engagement_rate': 'mean'
            }).reset_index()
            posts_daily['date'] = pd.to_datetime(posts_daily['date'])
            posts_daily['save_rate'] = (posts_daily['saves'] / posts_daily['reach'] * 100).round(2)
            
            # Merge com vendas
            merged = pd.merge(posts_daily, self.vendas_daily, left_on='date', right_on='data', how='inner')
            
            if len(merged) < 3:
                return {
                    'correlation': 0, 
                    'insight': 'Dados insuficientes para análise (menos de 3 pontos)',
                    'data': merged,
                    'top_saves_posts': pd.DataFrame(),
                    'best_save_rate': posts_daily['save_rate'].max() if not posts_daily.empty else 0,
                    'avg_save_rate': posts_daily['save_rate'].mean() if not posts_daily.empty else 0
                }
            
            # Calcular correlação
            correlation = merged['save_rate'].corr(merged['valor'])
            if pd.isna(correlation):
                correlation = 0
            
            # Top posts com mais saves
            required_cols = ['date', 'saves']
            optional_cols = ['caption', 'type']
            
            available_cols = [col for col in required_cols + optional_cols if col in self.posts_df.columns]
            top_saves_posts = self.posts_df.nlargest(5, 'saves')[available_cols] if 'saves' in self.posts_df.columns else pd.DataFrame()
            
            # Insight automático
            if correlation > 0.6:
                insight = f"🔥 FORTE correlação! Posts com mais saves aumentam vendas em {abs(correlation)*100:.0f}%"
            elif correlation > 0.3:
                insight = f"📈 Correlação moderada: saves impactam vendas em {abs(correlation)*100:.0f}%"
            else:
                insight = f"⚠️ Baixa correlação: saves não impactam diretamente vendas"
            
            return {
                'correlation': round(correlation, 3),
                'insight': insight,
                'data': merged,
                'top_saves_posts': top_saves_posts,
                'best_save_rate': posts_daily['save_rate'].max() if not posts_daily.empty else 0,
                'avg_save_rate': posts_daily['save_rate'].mean() if not posts_daily.empty else 0
            }
            
        except Exception as e:
            print(f"Erro em analyze_saves_to_sales: {e}")
            return {
                'correlation': 0,
                'insight': 'Erro na análise de correlação',
                'data': pd.DataFrame(),
                'top_saves_posts': pd.DataFrame(),
                'best_save_rate': 0,
                'avg_save_rate': 0
            }
    
    def analyze_stories_to_leads(self) -> Dict[str, Any]:
        """Análise: Stories com links → Leads gerados"""
        
        # Simular dados de stories (seria da API real)
        stories_data = self._generate_stories_data()
        stories_df = pd.DataFrame(stories_data)
        
        # Correlacionar com leads do Instagram
        instagram_leads = self.leads_df[self.leads_df['origem'] == 'Instagram']
        
        leads_by_day = instagram_leads.groupby(
            instagram_leads['created_at'].dt.date
        ).size().reset_index(name='leads_count')
        leads_by_day['date'] = pd.to_datetime(leads_by_day['created_at'])
        
        # Merge stories com leads
        merged = pd.merge(stories_df, leads_by_day, on='date', how='left').fillna(0)
        
        # Calcular métricas
        total_story_clicks = merged['link_clicks'].sum()
        total_leads = merged['leads_count'].sum()
        conversion_rate = (total_leads / total_story_clicks * 100) if total_story_clicks > 0 else 0
        
        # Melhores horários para stories
        best_hours = stories_df.groupby('hour')['link_clicks'].mean().sort_values(ascending=False).head(3)
        
        return {
            'total_story_clicks': int(total_story_clicks),
            'total_leads': int(total_leads),
            'conversion_rate': round(conversion_rate, 2),
            'best_hours': best_hours.to_dict(),
            'data': merged,
            'insight': f"Stories geram {conversion_rate:.1f}% de conversão para leads"
        }
    
    def analyze_viral_funnel(self) -> Dict[str, Any]:
        """Análise: Reels virais → Followers → Leads → Vendas"""
        
        # Identificar reels virais (score > 75)
        viral_reels = self.posts_df[
            (self.posts_df['type'] == 'VIDEO') & 
            (self.posts_df['viral_score'] > 75)
        ].copy()
        
        if len(viral_reels) == 0:
            return {'insight': 'Nenhum reel viral identificado', 'viral_reels': pd.DataFrame()}
        
        # Simular crescimento de followers após reels virais
        viral_impact = []
        
        for _, reel in viral_reels.iterrows():
            date = reel['date']
            
            # Simular impacto nos próximos 7 dias
            followers_gain = int(reel['viral_score'] * 2.5)  # Score 80 = +200 followers
            leads_generated = int(followers_gain * 0.03)     # 3% dos novos followers viram leads
            sales_generated = int(leads_generated * 0.15)    # 15% dos leads viram vendas
            
            viral_impact.append({
                'reel_date': date,
                'viral_score': reel['viral_score'],
                'caption_preview': reel['caption'][:50] + '...',
                'followers_gain': followers_gain,
                'leads_generated': leads_generated,
                'sales_generated': sales_generated,
                'roi_estimated': sales_generated * 1997  # Valor médio venda
            })
        
        viral_df = pd.DataFrame(viral_impact)
        
        # Métricas totais
        total_followers = viral_df['followers_gain'].sum()
        total_leads = viral_df['leads_generated'].sum() 
        total_sales = viral_df['sales_generated'].sum()
        total_roi = viral_df['roi_estimated'].sum()
        
        return {
            'viral_reels_count': len(viral_reels),
            'total_followers_gain': total_followers,
            'total_leads_generated': total_leads,
            'total_sales_generated': total_sales,
            'total_roi': total_roi,
            'viral_reels': viral_df,
            'insight': f"🚀 {len(viral_reels)} reels virais geraram {total_followers:,} followers e R$ {total_roi:,.2f}"
        }
    
    def analyze_posting_time_conversion(self) -> Dict[str, Any]:
        """Análise: Horário do post → Velocidade de conversão"""
        
        # Analisar velocidade de conversão por horário
        hourly_performance = self.posts_df.groupby('hour').agg({
            'engagement_rate': 'mean',
            'saves': 'mean',
            'reach': 'mean',
            'viral_score': 'mean'
        }).round(2)
        
        # Simular velocidade de conversão (horas até primeira venda)
        conversion_speed = {}
        for hour in range(24):
            if hour in [8, 9, 12, 13, 18, 19, 20, 21]:  # Horários prime
                speed = np.random.uniform(2, 6)  # 2-6 horas
            elif hour in [10, 11, 14, 15, 16, 17, 22]:  # Horários médios
                speed = np.random.uniform(6, 12)  # 6-12 horas
            else:  # Horários fracos
                speed = np.random.uniform(12, 24)  # 12-24 horas
            
            conversion_speed[hour] = round(speed, 1)
        
        # Identificar horários golden
        hourly_performance['conversion_speed'] = hourly_performance.index.map(conversion_speed)
        
        # Melhores horários (alto engagement + conversão rápida)
        hourly_performance['performance_score'] = (
            hourly_performance['engagement_rate'] * 0.4 +
            hourly_performance['viral_score'] * 0.3 +
            (24 - hourly_performance['conversion_speed']) * 0.3  # Inversão: menos horas = melhor
        )
        
        best_hours = hourly_performance.nlargest(3, 'performance_score')
        worst_hours = hourly_performance.nsmallest(3, 'performance_score')
        
        return {
            'hourly_data': hourly_performance,
            'best_hours': best_hours,
            'worst_hours': worst_hours,
            'golden_hour': best_hours.index[0],
            'fastest_conversion': min(conversion_speed.values()),
            'insight': f"⚡ Melhor horário: {best_hours.index[0]}h - conversão em {best_hours.iloc[0]['conversion_speed']:.1f}h"
        }
    
    def _generate_stories_data(self) -> List[Dict]:
        """Gera dados simulados de stories para demonstração"""
        
        stories = []
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        
        for date in dates:
            # 1-3 stories por dia
            num_stories = np.random.randint(1, 4)
            
            for i in range(num_stories):
                hour = np.random.choice([9, 12, 15, 18, 20, 21, 22], p=[0.1, 0.15, 0.1, 0.2, 0.25, 0.15, 0.05])
                
                # Stories com link têm mais clicks nos horários prime
                if hour in [18, 20, 21]:
                    link_clicks = np.random.randint(25, 85)
                elif hour in [12, 15]:
                    link_clicks = np.random.randint(15, 45)
                else:
                    link_clicks = np.random.randint(5, 25)
                
                stories.append({
                    'date': date,
                    'hour': hour,
                    'story_type': 'link' if np.random.random() > 0.4 else 'normal',
                    'views': np.random.randint(300, 1200),
                    'link_clicks': link_clicks if np.random.random() > 0.4 else 0,
                    'profile_visits': np.random.randint(5, 30)
                })
        
        return stories

class AutoInsightGenerator:
    """Gera insights automáticos baseados nas análises"""
    
    def __init__(self, correlator: InstagramSalesCorrelator):
        self.correlator = correlator
        
    def generate_all_insights(self) -> List[Dict[str, Any]]:
        """Gera todos os insights automáticos"""
        
        insights = []
        
        # 1. Análise de Saves x Vendas
        saves_analysis = self.correlator.analyze_saves_to_sales()
        if saves_analysis['correlation'] > 0.5:
            insights.append({
                'type': 'saves_correlation',
                'priority': 'high',
                'title': '🔥 Posts com Saves Geram Mais Vendas!',
                'message': saves_analysis['insight'],
                'action': f"Foque em conteúdo que gere saves - sua taxa atual é {saves_analysis['avg_save_rate']:.1f}%",
                'data': saves_analysis
            })
        
        # 2. Análise de Tipo de Conteúdo
        content_insights = self._analyze_content_performance()
        insights.extend(content_insights)
        
        # 3. Análise de Hashtags
        hashtag_insights = self._analyze_hashtag_performance()
        insights.extend(hashtag_insights)
        
        # 4. Análise de Horários
        timing_analysis = self.correlator.analyze_posting_time_conversion()
        insights.append({
            'type': 'optimal_timing',
            'priority': 'medium',
            'title': '⏰ Horário Ideal Identificado!',
            'message': timing_analysis['insight'],
            'action': f"Poste às {timing_analysis['golden_hour']}h para conversão {timing_analysis['fastest_conversion']:.1f}h mais rápida",
            'data': timing_analysis
        })
        
        # 5. Análise Viral
        viral_analysis = self.correlator.analyze_viral_funnel()
        if viral_analysis.get('viral_reels_count', 0) > 0:
            insights.append({
                'type': 'viral_content',
                'priority': 'high',
                'title': '🚀 Conteúdo Viral Identificado!',
                'message': viral_analysis['insight'],
                'action': f"Replique o padrão dos {viral_analysis['viral_reels_count']} reels virais",
                'data': viral_analysis
            })
        
        # 6. Stories Performance
        stories_analysis = self.correlator.analyze_stories_to_leads()
        best_story_hour = max(stories_analysis['best_hours'], key=stories_analysis['best_hours'].get)
        insights.append({
            'type': 'stories_performance',
            'priority': 'medium',
            'title': '📱 Stories Gerando Leads!',
            'message': f"Stories às {best_story_hour}h geram {stories_analysis['best_hours'][best_story_hour]:.0f} clicks médios",
            'action': f"Publique stories com link às {best_story_hour}h - conversão atual: {stories_analysis['conversion_rate']:.1f}%",
            'data': stories_analysis
        })
        
        return sorted(insights, key=lambda x: {'high': 3, 'medium': 2, 'low': 1}[x['priority']], reverse=True)
    
    def _analyze_content_performance(self) -> List[Dict[str, Any]]:
        """Analisa performance por tipo de conteúdo"""
        
        insights = []
        
        # Performance por tipo
        type_performance = self.correlator.posts_df.groupby('type').agg({
            'engagement_rate': 'mean',
            'saves': 'mean',
            'reach': 'mean',
            'viral_score': 'mean'
        }).round(2)
        
        if len(type_performance) > 1:
            best_type = type_performance['engagement_rate'].idxmax()
            best_engagement = type_performance.loc[best_type, 'engagement_rate']
            
            # Traduzir tipos
            type_names = {
                'VIDEO': 'Vídeos/Reels',
                'IMAGE': 'Fotos',
                'CAROUSEL_ALBUM': 'Carrosséis'
            }
            
            insights.append({
                'type': 'content_type',
                'priority': 'high',
                'title': f'🎥 {type_names.get(best_type, best_type)} Convertem Mais!',
                'message': f"{type_names.get(best_type, best_type)} têm {best_engagement:.1f}% de engagement",
                'action': f"Publique mais {type_names.get(best_type, best_type).lower()} - {best_engagement:.0f}% mais efetivo",
                'data': type_performance
            })
        
        return insights
    
    def _analyze_hashtag_performance(self) -> List[Dict[str, Any]]:
        """Analisa performance de hashtags simuladas"""
        
        insights = []
        
        # Simular análise de hashtags que trouxeram leads
        hashtag_leads = {
            '#vendas': {'leads': 12, 'qualified': 8},
            '#instagram': {'leads': 8, 'qualified': 5},
            '#dermato': {'leads': 10, 'qualified': 9},  # Alto qualify rate
            '#marketing': {'leads': 6, 'qualified': 3},
            '#negocios': {'leads': 9, 'qualified': 4}
        }
        
        # Identificar hashtag com melhor qualify rate
        best_hashtag = max(hashtag_leads.items(), 
                          key=lambda x: x[1]['qualified'] / x[1]['leads'] if x[1]['leads'] > 0 else 0)
        
        qualify_rate = (best_hashtag[1]['qualified'] / best_hashtag[1]['leads'] * 100)
        
        insights.append({
            'type': 'hashtag_performance',
            'priority': 'medium', 
            'title': f'#️⃣ {best_hashtag[0]} = Leads Qualificados!',
            'message': f"{best_hashtag[0]} trouxe {best_hashtag[1]['qualified']} leads qualificados",
            'action': f"Use mais {best_hashtag[0]} - {qualify_rate:.0f}% de qualificação vs {best_hashtag[1]['leads']} leads totais",
            'data': hashtag_leads
        })
        
        return insights

def create_insight_visualizations(insights: List[Dict]) -> Dict[str, go.Figure]:
    """Cria visualizações para os insights"""
    
    figures = {}
    
    for insight in insights:
        insight_type = insight['type']
        data = insight.get('data', {})
        
        if insight_type == 'saves_correlation' and 'data' in data:
            # Gráfico saves vs vendas
            df = data['data']
            fig = px.scatter(
                df, 
                x='save_rate', 
                y='valor',
                title='📊 Correlação: Save Rate vs Vendas',
                labels={'save_rate': 'Taxa de Saves (%)', 'valor': 'Vendas (R$)'},
                trendline='ols'
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            figures['saves_correlation'] = fig
        
        elif insight_type == 'content_type' and isinstance(data, pd.DataFrame):
            # Gráfico performance por tipo
            fig = px.bar(
                x=data.index,
                y=data['engagement_rate'],
                title='🎯 Performance por Tipo de Conteúdo',
                labels={'x': 'Tipo', 'y': 'Engagement Rate (%)'},
                color=data['engagement_rate'],
                color_continuous_scale='viridis'
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            figures['content_type'] = fig
        
        elif insight_type == 'optimal_timing' and 'hourly_data' in data:
            # Heatmap de performance por horário
            hourly_data = data['hourly_data']
            
            fig = px.bar(
                x=hourly_data.index,
                y=hourly_data['engagement_rate'],
                title='⏰ Performance por Horário',
                labels={'x': 'Hora', 'y': 'Engagement Rate (%)'},
                color=hourly_data['performance_score'],
                color_continuous_scale='plasma'
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            figures['optimal_timing'] = fig
    
    return figures