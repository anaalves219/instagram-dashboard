# 🚀 Instagram Sales Dashboard

Dashboard completo para gerenciamento de vendas high ticket no Instagram, desenvolvido para 2 sócios (Ana e Fernando) com deploy GRATUITO no Streamlit Cloud.

## 📋 Funcionalidades

### 🔐 Sistema de Autenticação
- Login seguro para 2 usuários (Ana e Fernando)
- Senhas criptografadas com hash SHA-256
- Temas personalizados por usuário
- Controle de sessão e logout automático

### 📊 Dashboard Overview
- Métricas em tempo real de vendas e faturamento
- Comparativo de performance entre vendedores
- Alertas e notificações importantes
- Progress das metas mensais
- Últimas atividades do sistema

### 💰 Gestão de Vendas
- CRUD completo de vendas
- Cálculo automático de comissões (30%)
- Histórico detalhado com filtros
- Export de relatórios (CSV/Excel/PDF)
- Acompanhamento de status (confirmada/pendente/cancelada)

### 🎯 Pipeline de Leads
- Gestão completa do funil de vendas
- Sistema de scoring (1-10)
- Follow-up automático de leads "frios"
- Pipeline visual com conversões
- Tags e categorização de leads

### ⚔️ Batalha dos Vendedores
- Competição saudável entre Ana e Fernando
- Comparativo em tempo real
- Rankings históricos
- Sistema de metas e desafios
- Badges e conquistas

### 💳 Análise Financeira
- Cálculo automático de ROI
- Controle de custos por categoria
- Projeções financeiras (conservador/realista/otimista)
- Fluxo de caixa com projeções
- DRE automático

### ⚙️ Configurações
- Integração com APIs do Meta (Instagram/WhatsApp)
- Webhooks para automação (N8N)
- Configuração de metas e comissões
- Gerenciamento de usuários
- Logs detalhados do sistema

## 🛠️ Tecnologias Utilizadas

- **Frontend**: Streamlit 1.29.0
- **Backend**: Python 3.11+
- **Banco de Dados**: Supabase (PostgreSQL gratuito)
- **Gráficos**: Plotly Express
- **Autenticação**: Hash SHA-256 + Sessions
- **Deploy**: Streamlit Cloud (GRATUITO)
- **APIs**: Meta Business (Instagram/WhatsApp)

## 🚀 Deploy Rápido (5 minutos)

### 1. Preparar o Repositório

```bash
# Clone ou faça download dos arquivos
git clone <seu-repositorio>
cd instagram-dashboard
```

### 2. Configurar Supabase

