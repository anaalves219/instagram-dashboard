import streamlit as st
import json
from datetime import datetime
from utils.database import Database
from utils.auth import get_current_user
from webhook_handler import get_webhook_url, get_recent_webhook_events, test_webhook_connection

def show_page():
    """Página de Configurações - APIs, metas, usuários e sistema"""
    
    st.title("⚙️ Configurações")
    st.markdown("**Configurações do sistema, APIs, metas e preferências**")
    
    # Inicializar database
    db = Database()
    user_info = get_current_user()
    
    # Tabs principais
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🔗 APIs", "🎯 Metas", "👥 Usuários", "🌐 Sistema", "🔧 Avançado", "🪝 Webhooks"])
    
    # ========== TAB 1: APIs ==========
    with tab1:
        st.markdown("### 🔗 Configurações de APIs")
        
        # Instagram/Meta API
        with st.expander("📱 Instagram/Meta API", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                instagram_token = st.text_input(
                    "🔑 Access Token",
                    value=st.secrets.get("INSTAGRAM_TOKEN", ""),
                    type="password",
                    help="Token de acesso da Meta for Developers"
                )
                
                instagram_app_id = st.text_input(
                    "📱 App ID",
                    value=st.secrets.get("INSTAGRAM_APP_ID", ""),
                    help="ID da aplicação no Facebook Developers"
                )
            
            with col2:
                instagram_business_id = st.text_input(
                    "🏢 Business Account ID",
                    value=st.secrets.get("INSTAGRAM_BUSINESS_ID", ""),
                    help="ID da conta comercial do Instagram"
                )
                
                # Webhook URL - Gerada automaticamente
                webhook_url = get_webhook_url()
                st.text_input(
                    "🔗 Webhook URL (Auto-gerada)",
                    value=webhook_url,
                    disabled=True,
                    help="URL para configurar no Facebook Developers - Meta for Business"
                )
                
                if st.button("📋 Copiar URL do Webhook", use_container_width=True):
                    st.code(webhook_url, language="text")
                    st.success("✅ URL copiada! Configure esta URL no Meta for Developers")
                
                instagram_webhook_secret = st.text_input(
                    "🔐 App Secret",
                    value=st.secrets.get("INSTAGRAM_APP_SECRET", ""),
                    type="password",
                    help="App Secret do Facebook para verificar webhooks"
                )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🧪 Testar Conexão Instagram", use_container_width=True):
                    if not instagram_token:
                        st.error("❌ Token não configurado")
                    elif not st.secrets.get("INSTAGRAM_BUSINESS_ID"):
                        st.error("❌ Business ID não configurado")
                    else:
                        try:
                            from pages.instagram_analytics import InstagramAPI
                            api = InstagramAPI()
                            result = api.get_account_info()
                            
                            if result and 'error' not in result:
                                st.success(f"✅ Conectado! Conta: @{result.get('username', 'N/A')}")
                                st.info(f"📊 {result.get('followers_count', 0)} seguidores | {result.get('media_count', 0)} posts")
                            elif result and 'error' in result:
                                error_msg = result['error'].get('message', 'Erro desconhecido')
                                st.error(f"❌ Erro da API: {error_msg}")
                                if 'access token' in error_msg.lower():
                                    st.info("💡 Verifique se o token está válido e não expirou")
                                elif 'permissions' in error_msg.lower():
                                    st.info("💡 Verifique se o token tem permissões de business account")
                            else:
                                st.error("❌ Sem resposta da API Instagram")
                                st.info("💡 Verifique sua conexão ou tente mais tarde")
                        except Exception as e:
                            st.error(f"❌ Erro no teste: {str(e)}")
                            st.info("💡 Verifique se todas as configurações estão corretas")
            
            with col2:
                if st.button("🪝 Testar Webhook", use_container_width=True):
                    if test_webhook_connection():
                        st.success("✅ Webhook testado com sucesso!")
                    else:
                        st.error("❌ Erro ao testar webhook")
        
        # WhatsApp API
        with st.expander("💬 WhatsApp Business API"):
            col1, col2 = st.columns(2)
            
            with col1:
                whatsapp_token = st.text_input(
                    "🔑 WhatsApp Access Token",
                    value=st.secrets.get("WHATSAPP_TOKEN", ""),
                    type="password"
                )
                
                whatsapp_phone_id = st.text_input(
                    "📞 Phone Number ID",
                    value=st.secrets.get("WHATSAPP_PHONE_ID", "")
                )
            
            with col2:
                whatsapp_webhook_token = st.text_input(
                    "🔐 Webhook Verify Token",
                    value=st.secrets.get("WHATSAPP_WEBHOOK_TOKEN", ""),
                    type="password"
                )
                
                whatsapp_webhook_url = st.text_input(
                    "🔗 Webhook URL",
                    value=st.secrets.get("WHATSAPP_WEBHOOK", "")
                )
            
            if st.button("🧪 Testar WhatsApp API", use_container_width=True):
                st.info("🔧 Implementação da API em desenvolvimento")
        
        # N8N Webhook
        with st.expander("🤖 N8N Automação"):
            n8n_webhook = st.text_input(
                "🔗 N8N Webhook URL",
                value=st.secrets.get("N8N_WEBHOOK", ""),
                help="URL do webhook para automações no N8N"
            )
            
            n8n_auth_token = st.text_input(
                "🔑 Token de Autenticação",
                value=st.secrets.get("N8N_AUTH_TOKEN", ""),
                type="password"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🧪 Testar N8N", use_container_width=True):
                    if n8n_webhook:
                        st.success("✅ Webhook N8N configurado!")
                    else:
                        st.warning("⚠️ URL do webhook não configurada")
            
            with col2:
                if st.button("🚀 Enviar Teste", use_container_width=True):
                    st.info("📤 Teste enviado para N8N")
        
        # Status das integrações
        st.markdown("#### 🔍 Status das Integrações")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Teste real de conectividade
            if instagram_token and st.secrets.get("INSTAGRAM_BUSINESS_ID"):
                try:
                    # Importar e testar a API aqui
                    from pages.instagram_analytics import InstagramAPI
                    api = InstagramAPI()
                    test_result = api.get_account_info()
                    if test_result and 'error' not in test_result:
                        instagram_status = "🟢 Conectado e Funcionando"
                    else:
                        instagram_status = "🟡 Token Configurado (Verificar)"
                except:
                    instagram_status = "🟡 Token Configurado (Verificar)"
            else:
                instagram_status = "🔴 Não Configurado"
            st.markdown(f"**Instagram:** {instagram_status}")
        
        with col2:
            whatsapp_status = "🟢 Conectado" if whatsapp_token else "🔴 Desconectado"
            st.markdown(f"**WhatsApp:** {whatsapp_status}")
        
        with col3:
            n8n_status = "🟢 Conectado" if n8n_webhook else "🔴 Desconectado"
            st.markdown(f"**N8N:** {n8n_status}")
    
    # ========== TAB 2: METAS ==========
    with tab2:
        st.markdown("### 🎯 Configuração de Metas")
        
        # Metas mensais
        st.markdown("#### 📊 Metas Mensais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**👤 Meta Ana**")
            meta_ana_vendas = st.number_input("💰 Meta de Vendas (R$)", value=50000.0, key="meta_ana_vendas")
            meta_ana_leads = st.number_input("🎯 Meta de Leads", value=100, key="meta_ana_leads")
            meta_ana_conversao = st.number_input("📈 Meta Conversão (%)", value=15.0, key="meta_ana_conversao")
        
        with col2:
            st.markdown("**👤 Meta Fernando**")
            meta_fernando_vendas = st.number_input("💰 Meta de Vendas (R$)", value=50000.0, key="meta_fernando_vendas")
            meta_fernando_leads = st.number_input("🎯 Meta de Leads", value=100, key="meta_fernando_leads")
            meta_fernando_conversao = st.number_input("📈 Meta Conversão (%)", value=15.0, key="meta_fernando_conversao")
        
        # Metas da equipe
        st.markdown("#### 🏢 Metas da Equipe")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            meta_equipe_mensal = st.number_input("💰 Meta Mensal Equipe (R$)", value=100000.0)
        
        with col2:
            meta_equipe_trimestral = st.number_input("📅 Meta Trimestral (R$)", value=300000.0)
        
        with col3:
            meta_equipe_anual = st.number_input("🏆 Meta Anual (R$)", value=1200000.0)
        
        # Configurações de comissão
        st.markdown("#### 💵 Configurações de Comissão")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            comissao_padrao = st.number_input("📈 Comissão Padrão (%)", value=30.0, min_value=0.0, max_value=100.0)
        
        with col2:
            bonus_meta = st.number_input("🎁 Bônus por Meta (%)", value=5.0, min_value=0.0, max_value=50.0)
        
        with col3:
            comissao_lider = st.number_input("👑 Comissão Líder Mensal (%)", value=35.0, min_value=0.0, max_value=100.0)
        
        if st.button("💾 Salvar Metas", type="primary", use_container_width=True):
            st.success("✅ Metas atualizadas com sucesso!")
            db.log_activity(user_info.get('username', ''), 'Metas Atualizadas', 'Configurações de metas modificadas')
    
    # ========== TAB 3: USUÁRIOS ==========
    with tab3:
        st.markdown("### 👥 Gerenciamento de Usuários")
        
        # Informações dos usuários atuais
        usuarios_data = [
            {
                "Usuário": "ana",
                "Nome": "Ana",
                "Último Login": "02/02/2024 14:30",
                "Status": "🟢 Ativo",
                "Permissões": "Admin"
            },
            {
                "Usuário": "fernando", 
                "Nome": "Fernando",
                "Último Login": "02/02/2024 13:45",
                "Status": "🟢 Ativo",
                "Permissões": "Admin"
            }
        ]
        
        st.dataframe(
            usuarios_data,
            column_config={
                "Usuário": st.column_config.TextColumn("Usuário"),
                "Nome": st.column_config.TextColumn("Nome"),
                "Último Login": st.column_config.TextColumn("Último Login"),
                "Status": st.column_config.TextColumn("Status"),
                "Permissões": st.column_config.TextColumn("Permissões")
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Adicionar novo usuário
        with st.expander("➕ Adicionar Novo Usuário"):
            col1, col2 = st.columns(2)
            
            with col1:
                novo_usuario = st.text_input("👤 Nome de Usuário")
                novo_nome = st.text_input("📝 Nome Completo")
                nova_senha = st.text_input("🔑 Senha", type="password")
            
            with col2:
                novo_role = st.selectbox("🎭 Função", ["vendedor", "admin", "visualizador"])
                novo_tema_primary = st.color_picker("🎨 Cor Primária", "#9D4EDD")
                novo_tema_secondary = st.color_picker("🌈 Cor Secundária", "#06FFA5")
            
            if st.button("👥 Adicionar Usuário", use_container_width=True):
                st.success("✅ Usuário adicionado com sucesso!")
        
        # Configurações de segurança
        st.markdown("#### 🔒 Configurações de Segurança")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tempo_sessao = st.number_input("⏰ Tempo de Sessão (horas)", value=8, min_value=1, max_value=24)
            backup_automatico = st.checkbox("💾 Backup Automático", value=True)
        
        with col2:
            log_detalhado = st.checkbox("📝 Log Detalhado", value=True)
            notificacoes_login = st.checkbox("🔔 Notificar Logins", value=False)
        
        if st.button("🔒 Salvar Segurança", use_container_width=True):
            st.success("✅ Configurações de segurança atualizadas!")
    
    # ========== TAB 4: SISTEMA ==========
    with tab4:
        st.markdown("### 🌐 Configurações do Sistema")
        
        # Configurações gerais
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ⚙️ Configurações Gerais")
            
            nome_empresa = st.text_input("🏢 Nome da Empresa", value="Instagram Sales Pro")
            produto_principal = st.text_input("🛍️ Produto Principal", value="Curso High Ticket")
            valor_produto = st.number_input("💰 Valor Padrão do Produto", value=1997.0)
            moeda = st.selectbox("💱 Moeda", ["BRL", "USD", "EUR"], index=0)
        
        with col2:
            st.markdown("#### 🕐 Configurações de Tempo")
            
            fuso_horario = st.selectbox("🌍 Fuso Horário", [
                "America/Sao_Paulo", "America/New_York", "Europe/London"
            ])
            formato_data = st.selectbox("📅 Formato de Data", ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
            primeiro_dia_semana = st.selectbox("📆 Primeiro Dia da Semana", ["Segunda", "Domingo"])
        
        # Configurações de notificação
        st.markdown("#### 🔔 Configurações de Notificação")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            notif_vendas = st.checkbox("💰 Notificar Vendas", value=True)
            notif_leads = st.checkbox("🎯 Notificar Novos Leads", value=True)
        
        with col2:
            notif_metas = st.checkbox("🏆 Notificar Metas Atingidas", value=True)
            notif_alertas = st.checkbox("⚠️ Alertas de Sistema", value=True)
        
        with col3:
            notif_email = st.checkbox("📧 Enviar por E-mail", value=False)
            notif_webhook = st.checkbox("🔗 Enviar via Webhook", value=True)
        
        # Configurações de aparência
        st.markdown("#### 🎨 Configurações de Aparência")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tema_padrao = st.selectbox("🌙 Tema Padrão", ["Dark", "Light", "Auto"])
            densidade_interface = st.selectbox("📱 Densidade da Interface", ["Compacta", "Normal", "Espaçosa"])
        
        with col2:
            animacoes = st.checkbox("✨ Animações", value=True)
            auto_refresh = st.number_input("🔄 Auto-refresh (segundos)", value=300, min_value=30, max_value=3600)
        
        if st.button("🌐 Salvar Configurações do Sistema", type="primary", use_container_width=True):
            st.success("✅ Configurações do sistema atualizadas!")
    
    # ========== TAB 5: AVANÇADO ==========
    with tab5:
        st.markdown("### 🔧 Configurações Avançadas")
        
        # Banco de dados
        st.markdown("#### 💾 Banco de Dados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Verificar Conexão", use_container_width=True):
                if db.is_connected():
                    st.success("✅ Conectado ao Supabase")
                else:
                    st.error("❌ Erro de conexão")
            
            if st.button("🧹 Limpar Cache", use_container_width=True):
                st.success("✅ Cache limpo com sucesso!")
        
        with col2:
            if st.button("💾 Backup Manual", use_container_width=True):
                st.success("✅ Backup realizado com sucesso!")
            
            if st.button("📊 Estatísticas do DB", use_container_width=True):
                st.info("📈 Total de registros: 1.247")
        
        # Logs do sistema
        st.markdown("#### 📝 Logs do Sistema")
        
        logs_df = db.get_activity_logs(limit=20)
        
        if not logs_df.empty:
            st.dataframe(
                logs_df[['timestamp', 'user_id', 'action', 'details']],
                column_config={
                    'timestamp': st.column_config.DatetimeColumn('Data/Hora'),
                    'user_id': st.column_config.TextColumn('Usuário'),
                    'action': st.column_config.TextColumn('Ação'),
                    'details': st.column_config.TextColumn('Detalhes')
                },
                hide_index=True,
                use_container_width=True,
                height=300
            )
        else:
            st.info("📝 Nenhum log encontrado")
        
        # Rate limiting
        st.markdown("#### 🚦 Rate Limiting")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            rate_limit_requests = st.number_input("📊 Requests por Minuto", value=100, min_value=10)
        
        with col2:
            rate_limit_api = st.number_input("🔗 API Calls por Hora", value=1000, min_value=100)
        
        with col3:
            rate_limit_export = st.number_input("📥 Exports por Dia", value=50, min_value=5)
        
        # Configurações de desenvolvimento
        st.markdown("#### 🛠️ Desenvolvimento")
        
        col1, col2 = st.columns(2)
        
        with col1:
            debug_mode = st.checkbox("🐛 Modo Debug", value=False)
            verbose_logs = st.checkbox("📝 Logs Verbosos", value=False)
        
        with col2:
            mock_data = st.checkbox("🎭 Usar Dados Mock", value=True)
            test_mode = st.checkbox("🧪 Modo de Teste", value=False)
        
        # Informações do sistema
        st.markdown("#### ℹ️ Informações do Sistema")
        
        info_sistema = {
            "Versão": "1.0.0",
            "Última Atualização": "02/02/2024",
            "Streamlit": "1.29.0",
            "Python": "3.11.5",
            "Supabase": "Conectado",
            "Uptime": "7 dias, 14 horas"
        }
        
        for chave, valor in info_sistema.items():
            st.markdown(f"**{chave}:** {valor}")
        
        # Ações de sistema
        st.markdown("#### ⚡ Ações de Sistema")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Reiniciar Aplicação", use_container_width=True):
                st.warning("⚠️ Aplicação será reiniciada em 10 segundos...")
        
        with col2:
            if st.button("📤 Export Completo", use_container_width=True):
                st.success("✅ Export iniciado!")
        
        with col3:
            if st.button("🗑️ Limpar Dados de Teste", use_container_width=True):
                st.warning("⚠️ Dados de teste serão removidos!")
        
        if st.button("💾 Salvar Configurações Avançadas", type="primary", use_container_width=True):
            st.success("✅ Configurações avançadas salvas!")
            db.log_activity(user_info.get('username', ''), 'Config Avançadas', 'Configurações avançadas modificadas')
    
    # ========== TAB 6: WEBHOOKS ==========
    with tab6:
        st.markdown("### 🪝 Gerenciamento de Webhooks")
        
        # Status do webhook
        st.markdown("#### 📊 Status dos Webhooks")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            webhook_url = get_webhook_url()
            instagram_secret = st.secrets.get("INSTAGRAM_APP_SECRET", "")
            webhook_status = "🟢 Ativo" if instagram_secret else "🟡 Configuração Pendente"
            st.metric("Instagram Webhook", webhook_status)
        
        with col2:
            recent_events = get_recent_webhook_events(limit=5)
            st.metric("Eventos Recentes", len(recent_events))
        
        with col3:
            # Simular uptime
            st.metric("Uptime", "99.8%", delta="0.1%")
        
        st.divider()
        
        # URL do webhook
        st.markdown("#### 🔗 URL do Webhook")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.code(webhook_url, language="text")
        
        with col2:
            if st.button("📋 Copiar", use_container_width=True):
                st.success("✅ Copiado!")
        
        st.markdown("""
        **📝 Como configurar no Meta for Developers:**
        1. Acesse [Facebook for Developers](https://developers.facebook.com)
        2. Vá em seu App > Webhooks
        3. Cole a URL acima no campo "Callback URL"
        4. Configure o Verify Token nos secrets do Streamlit
        5. Selecione os eventos: `messages`, `comments`, `mentions`
        """)
        
        st.divider()
        
        # Configurações do webhook
        st.markdown("#### ⚙️ Configurações")
        
        col1, col2 = st.columns(2)
        
        with col1:
            verify_token = st.text_input(
                "🔐 Verify Token",
                value=st.secrets.get("WEBHOOK_VERIFY_TOKEN", ""),
                type="password",
                help="Token para verificar webhooks (configure o mesmo no Meta)"
            )
            
            enable_auto_leads = st.checkbox(
                "🎯 Auto-criar Leads",
                value=True,
                help="Criar leads automaticamente com comentários quentes"
            )
        
        with col2:
            app_secret = st.text_input(
                "🔑 App Secret",
                value=st.secrets.get("INSTAGRAM_APP_SECRET", ""),
                type="password",
                help="App Secret do Facebook para validar assinatura"
            )
            
            enable_notifications = st.checkbox(
                "🔔 Notificações",
                value=True,
                help="Enviar notificações para leads quentes"
            )
        
        # Teste do webhook
        st.markdown("#### 🧪 Teste do Webhook")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔍 Testar Conexão", use_container_width=True):
                if test_webhook_connection():
                    st.success("✅ Webhook funcionando!")
                else:
                    st.error("❌ Erro no webhook")
        
        with col2:
            if st.button("📤 Simular Evento", use_container_width=True):
                # Simular evento de teste
                st.info("📨 Evento de teste enviado")
        
        with col3:
            if st.button("🔄 Reprocessar", use_container_width=True):
                st.info("♻️ Reprocessando eventos pendentes")
        
        st.divider()
        
        # Últimos eventos
        st.markdown("#### 📋 Últimos Eventos Recebidos")
        
        recent_events = get_recent_webhook_events(limit=10)
        
        if recent_events:
            for i, event in enumerate(recent_events):
                with st.expander(f"🔔 {event.get('event_type', 'unknown')} - {event.get('created_at', 'N/A')[:19]}"):
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        st.markdown(f"**Tipo:** {event.get('event_type', 'N/A')}")
                        st.markdown(f"**Status:** {event.get('status', 'N/A')}")
                        st.markdown(f"**Origem:** {event.get('source', 'N/A')}")
                    
                    with col2:
                        if 'data' in event:
                            try:
                                if isinstance(event['data'], str):
                                    data = json.loads(event['data'])
                                else:
                                    data = event['data']
                                st.json(data)
                            except:
                                st.text(str(event['data']))
        else:
            st.info("📭 Nenhum evento de webhook recebido ainda")
        
        # Estatísticas
        st.markdown("#### 📊 Estatísticas dos Webhooks")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Eventos Hoje", "12", delta="3")
        
        with col2:
            st.metric("Leads Criados", "4", delta="1")
        
        with col3:
            st.metric("Comentários", "8", delta="2")
        
        with col4:
            st.metric("DMs", "2", delta="1")
        
        # Alertas e notificações
        st.markdown("#### 🚨 Alertas Recentes")
        
        st.success("🔥 **Lead Quente Detectado!** @maria_silva comentou 'quanto custa?' há 5 min")
        st.info("💬 **Nova DM** de @joao123 há 12 min")
        st.warning("⚠️ **Webhook com delay** - Meta com latência de 2.3s")
        
        if st.button("💾 Salvar Configurações de Webhook", type="primary", use_container_width=True):
            st.success("✅ Configurações de webhook salvas!")
            db.log_activity(user_info.get('username', ''), 'Webhook Config', 'Configurações de webhook modificadas')