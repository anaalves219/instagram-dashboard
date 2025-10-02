# 🪝 Configuração de Webhooks - Instagram Sales Dashboard

Este guia ensina como configurar webhooks do Instagram para criar leads automáticos quando alguém comenta ou envia DM com palavras-chave de interesse.

## 🎯 O que os Webhooks Fazem

### ✅ Funcionalidades Implementadas
- **🔥 Leads Quentes Automáticos**: Cria leads automaticamente quando detecta comentários com palavras como "quanto", "preço", "info"
- **💬 Notificações de DM**: Alerta quando alguém manda mensagem direta  
- **📢 Detecção de Menções**: Monitora quando você é mencionada em stories
- **🔔 Sistema de Alertas**: Notificações em tempo real no dashboard
- **📊 Estatísticas**: Acompanha quantos leads vieram de cada fonte

### 🎨 Palavras-Chave Detectadas
```python
# Palavras que ativam criação automática de lead:
["quanto", "preço", "valor", "info", "quero", "interessada", 
 "interessado", "como", "onde", "quando", "duvida", "dúvida", 
 "fale", "comigo", "dm", "direct"]
```

## 🛠️ Configuração no Meta for Developers

### 1. Criar Aplicação Facebook
1. Acesse [Facebook for Developers](https://developers.facebook.com)
2. Clique em **"Meus Apps"** → **"Criar App"**
3. Escolha **"Empresa"** como tipo de app
4. Preencha:
   - **Nome do App**: "Instagram Sales Dashboard"
   - **Email de Contato**: seu email
   - **Categoria**: Business

### 2. Configurar Instagram Basic Display
1. No painel do app, vá em **"Produtos"**
2. Encontre **"Instagram Basic Display"** e clique **"Configurar"**
3. Vá em **"Configurações Básicas"** do Instagram
4. Anote o **App ID** e **App Secret**

### 3. Configurar Webhooks
1. No menu esquerdo, clique em **"Webhooks"**
2. Clique **"Criar Assinatura"** para Instagram
3. Configure:

```
Callback URL: https://instagram-dashboard-8vfqbyyrmfbnpmsbl3mbts.streamlit.app/webhook/instagram
Verify Token: meu_token_secreto_123
```

4. Selecione os eventos:
   - ✅ **messages** (DMs)
   - ✅ **comments** (Comentários)  
   - ✅ **mentions** (Menções em stories)

5. Clique **"Verificar e Salvar"**

## ⚙️ Configuração no Streamlit Cloud

### 1. Adicionar Secrets
No seu app do Streamlit Cloud, vá em **Settings** → **Secrets** e adicione:

```toml
# ========== WEBHOOK CONFIGURATION ==========
INSTAGRAM_APP_SECRET = "seu-app-secret-do-facebook"
WEBHOOK_VERIFY_TOKEN = "meu_token_secreto_123"
WEBHOOK_AUTO_LEADS = "true"
WEBHOOK_NOTIFICATIONS = "true"

# ========== INSTAGRAM API ==========
INSTAGRAM_TOKEN = "seu-access-token-do-instagram"
INSTAGRAM_BUSINESS_ID = "seu-business-account-id"
INSTAGRAM_APP_ID = "seu-app-id-do-facebook"
```

### 2. Executar Schema SQL
No Supabase, execute o arquivo `webhook_schema.sql`:

1. Acesse [app.supabase.com](https://app.supabase.com)
2. Vá no seu projeto → **SQL Editor**
3. Cole o conteúdo completo de `webhook_schema.sql`
4. Clique **"Run"**

## 🧪 Testar o Webhook

### 1. No Dashboard
1. Acesse **Configurações** → **Webhooks**
2. Verifique se a URL está correta
3. Clique **"Testar Conexão"**
4. Deve aparecer: ✅ **Webhook funcionando!**

### 2. Teste Real
1. Faça um post no seu Instagram Business
2. Peça alguém para comentar "quanto custa?"
3. Em 1-2 segundos deve aparecer:
   - 🔥 Lead criado automaticamente na aba **Leads**
   - 🔔 Notificação no dashboard
   - 📊 Estatística atualizada

## 📊 Monitoramento

### Dashboard de Webhooks
Acesse **Configurações** → **Webhooks** para ver:

- **📈 Status**: Se está ativo/inativo
- **🔢 Eventos Recentes**: Últimos webhooks recebidos  
- **📋 Logs Detalhados**: JSON completo de cada evento
- **📊 Estatísticas**: Leads criados, comentários processados
- **🚨 Alertas**: Problemas ou delays

### Leads Automáticos
Na aba **Leads**, você verá:

```
🔥 LEAD QUENTE AUTOMÁTICO!
Nome: @usuario_instagram
Origem: Instagram - Comentário  
Nota: "Comentou: 'quanto custa esse curso?'"
Score: 9/10 (automático)
```

## 🔧 Troubleshooting

### ❌ Webhook Não Funciona
```bash
# Verifique no Streamlit Cloud:
1. Secrets configurados corretamente
2. App restarted após mudanças
3. URL do webhook sem typo

# Teste no Meta Developers:
1. Webhooks → Test → Enviar evento teste
2. Deve retornar status 200
```

### ❌ Leads Não São Criados
```python
# Verifique se:
1. WEBHOOK_AUTO_LEADS = "true" nos secrets
2. Tabela 'leads' existe no Supabase  
3. Palavras-chave estão corretas
4. Instagram Business Account conectado
```

### ❌ Notificações Não Aparecem  
```sql
-- Verifique no Supabase se tabela existe:
SELECT * FROM notificacoes ORDER BY created_at DESC LIMIT 5;

-- Se não existir, execute webhook_schema.sql
```

## 🚀 URLs Importantes

- **Webhook URL**: `https://instagram-dashboard-8vfqbyyrmfbnpmsbl3mbts.streamlit.app/webhook/instagram`
- **Meta Developers**: https://developers.facebook.com
- **Supabase**: https://app.supabase.com  
- **Streamlit Cloud**: https://share.streamlit.io

## 🔐 Segurança

### ✅ Implementado
- **Verificação de Assinatura**: Usa App Secret para validar
- **Verify Token**: Confirma origem do webhook
- **HTTPS Only**: Todas as comunicações criptografadas
- **Rate Limiting**: Proteção contra spam

### 🛡️ Boas Práticas
- Mantenha o **App Secret** privado
- Troque o **Verify Token** mensalmente
- Monitore logs de webhook regularmente
- Use tokens longos e complexos

## 📈 Resultados Esperados

Com webhooks configurados corretamente:

- **⚡ Resposta Instantânea**: Leads criados em < 2 segundos
- **🎯 Alta Conversão**: Capture 90%+ dos interessados
- **📊 Dados Precisos**: Tracking completo da origem
- **🤖 Automação Total**: Sem intervenção manual
- **💰 Mais Vendas**: Resposta rápida = mais conversões

---

**💡 Dica Pro**: Configure notificações no celular para ser alertada de leads quentes instantaneamente!

**🆘 Precisa de Ajuda?** Verifique os logs no dashboard ou entre em contato.