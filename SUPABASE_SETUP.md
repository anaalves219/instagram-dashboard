# 🗃️ Configuração do Supabase

Para usar o dashboard sem dados mock, você precisa configurar o Supabase. Siga os passos abaixo:

## 🚀 Passo 1: Criar Conta no Supabase

1. Acesse [supabase.com](https://supabase.com)
2. Clique em "Start your project"
3. Faça login com GitHub
4. É **GRATUITO** até 500MB e 2 projetos

## 📊 Passo 2: Criar Projeto

1. Clique em "New Project"
2. Nome: `instagram-sales-dashboard`
3. Database Password: `sua-senha-segura`
4. Region: `South America (São Paulo)` ou `East US (N. Virginia)`
5. Clique "Create new project"
6. **Aguarde 2-3 minutos** para o projeto ser criado

## 🗄️ Passo 3: Executar Schema

1. No painel do Supabase, vá em **SQL Editor**
2. Clique em "New query"
3. **Copie TODO o conteúdo** do arquivo `schema.sql`
4. **Cole no editor** e clique "Run"
5. Aguarde a execução (pode demorar 30-60 segundos)

✅ **Sucesso se aparecer:** "Success. No rows returned"

## 🔑 Passo 4: Copiar Credenciais

1. Vá em **Settings** > **API**
2. Copie:
   - **URL**: `https://seu-projeto.supabase.co`
   - **anon public**: `eyJ0eXAiOiJKV1Q...` (chave longa)

## ⚙️ Passo 5: Configurar no Streamlit Cloud

1. Vá ao seu app no Streamlit Cloud
2. **Settings** > **Secrets**
3. Adicione:

```toml
[secrets]
SUPABASE_URL = "https://seu-projeto.supabase.co"
SUPABASE_ANON_KEY = "sua-chave-anon-aqui"
```

4. Clique **"Save"**
5. O app vai reiniciar automaticamente

## ✅ Passo 6: Testar

1. Acesse seu dashboard
2. Faça login com `ana` / `ana2024`
3. Se aparecer **"⚠️ Supabase não configurado!"** = erro nas credenciais
4. Se aparecer **dashboard vazio** = ✅ SUCESSO!

## 🎯 Primeiro Uso

Após configurar:

1. **Adicione sua primeira venda** na página Vendas
2. **Adicione alguns leads** na página Leads
3. **Configure suas metas** na página Config
4. **Explore todas as funcionalidades!**

## 🔒 Segurança

- ✅ Todas as credenciais ficam nos **secrets** do Streamlit
- ✅ Conexão **HTTPS** criptografada
- ✅ Banco **PostgreSQL** profissional
- ✅ Backup automático do Supabase

## 🆘 Problemas Comuns

### "Supabase não configurado"
- Verifique se copiou URL e ANON_KEY corretos
- Confirme que salvou nos secrets do Streamlit Cloud

### "Erro ao buscar vendas"
- Execute o arquivo `schema.sql` no Supabase
- Verifique se todas as tabelas foram criadas

### "403 Forbidden"
- A ANON_KEY está incorreta
- Copie novamente de Settings > API

### ⚠️ "ROW LEVEL SECURITY VIOLATION" (MAIS COMUM)
**ERRO:** `new row violates row-level security policy`

**SOLUÇÃO RÁPIDA:**
1. Vá no **Supabase SQL Editor**
2. Copie todo conteúdo do arquivo `fix_rls_policies.sql`
3. Execute no SQL Editor
4. Clique "Run"

**OU SOLUÇÃO MANUAL:**
1. No Supabase: **Authentication** > **Policies**
2. Para cada tabela (vendas, leads, metas, etc.):
   - Delete todas as policies existentes
   - Crie nova policy: "Enable all operations"
   - Allowed operation: "All"
   - Target roles: "authenticated" 
   - USING expression: `true`
   - WITH CHECK expression: `true`

✅ **Isso permite todas as operações nas tabelas**

### 🔒 "SMART RLS - SEGURANÇA AVANÇADA" (RECOMENDADO)
**OBJETIVO:** Todos veem todos os dados, mas cada vendedor só edita o seu

**SOLUÇÃO COMPLETA (3 scripts):**
1. **DIAGNÓSTICO:** Vá no **Supabase SQL Editor**
   - Copie todo conteúdo do arquivo `diagnose_tables.sql`
   - Execute e veja quais tabelas existem

2. **RLS PRINCIPAL:** No **Supabase SQL Editor**
   - Copie todo conteúdo do arquivo `rls_smart_policies_safe.sql`
   - Execute e aguarde mensagens de sucesso

3. **RLS VIEWS FIX:** No **Supabase SQL Editor**
   - Copie todo conteúdo do arquivo `rls_views_fix.sql`
   - Execute para tratar views corretamente (leads_funil, performance_diaria, users, vendas_resumo são VIEWS, não tabelas)

**✅ RESULTADO:**
- **Ana** vê vendas de Fernando, mas só edita as suas
- **Fernando** vê vendas de Ana, mas só edita as suas
- **Relatórios** mostram dados de ambos
- **Segurança** máxima - ninguém altera dados do outro

**🎯 BENEFÍCIOS:**
- Dashboard conjunto funcionando
- Cada vendedor protegido
- Transparência total nos dados
- Relatórios comparativos precisos

## 📞 Suporte

- **Supabase Docs**: https://supabase.com/docs
- **Streamlit Secrets**: https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources

---

🎉 **Após a configuração, você terá um dashboard profissional 100% funcional!**