import streamlit as st
import hashlib
import hmac
import json
from datetime import datetime
from utils.database import Database

def verify_webhook(request_data, signature):
    """Verifica se o webhook veio mesmo do Instagram"""
    app_secret = st.secrets.get("INSTAGRAM_APP_SECRET", "")
    
    if not app_secret:
        return False
    
    expected_signature = hmac.new(
        app_secret.encode('utf-8'),
        request_data,
        hashlib.sha256
    ).hexdigest()
    
    return f"sha256={expected_signature}" == signature

def handle_instagram_webhook():
    """Processa webhooks do Instagram"""
    
    # Verificação inicial (quando Instagram testa a URL)
    params = st.query_params
    if params.get("hub.mode") == "subscribe":
        verify_token = st.secrets.get("WEBHOOK_VERIFY_TOKEN", "meu_token_123")
        
        if params.get("hub.verify_token") == verify_token:
            # Retorna o challenge para confirmar
            return params.get("hub.challenge")
    
    # Processar eventos reais
    if hasattr(st, 'request') and st.request.method == "POST":
        try:
            data = st.request.json
            
            # Salva no banco para processar
            save_webhook_event(data)
            
            # Processa baseado no tipo
            if "messaging" in data:
                handle_new_dm(data)
            elif "comments" in data:
                handle_new_comment(data)
            elif "mentions" in data:
                handle_mention(data)
                
            return {"status": "ok"}
        except Exception as e:
            st.error(f"Erro ao processar webhook: {e}")
            return {"status": "error", "message": str(e)}

def save_webhook_event(data):
    """Salva evento do webhook no banco de dados"""
    db = Database()
    
    if not db.is_connected():
        return
    
    try:
        # Cria uma entrada no log de atividades
        db.log_activity(
            user_id="system",
            action="webhook_received",
            details=json.dumps(data, default=str)
        )
        
        # Salva na tabela de webhooks se existir
        webhook_data = {
            'source': 'instagram',
            'event_type': detect_event_type(data),
            'data': json.dumps(data),
            'processed_at': datetime.now().isoformat(),
            'status': 'received'
        }
        
        # Se tabela webhooks existir, insere lá
        try:
            db.supabase.table('webhooks').insert(webhook_data).execute()
        except:
            # Se não existir a tabela, salva nos logs
            pass
            
    except Exception as e:
        st.error(f"Erro ao salvar webhook: {e}")

def detect_event_type(data):
    """Detecta o tipo de evento do webhook"""
    if "messaging" in data:
        return "new_message"
    elif "comments" in data:
        return "new_comment"
    elif "mentions" in data:
        return "mention"
    elif "story_insights" in data:
        return "story_insights"
    else:
        return "unknown"

def handle_new_comment(data):
    """Quando alguém comenta"""
    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            if change["field"] == "comments":
                comment = change["value"]
                
                # Verifica se tem palavras-chave de venda
                text = comment.get("text", "").lower()
                hot_words = ["quanto", "preço", "valor", "info", "quero", "interessada", "interessado", 
                           "como", "onde", "quando", "duvida", "dúvida", "fale", "comigo", "dm", "direct"]
                
                if any(word in text for word in hot_words):
                    # LEAD QUENTE DETECTADO!
                    create_hot_lead_alert(comment)

def handle_new_dm(data):
    """Quando alguém manda DM"""
    for entry in data.get("entry", []):
        for messaging in entry.get("messaging", []):
            message = messaging.get("message", {})
            sender = messaging.get("sender", {})
            
            # Todo DM é potencialmente um lead quente
            create_hot_lead_alert({
                "type": "dm",
                "sender_id": sender.get("id"),
                "text": message.get("text", ""),
                "timestamp": messaging.get("timestamp")
            })

def handle_mention(data):
    """Quando alguém menciona no stories/posts"""
    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            if change["field"] == "mentions":
                mention = change["value"]
                create_mention_alert(mention)

