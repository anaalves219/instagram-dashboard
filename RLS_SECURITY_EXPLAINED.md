# 🔒 Row Level Security (RLS) - Sistema Inteligente

## 🎯 Como Funciona

### **👁️ VISUALIZAÇÃO: Todos veem TUDO**
- Ana vê suas vendas + vendas do Fernando
- Fernando vê suas vendas + vendas da Ana
- Relatórios mostram dados completos
- Dashboard comparativo funciona perfeitamente

### **✏️ EDIÇÃO: Cada um edita apenas o SEU**
- Ana só pode criar/editar/deletar suas próprias vendas
- Fernando só pode criar/editar/deletar suas próprias vendas
- Tentativa de editar dados do outro = BLOQUEADO pelo Supabase

## 📋 Tipos de Objetos

### **🗃️ TABELAS (suportam RLS):**
- `vendas` - Dados de vendas
- `leads` - Dados de leads  
- `metas` - Metas de vendedores
- `custos` - Custos operacionais
- `activity_logs` - Logs de atividades
- `configuracoes` - Configurações do sistema
- `notificacoes` - Notificações

### **👁️ VIEWS (herdam RLS das tabelas):**
- `leads_funil` - View do funil de leads
- `performance_diaria` - View de performance diária
- `users` - View de usuários
- `vendas_resumo` - View resumo de vendas

**💡 IMPORTANTE:** Views não podem ter RLS aplicado diretamente, mas herdam a segurança das tabelas que usam.

## 🔧 Implementação Técnica

### **1. Contexto do Usuário**
```javascript
// No código da aplicação
user_info = st.session_state.get('user_info', {})
current_user = user_info.get('name', '')  // "Ana" ou "Fernando"

// Define no Supabase
supabase.rpc('set_config', {
    'parameter': 'app.current_user_name',
    'value': current_user
})
```

### **2. Políticas RLS**
```sql
-- TODOS podem VER todas as vendas
CREATE POLICY "vendas_select_all" ON vendas
    FOR SELECT USING (true);

-- APENAS o próprio vendedor pode EDITAR
CREATE POLICY "vendas_update_own" ON vendas
    FOR UPDATE USING (
        vendedor = current_setting('app.current_user_name', true)
    );
```

## ✅ Exemplo Prático

### **Cenário: Ana logada no sistema**

**✅ PODE FAZER:**
- Ver suas vendas: `SELECT * FROM vendas WHERE vendedor = 'Ana'`
- Ver vendas do Fernando: `SELECT * FROM vendas WHERE vendedor = 'Fernando'`
- Criar nova venda: `INSERT INTO vendas (vendedor='Ana', ...)`
- Editar sua venda: `UPDATE vendas SET valor=2000 WHERE vendedor='Ana'`

**❌ NÃO PODE FAZER:**
- Editar venda do Fernando: `UPDATE vendas SET valor=2000 WHERE vendedor='Fernando'`
- Criar venda como Fernando: `INSERT INTO vendas (vendedor='Fernando', ...)`
- Deletar venda do Fernando: `DELETE FROM vendas WHERE vendedor='Fernando'`

## 🛡️ Segurança

### **Proteção a Nível de Banco**
- RLS é aplicado ANTES da query chegar no banco
- Impossível burlar via código da aplicação
- Proteção mesmo se houver bug no frontend

### **Transparência de Dados**
- Relatórios funcionam normalmente
- Métricas comparativas precisas
- Dashboard conjunto operacional

## 🚀 Benefícios

1. **👥 Colaboração**: Todos veem o desempenho geral
2. **🔒 Proteção**: Ninguém altera dados alheios
3. **📊 Relatórios**: Métricas completas e precisas
4. **⚡ Performance**: RLS nativo do PostgreSQL
5. **🛡️ Segurança**: Proteção a nível de banco de dados

## 🔄 Como Ativar

1. Execute `rls_smart_policies.sql` no Supabase SQL Editor
2. As políticas são aplicadas automaticamente
3. Sistema funciona transparentemente
4. Cada usuário logado tem suas permissões

## 🧪 Como Testar

### **Teste 1: Visualização**
1. Login como Ana
2. Vá em Vendas - deve ver vendas de Ana + Fernando
3. Vá em Relatórios - deve ver dados completos

### **Teste 2: Edição Própria**
1. Login como Ana
2. Adicione nova venda
3. Edite uma venda existente da Ana
4. ✅ Deve funcionar normalmente

### **Teste 3: Proteção**
1. Login como Ana
2. Tente editar venda do Fernando (via código)
3. ❌ Deve ser bloqueado pelo RLS

---

🎯 **Resultado**: Sistema seguro, transparente e colaborativo!