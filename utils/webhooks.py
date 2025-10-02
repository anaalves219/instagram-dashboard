import requests
import json
from datetime import datetime
import streamlit as st
import hashlib
import hmac
from typing import Dict, Any, Optional

class WebhookManager:
    """Gerenciador de webhooks para integração com sistemas externos"""
    
    def __init__(self):
        self.n8n_webhook_url = st.secrets.get("N8N_WEBHOOK", "")
        self.n8n_auth_token = st.secrets.get("N8N_AUTH_TOKEN", "")
        self.instagram_webhook_secret = st.secrets.get("INSTAGRAM_WEBHOOK_SECRET", "")
        self.whatsapp_webhook_secret = st.secrets.get("WHATSAPP_WEBHOOK_SECRET", "")
    
    def send_to_n8n(self, event_type: str, data: Dict[str, Any]) -> bool:
        """Envia dados para N8N via webhook"""
        if not self.n8n_webhook_url:
            return False
        
        try:
            payload = {
                "timestamp": datetime.now().isoformat(),
                "event_type": event_type,
                "source": "instagram_sales_dashboard",
                "data": data
            }
            
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Instagram-Sales-Dashboard/1.0"
            }
            
            if self.n8n_auth_token:
                headers["Authorization"] = f"Bearer {self.n8n_auth_token}"
            
            response = requests.post(
                self.n8n_webhook_url,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception as e:
            st.error(f"Erro ao enviar webhook para N8N: {e}")
            return False
    
    def notify_new_sale(self, venda_data: Dict[str, Any]) -> bool:
        """Notifica nova venda via webhook"""
        return self.send_to_n8n("nova_venda", {
            "cliente_nome": venda_data.get("cliente_nome"),
            "valor": venda_data.get("valor"),
            "vendedor": venda_data.get("vendedor"),
            "produto": venda_data.get("produto"),
            "data_venda": venda_data.get("data_venda"),
            "meio_pagamento": venda_data.get("meio_pagamento")
        })
    
    def notify_new_lead(self, lead_data: Dict[str, Any]) -> bool:
        """Notifica novo lead via webhook"""
        return self.send_to_n8n("novo_lead", {
            "nome": lead_data.get("nome"),
            "telefone": lead_data.get("telefone"),
            "instagram": lead_data.get("instagram"),
            "vendedor": lead_data.get("vendedor"),
            "origem": lead_data.get("origem"),
            "score": lead_data.get("score"),
            "status": lead_data.get("status")
        })
    
    def notify_goal_achieved(self, goal_data: Dict[str, Any]) -> bool:
        """Notifica meta atingida via webhook"""
        return self.send_to_n8n("meta_atingida", {
            "vendedor": goal_data.get("vendedor"),
            "tipo_meta": goal_data.get("tipo_meta"),
            "valor_meta": goal_data.get("valor_meta"),
            "valor_atingido": goal_data.get("valor_atingido"),
            "data_conclusao": goal_data.get("data_conclusao")
        })
    
    def notify_lead_followup(self, lead_data: Dict[str, Any]) -> bool:
        """Notifica follow-up de lead via webhook"""
        return self.send_to_n8n("followup_lead", {
            "nome": lead_data.get("nome"),
            "telefone": lead_data.get("telefone"),
            "vendedor": lead_data.get("vendedor"),
            "dias_sem_contato": lead_data.get("dias_sem_contato"),
            "score": lead_data.get("score"),
            "urgencia": lead_data.get("urgencia", "normal")
        })
    
    def send_daily_report(self, report_data: Dict[str, Any]) -> bool:
        """Envia relatório diário via webhook"""
        return self.send_to_n8n("relatorio_diario", {
            "data": report_data.get("data"),
            "total_vendas": report_data.get("total_vendas"),
            "faturamento": report_data.get("faturamento"),
            "novos_leads": report_data.get("novos_leads"),
            "leads_convertidos": report_data.get("leads_convertidos"),
            "vendas_ana": report_data.get("vendas_ana"),
            "vendas_fernando": report_data.get("vendas_fernando")
        })
    
    def verify_instagram_webhook(self, signature: str, payload: str) -> bool:
        """Verifica assinatura do webhook do Instagram"""
        if not self.instagram_webhook_secret:
            return False
        
        try:
            expected_signature = hmac.new(
                self.instagram_webhook_secret.encode(),
                payload.encode(),
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(f"sha256={expected_signature}", signature)
            
        except Exception:
            return False
    
    def verify_whatsapp_webhook(self, signature: str, payload: str) -> bool:
        """Verifica assinatura do webhook do WhatsApp"""
        if not self.whatsapp_webhook_secret:
            return False
        
        try:
            expected_signature = hmac.new(
                self.whatsapp_webhook_secret.encode(),
                payload.encode(),
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(f"sha256={expected_signature}", signature)
            
        except Exception:
            return False
    
    def process_instagram_webhook(self, webhook_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Processa webhook recebido do Instagram"""
        try:
            # Extrair dados relevantes do webhook
            if webhook_data.get("object") == "instagram":
                entries = webhook_data.get("entry", [])
                
                for entry in entries:
                    changes = entry.get("changes", [])
                    
                    for change in changes:
                        field = change.get("field")
                        value = change.get("value", {})
                        
                        if field == "comments":
                            # Novo comentário
                            comment_data = {
                                "id": value.get("id"),
                                "text": value.get("text"),
                                "from": value.get("from", {}).get("username"),
                                "media_id": value.get("media", {}).get("id"),
                                "timestamp": datetime.now().isoformat()
                            }
                            
                            # Enviar para N8N para processamento
                            self.send_to_n8n("instagram_comment", comment_data)
                            
                            return comment_data
                        
                        elif field == "mentions":
                            # Nova menção
                            mention_data = {
                                "id": value.get("id"),
                                "media_id": value.get("media_id"),
                                "comment_id": value.get("comment_id"),
                                "timestamp": datetime.now().isoformat()
                            }
                            
                            self.send_to_n8n("instagram_mention", mention_data)
                            
                            return mention_data
            
            return None
            
        except Exception as e:
            st.error(f"Erro ao processar webhook do Instagram: {e}")
            return None
    
    def process_whatsapp_webhook(self, webhook_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Processa webhook recebido do WhatsApp"""
        try:
            if webhook_data.get("object") == "whatsapp_business_account":
                entries = webhook_data.get("entry", [])
                
                for entry in entries:
                    changes = entry.get("changes", [])
                    
                    for change in changes:
                        value = change.get("value", {})
                        messages = value.get("messages", [])
                        
                        for message in messages:
                            message_data = {
                                "id": message.get("id"),
                                "from": message.get("from"),
                                "timestamp": message.get("timestamp"),
                                "type": message.get("type"),
                                "text": message.get("text", {}).get("body") if message.get("type") == "text" else None
                            }
                            
                            # Enviar para N8N para processamento
                            self.send_to_n8n("whatsapp_message", message_data)
                            
                            return message_data
            
            return None
            
        except Exception as e:
            st.error(f"Erro ao processar webhook do WhatsApp: {e}")
            return None
    
    def send_whatsapp_message(self, phone_number: str, message: str) -> bool:
        """Envia mensagem via WhatsApp Business API"""
        whatsapp_token = st.secrets.get("WHATSAPP_TOKEN", "")
        phone_id = st.secrets.get("WHATSAPP_PHONE_ID", "")
        
        if not whatsapp_token or not phone_id:
            return False
        
        try:
            url = f"https://graph.facebook.com/v18.0/{phone_id}/messages"
            
            headers = {
                "Authorization": f"Bearer {whatsapp_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "type": "text",
                "text": {
                    "body": message
                }
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            return response.status_code == 200
            
        except Exception as e:
            st.error(f"Erro ao enviar mensagem WhatsApp: {e}")
            return False
    
    def send_bulk_whatsapp_messages(self, contacts: list, message_template: str) -> Dict[str, Any]:
        """Envia mensagens em massa via WhatsApp"""
        results = {
            "sent": 0,
            "failed": 0,
            "errors": []
        }
        
        for contact in contacts:
            phone = contact.get("telefone", "").replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
            name = contact.get("nome", "")
            
            # Personalizar mensagem
            personalized_message = message_template.replace("{nome}", name)
            
            if self.send_whatsapp_message(phone, personalized_message):
                results["sent"] += 1
            else:
                results["failed"] += 1
                results["errors"].append(f"Falha ao enviar para {name} ({phone})")
        
        return results
    
    def test_webhook_connection(self, webhook_url: str, auth_token: Optional[str] = None) -> Dict[str, Any]:
        """Testa conexão com webhook"""
        try:
            test_payload = {
                "test": True,
                "timestamp": datetime.now().isoformat(),
                "message": "Teste de conexão do Instagram Sales Dashboard"
            }
            
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Instagram-Sales-Dashboard/1.0"
            }
            
            if auth_token:
                headers["Authorization"] = f"Bearer {auth_token}"
            
            response = requests.post(
                webhook_url,
                json=test_payload,
                headers=headers,
                timeout=5
            )
            
            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "message": "Conexão estabelecida com sucesso!" if response.status_code == 200 else f"Erro: {response.status_code}"
            }
            
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "Timeout: Webhook não respondeu em 5 segundos"
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "Erro de conexão: Não foi possível conectar ao webhook"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro inesperado: {str(e)}"
            }
    
    def create_webhook_url(self, base_url: str, endpoint: str) -> str:
        """Cria URL completa do webhook"""
        if not base_url.endswith("/"):
            base_url += "/"
        
        if endpoint.startswith("/"):
            endpoint = endpoint[1:]
        
        return f"{base_url}{endpoint}"
    
    def get_webhook_status(self) -> Dict[str, Any]:
        """Retorna status de todos os webhooks configurados"""
        status = {
            "n8n": {
                "configured": bool(self.n8n_webhook_url),
                "url": self.n8n_webhook_url if self.n8n_webhook_url else "Não configurado",
                "auth": bool(self.n8n_auth_token)
            },
            "instagram": {
                "configured": bool(self.instagram_webhook_secret),
                "secret_set": bool(self.instagram_webhook_secret)
            },
            "whatsapp": {
                "configured": bool(self.whatsapp_webhook_secret),
                "secret_set": bool(self.whatsapp_webhook_secret)
            }
        }
        
        return status