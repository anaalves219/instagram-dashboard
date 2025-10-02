import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime, timedelta
import json

class Database:
    def __init__(self):
        self.supabase_url = st.secrets.get("SUPABASE_URL", "")
        self.supabase_key = st.secrets.get("SUPABASE_ANON_KEY", "")
        
        if self.supabase_url and self.supabase_key:
            self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        else:
            self.supabase = None
            st.warning("⚠️ Configuração do Supabase não encontrada. Usando dados de exemplo.")
    
    def is_connected(self):
        return self.supabase is not None
    
    def log_activity(self, user_id: str, action: str, details: str = ""):
        """Registra atividade do usuário"""
        if not self.is_connected():
            return
        
        try:
            self.supabase.table('activity_logs').insert({
                'user_id': user_id,
                'action': action,
                'details': details,
                'timestamp': datetime.now().isoformat()
            }).execute()
        except Exception as e:
            st.error(f"Erro ao registrar atividade: {e}")
    
    # VENDAS
    def get_vendas(self, start_date=None, end_date=None):
        """Busca vendas com filtros de data"""
        if not self.is_connected():
            st.error("⚠️ **Supabase não configurado!** Configure SUPABASE_URL e SUPABASE_ANON_KEY nos secrets.")
            return pd.DataFrame()
        
        try:
            query = self.supabase.table('vendas').select('*')
            
            if start_date:
                query = query.gte('data_venda', start_date.isoformat())
            if end_date:
                query = query.lte('data_venda', end_date.isoformat())
                
            result = query.order('data_venda', desc=True).execute()
            return pd.DataFrame(result.data)
        except Exception as e:
            st.error(f"Erro ao buscar vendas: {e}")
            return pd.DataFrame()
    
    def add_venda(self, venda_data):
        """Adiciona nova venda"""
        if not self.is_connected():
            st.error("⚠️ Configure o Supabase para adicionar vendas!")
            return False
        
        try:
            result = self.supabase.table('vendas').insert(venda_data).execute()
            return True
        except Exception as e:
            st.error(f"Erro ao adicionar venda: {e}")
            return False
    
    def update_venda(self, venda_id, venda_data):
        """Atualiza venda existente"""
        if not self.is_connected():
            st.success("✅ Venda atualizada (modo demo)")
            return True
        
        try:
            result = self.supabase.table('vendas').update(venda_data).eq('id', venda_id).execute()
            return True
        except Exception as e:
            st.error(f"Erro ao atualizar venda: {e}")
            return False
    
    def delete_venda(self, venda_id):
        """Remove venda"""
        if not self.is_connected():
            st.success("✅ Venda removida (modo demo)")
            return True
        
        try:
            result = self.supabase.table('vendas').delete().eq('id', venda_id).execute()
            return True
        except Exception as e:
            st.error(f"Erro ao remover venda: {e}")
            return False
    
    # LEADS
    def get_leads(self, status=None):
        """Busca leads com filtro de status"""
        if not self.is_connected():
            st.error("⚠️ **Supabase não configurado!** Configure SUPABASE_URL e SUPABASE_ANON_KEY nos secrets.")
            return pd.DataFrame()
        
        try:
            query = self.supabase.table('leads').select('*')
            
            if status:
                query = query.eq('status', status)
                
            result = query.order('created_at', desc=True).execute()
            return pd.DataFrame(result.data)
        except Exception as e:
            st.error(f"Erro ao buscar leads: {e}")
            return pd.DataFrame()
    
    def add_lead(self, lead_data):
        """Adiciona novo lead"""
        if not self.is_connected():
            st.error("⚠️ Configure o Supabase para adicionar leads!")
            return False
        
        try:
            result = self.supabase.table('leads').insert(lead_data).execute()
            return True
        except Exception as e:
            st.error(f"Erro ao adicionar lead: {e}")
            return False
    
    def update_lead(self, lead_id, lead_data):
        """Atualiza lead existente"""
        if not self.is_connected():
            st.success("✅ Lead atualizado (modo demo)")
            return True
        
        try:
            result = self.supabase.table('leads').update(lead_data).eq('id', lead_id).execute()
            return True
        except Exception as e:
            st.error(f"Erro ao atualizar lead: {e}")
            return False
    
    # DADOS MOCK
    def _get_mock_vendas(self):
        """Dados de exemplo para vendas"""
        data = []
        today = datetime.now()
        
        for i in range(30):
            date = today - timedelta(days=i)
            vendedor = "Ana" if i % 2 == 0 else "Fernando"
            
            data.append({
                'id': i + 1,
                'cliente_nome': f"Cliente {i+1}",
                'cliente_instagram': f"@cliente{i+1}",
                'produto': "Curso High Ticket",
                'valor': 1997.0,
                'vendedor': vendedor,
                'data_venda': date.strftime('%Y-%m-%d'),
                'status': 'confirmada' if i % 4 != 0 else 'pendente',
                'meio_pagamento': 'PIX' if i % 3 == 0 else 'Cartão',
                'comissao_pct': 0.3,
                'created_at': date.isoformat()
            })
        
        return pd.DataFrame(data)
    
    def _get_mock_leads(self):
        """Dados de exemplo para leads"""
        data = []
        today = datetime.now()
        statuses = ['novo', 'contatado', 'interessado', 'negociacao', 'fechado', 'perdido']
        
        for i in range(50):
            date = today - timedelta(days=i // 2)
            vendedor = "Ana" if i % 2 == 0 else "Fernando"
            
            data.append({
                'id': i + 1,
                'nome': f"Lead {i+1}",
                'instagram': f"@lead{i+1}",
                'telefone': f"(11) 9999-{i:04d}",
                'email': f"lead{i+1}@email.com",
                'status': statuses[i % len(statuses)],
                'origem': 'Instagram' if i % 3 == 0 else 'WhatsApp',
                'vendedor': vendedor,
                'nota': f"Anotações sobre o lead {i+1}",
                'score': (i % 10) + 1,
                'ultima_interacao': date.strftime('%Y-%m-%d'),
                'created_at': date.isoformat()
            })
        
        return pd.DataFrame(data)
    
    def get_activity_logs(self, user_id=None, limit=50):
        """Busca logs de atividade"""
        if not self.is_connected():
            return pd.DataFrame()
        
        try:
            query = self.supabase.table('activity_logs').select('*')
            
            if user_id:
                query = query.eq('user_id', user_id)
                
            result = query.order('timestamp', desc=True).limit(limit).execute()
            return pd.DataFrame(result.data)
        except Exception as e:
            st.error(f"Erro ao buscar logs: {e}")
            return pd.DataFrame()
    
    def _get_mock_activity_logs(self):
        """Dados de exemplo para logs"""
        data = []
        today = datetime.now()
        actions = ['Venda Adicionada', 'Lead Atualizado', 'Login', 'Export Realizado']
        
        for i in range(20):
            date = today - timedelta(hours=i)
            user = "Ana" if i % 2 == 0 else "Fernando"
            
            data.append({
                'id': i + 1,
                'user_id': user.lower(),
                'action': actions[i % len(actions)],
                'details': f"Detalhes da ação {i+1}",
                'timestamp': date.isoformat()
            })
        
        return pd.DataFrame(data)