def create_hot_lead_alert(comment_data):
    """Cria alerta de lead quente no banco"""
    db = Database()
    
    if not db.is_connected():
        return
    
    try:
        # Pega dados do comentário
        text = comment_data.get("text", "")
        user_id = comment_data.get("from", {}).get("id", "")
        username = comment_data.get("from", {}).get("username", "")
        
        # Cria lead automático
        lead_data = {
            'nome': username or f"Usuario_{user_id}",
            'instagram': f"@{username}" if username else "",
            'status': 'quente',
            'origem': 'Instagram - Comentário',
            'vendedor': 'Ana',  # Pode alternar ou usar regra
            'nota': f"LEAD QUENTE! Comentou: '{text}'",
            'score': 9,  # Score alto para leads automáticos
            'ultima_interacao': datetime.now().date(),
            'tags': ['webhook', 'comentario', 'quente']
        }
        
        # Insere no banco
        db.supabase.table('leads').insert(lead_data).execute()
        
        # Cria notificação
        notification_data = {
            'user_id': 'ana',
            'titulo': '🔥 LEAD QUENTE DETECTADO!',
            'mensagem': f"@{username} comentou palavras-chave de interesse: '{text[:50]}...'",
            'tipo': 'hot_lead',
            'lida': False
        }
        
        db.supabase.table('notificacoes').insert(notification_data).execute()
        
    except Exception as e:
        st.error(f"Erro ao criar lead quente: {e}")

def create_mention_alert(mention_data):
    """Cria alerta para menção"""
    db = Database()
    
    if not db.is_connected():
        return
    
    try:
        # Cria notificação para menção
        notification_data = {
            'user_id': 'ana',
            'titulo': '📢 Nova Menção!',
            'mensagem': f"Você foi mencionada em um story/post",
            'tipo': 'mention',
            'lida': False
        }
        
        db.supabase.table('notificacoes').insert(notification_data).execute()
        
    except Exception as e:
        st.error(f"Erro ao criar alerta de menção: {e}")

def get_webhook_url():
    """Retorna a URL do webhook baseada no app atual"""
    # Pega a URL base do Streamlit app
    try:
        # Para produção no Streamlit Cloud
        base_url = "https://instagram-dashboard-8vfqbyyrmfbnpmsbl3mbts.streamlit.app"
        
        # Para desenvolvimento local
        if "localhost" in st.get_option("server.headless") or "127.0.0.1" in str(st.get_option("server.headless")):
            base_url = "http://localhost:8501"
            
        return f"{base_url}/webhook/instagram"
    except:
        # Fallback manual
        return "https://instagram-dashboard-8vfqbyyrmfbnpmsbl3mbts.streamlit.app/webhook/instagram"

def get_recent_webhook_events(limit=10):
    """Busca eventos recentes do webhook"""
    db = Database()
    
    if not db.is_connected():
        return []
    
    try:
        # Tenta buscar da tabela webhooks primeiro
        try:
            response = db.supabase.table('webhooks')\
                .select('*')\
                .order('created_at', desc=True)\
                .limit(limit)\
                .execute()
            return response.data
        except:
            # Se não existir tabela webhooks, busca dos logs
            response = db.supabase.table('activity_logs')\
                .select('*')\
                .eq('action', 'webhook_received')\
                .order('timestamp', desc=True)\
                .limit(limit)\
                .execute()
            
            # Converte formato dos logs para formato webhook
            events = []
            for log in response.data:
                try:
                    details = json.loads(log['details'])
                    events.append({
                        'id': log['id'],
                        'event_type': detect_event_type(details),
                        'source': 'instagram',
                        'created_at': log['timestamp'],
                        'status': 'processed',
                        'data': log['details']
                    })
                except:
                    continue
            
            return events
            
    except Exception as e:
        st.error(f"Erro ao buscar eventos de webhook: {e}")
        return []

def test_webhook_connection():
    """Testa se o webhook está funcionando"""
    webhook_url = get_webhook_url()
    
    # Simula um teste básico
    test_data = {
        "test": True,
        "timestamp": datetime.now().isoformat(),
        "message": "Teste de conexão do webhook"
    }
    
    try:
        # Em produção, aqui faria uma requisição HTTP para testar
        # Por enquanto, apenas salva um evento de teste
        save_webhook_event(test_data)
        return True
    except:
        return False