1. Acesse [supabase.com](https://supabase.com) e crie uma conta gratuita
2. Crie um novo projeto
3. No SQL Editor, execute o arquivo `schema.sql` completo
4. Anote a **URL** e **ANON KEY** do projeto

### 3. Deploy no Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Conecte sua conta GitHub
3. Clique em "New app"
4. Selecione o repositório `instagram-dashboard`
5. Main file path: `app.py`
6. Clique em "Deploy!"

### 4. Configurar Secrets

No Streamlit Cloud, vá em **Settings > Secrets** e adicione:

```toml
[secrets]
# Supabase Configuration
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "your-anon-key-here"

# Instagram/Meta API (opcional)
INSTAGRAM_TOKEN = "your-instagram-token"
INSTAGRAM_APP_ID = "your-app-id"
INSTAGRAM_BUSINESS_ID = "your-business-id"
INSTAGRAM_WEBHOOK = "your-webhook-url"
INSTAGRAM_WEBHOOK_SECRET = "your-webhook-secret"

# WhatsApp API (opcional)
WHATSAPP_TOKEN = "your-whatsapp-token"
WHATSAPP_PHONE_ID = "your-phone-id"
WHATSAPP_WEBHOOK_TOKEN = "your-webhook-token"
WHATSAPP_WEBHOOK = "your-webhook-url"
WHATSAPP_WEBHOOK_SECRET = "your-webhook-secret"

# N8N Automation (opcional)
N8N_WEBHOOK = "your-n8n-webhook-url"
N8N_AUTH_TOKEN = "your-n8n-auth-token"
```

### 5. Testar o Sistema

1. Acesse a URL do seu app no Streamlit Cloud
2. Use as credenciais de teste:
   - **Ana**: usuário `ana` | senha `ana2024`
   - **Fernando**: usuário `fernando` | senha `fernando2024`

## 🔧 Configuração Local (Desenvolvimento)

### Pré-requisitos
- Python 3.11+
- Git

### Instalação

```bash
# Clone o repositório
git clone <seu-repositorio>
cd instagram-dashboard

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# Execute a aplicação
streamlit run app.py
```

### Estrutura do Projeto

```
instagram-dashboard/
├── app.py                 # Aplicação principal
├── requirements.txt       # Dependências Python
├── schema.sql            # Schema do banco Supabase
├── README.md             # Este arquivo
├── 
├── pages/                # Páginas do dashboard
│   ├── __init__.py
│   ├── overview.py       # Dashboard principal
│   ├── vendas.py         # Gestão de vendas
│   ├── leads.py          # Pipeline de leads
│   ├── batalha.py        # Comparativo vendedores
│   ├── financeiro.py     # Análise financeira
│   └── config.py         # Configurações
├── 
├── utils/                # Utilitários
│   ├── __init__.py
│   ├── auth.py           # Sistema de autenticação
│   ├── database.py       # Conexão com Supabase
│   ├── styles.py         # CSS customizado
│   ├── exports.py        # Sistema de exports
│   └── webhooks.py       # Gerenciador de webhooks
└── 
└── data/                 # Dados de exemplo
    └── sample_data.py    # Gerador de dados
```

## 📊 Dados de Exemplo

O sistema inclui dados de exemplo para demonstração:

```bash
# Gerar dados de exemplo
python data/sample_data.py
```

Isto criará:
- **100 vendas** com faturamento de ~R$ 190k
- **200 leads** com score médio 6.2
- **50 custos** totalizando ~R$ 170k
- **100 logs** de atividades

## 🔐 Credenciais Padrão

### Usuários do Sistema
- **Ana**: `ana` / `ana2024`
- **Fernando**: `fernando` / `fernando2024`

### Temas Personalizados
- **Ana**: Roxo (#9D4EDD) + Verde (#06FFA5)
- **Fernando**: Azul (#0EA5E9) + Laranja (#F97316)

## 🔗 Integrações

### Instagram Business API
1. Crie um app no [Facebook Developers](https://developers.facebook.com)
2. Configure o Instagram Basic Display ou Instagram Business
3. Adicione as credenciais no `secrets.toml`

### WhatsApp Business API
1. Configure no [Meta Business](https://business.facebook.com)
2. Obtenha o Phone Number ID e Access Token
3. Configure os webhooks para notificações

### N8N Automação
1. Configure um workflow no N8N
2. Crie um webhook endpoint
3. Use para automações como:
   - Notificar vendas no Slack/Discord
   - Enviar relatórios por email
   - Integrar com CRM
   - Backup automático

## 📱 Mobile Responsive

O dashboard é totalmente responsivo e funciona perfeitamente em:
- 📱 Smartphones (iOS/Android)
- 📱 Tablets
- 💻 Desktops
- 🖥️ Monitores ultrawide

## 🔒 Segurança

### Implementado
- ✅ Autenticação com hash SHA-256
- ✅ Controle de sessão
- ✅ Secrets via Streamlit Cloud
- ✅ Rate limiting (configurável)
- ✅ Logs de auditoria
- ✅ HTTPS only (Streamlit Cloud)

### Recomendações Adicionais
- 🔄 Backup diário automático
- 🔐 Rotação de senhas mensal
- 🚨 Monitoramento de tentativas de login
- 📧 Alertas de segurança

## 📈 Métricas e KPIs

### Vendas
- Faturamento total e por vendedor
- Ticket médio
- Taxa de conversão
- Comissões calculadas
- Metas vs realizado

### Leads
- Funil de conversão completo
- Score médio dos leads
- Tempo médio de conversão
- Follow-up necessário
- ROI por canal

### Financeiro
- ROI calculado automaticamente
- Margem de lucro
- Custos por categoria
- Projeções baseadas em histórico
- Fluxo de caixa

## 🛠️ Personalização

### Alternar Usuários
Edite `utils/auth.py` para adicionar novos usuários:

```python
USERS = {
    "novo_usuario": {
        "password_hash": "hash_da_senha",
        "name": "Nome Completo",
        "role": "vendedor",
        "theme": {"primary": "#CODIGO", "secondary": "#CODIGO"}
    }
}
```

### Personalizar Cores
Edite `utils/styles.py` para alterar o tema visual.

### Adicionar Páginas
1. Crie um novo arquivo em `pages/`
2. Implemente a função `show_page()`
3. Adicione ao menu em `app.py`

## 🚨 Troubleshooting

### Erro de Conexão com Supabase
```
❌ Supabase configuration not found
```
**Solução**: Verifique se `SUPABASE_URL` e `SUPABASE_ANON_KEY` estão corretos nos secrets.

### Erro de Importação
```
❌ No module named 'streamlit_option_menu'
```
**Solução**: Execute `pip install -r requirements.txt`

### App Não Carrega
**Soluções**:
1. Verifique os logs no Streamlit Cloud
2. Confirme que `app.py` está na raiz
3. Verifique se todos os arquivos foram enviados

### Performance Lenta
**Otimizações**:
1. Use `@st.cache_data` para dados que não mudam
2. Limite consultas ao banco
3. Otimize queries SQL
4. Use paginação para tabelas grandes

## 📞 Suporte

### Documentação
- [Streamlit Docs](https://docs.streamlit.io)
- [Supabase Docs](https://supabase.com/docs)
- [Plotly Docs](https://plotly.com/python/)

### Comunidade
- [Streamlit Community](https://discuss.streamlit.io)
- [Supabase Discord](https://discord.supabase.com)

## 📝 Changelog

### v1.0.0 (Inicial)
- ✅ Sistema completo de autenticação
- ✅ Dashboard com métricas em tempo real
- ✅ CRUD completo de vendas e leads
- ✅ Sistema de batalha entre vendedores
- ✅ Análise financeira com ROI
- ✅ Configurações e integrações
- ✅ Export/Import de dados
- ✅ Mobile responsive
- ✅ Deploy gratuito no Streamlit Cloud

## 📄 Licença

Este projeto é privado e destinado ao uso interno da equipe de vendas.

## 🎯 Próximas Funcionalidades

- [ ] App mobile nativo (React Native)
- [ ] Integração com Zapier
- [ ] IA para previsão de vendas
- [ ] Chat interno entre vendedores
- [ ] Gamificação avançada
- [ ] Relatórios automáticos por email
- [ ] Dashboard para clientes
- [ ] Integração com redes sociais

---

**🚀 Desenvolvido com ❤️ para maximizar vendas high ticket no Instagram!**

---

## 🏁 Quick Start

Para deploy imediato:

1. ⭐ Criar projeto no Supabase
2. 🗃️ Executar `schema.sql` no Supabase
3. 🚀 Deploy no Streamlit Cloud
4. ⚙️ Configurar secrets com URLs do Supabase
5. 🎉 Acessar e usar credenciais: `ana`/`ana2024` ou `fernando`/`fernando2024`

**Em 5 minutos você terá um dashboard profissional rodando!** 🎯