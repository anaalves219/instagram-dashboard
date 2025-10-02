-- SMART RLS POLICIES SEGURO - TODOS VEEM TUDO, CADA UM EDITA O SEU
-- Execute este script APÓS executar diagnose_tables.sql

-- 0. CRIAR função para definir usuário atual
CREATE OR REPLACE FUNCTION set_config(parameter text, value text)
RETURNS void AS $$
BEGIN
    PERFORM set_config(parameter, value, false);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Dar permissão para usar a função
GRANT EXECUTE ON FUNCTION set_config(text, text) TO authenticated, anon;

-- 1. HABILITAR RLS em todas as tabelas
ALTER TABLE IF EXISTS vendas ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS metas ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS custos ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS activity_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS configuracoes ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS notificacoes ENABLE ROW LEVEL SECURITY;

-- 2. LIMPAR políticas existentes
DROP POLICY IF EXISTS "vendas_allow_all" ON vendas;
DROP POLICY IF EXISTS "leads_allow_all" ON leads;
DROP POLICY IF EXISTS "metas_allow_all" ON metas;
DROP POLICY IF EXISTS "custos_allow_all" ON custos;
DROP POLICY IF EXISTS "activity_logs_allow_all" ON activity_logs;
DROP POLICY IF EXISTS "configuracoes_allow_all" ON configuracoes;
DROP POLICY IF EXISTS "notificacoes_allow_all" ON notificacoes;

-- 3. POLÍTICAS PARA VENDAS (se a tabela existir)
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'vendas') THEN
        -- Verificar se coluna vendedor existe
        IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'vendas' AND column_name = 'vendedor') THEN
            -- Todos podem VER todas as vendas
            EXECUTE 'CREATE POLICY "vendas_select_all" ON vendas FOR SELECT USING (true)';
            
            -- Apenas o próprio vendedor pode INSERIR
            EXECUTE 'CREATE POLICY "vendas_insert_own" ON vendas FOR INSERT WITH CHECK (vendedor = current_setting(''app.current_user_name'', true))';
            
            -- Apenas o próprio vendedor pode ATUALIZAR
            EXECUTE 'CREATE POLICY "vendas_update_own" ON vendas FOR UPDATE USING (vendedor = current_setting(''app.current_user_name'', true))';
            
            -- Apenas o próprio vendedor pode DELETAR
            EXECUTE 'CREATE POLICY "vendas_delete_own" ON vendas FOR DELETE USING (vendedor = current_setting(''app.current_user_name'', true))';
            
            RAISE NOTICE 'RLS para VENDAS criado com sucesso!';
        ELSE
            -- Se não tem coluna vendedor, permite tudo por enquanto
            EXECUTE 'CREATE POLICY "vendas_allow_all" ON vendas FOR ALL USING (true) WITH CHECK (true)';
            RAISE NOTICE 'VENDAS: Coluna vendedor não encontrada - usando política permissiva';
        END IF;
    END IF;
END $$;

-- 4. POLÍTICAS PARA LEADS (se a tabela existir)
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'leads') THEN
        IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'leads' AND column_name = 'vendedor') THEN
            EXECUTE 'CREATE POLICY "leads_select_all" ON leads FOR SELECT USING (true)';
            EXECUTE 'CREATE POLICY "leads_insert_own" ON leads FOR INSERT WITH CHECK (vendedor = current_setting(''app.current_user_name'', true))';
            EXECUTE 'CREATE POLICY "leads_update_own" ON leads FOR UPDATE USING (vendedor = current_setting(''app.current_user_name'', true))';
            EXECUTE 'CREATE POLICY "leads_delete_own" ON leads FOR DELETE USING (vendedor = current_setting(''app.current_user_name'', true))';
            RAISE NOTICE 'RLS para LEADS criado com sucesso!';
        ELSE
            EXECUTE 'CREATE POLICY "leads_allow_all" ON leads FOR ALL USING (true) WITH CHECK (true)';
            RAISE NOTICE 'LEADS: Coluna vendedor não encontrada - usando política permissiva';
        END IF;
    END IF;
END $$;

-- 5. POLÍTICAS PARA METAS (se a tabela existir)
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'metas') THEN
        IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'metas' AND column_name = 'vendedor') THEN
            EXECUTE 'CREATE POLICY "metas_select_all" ON metas FOR SELECT USING (true)';
            EXECUTE 'CREATE POLICY "metas_insert_own" ON metas FOR INSERT WITH CHECK (vendedor = current_setting(''app.current_user_name'', true))';
            EXECUTE 'CREATE POLICY "metas_update_own" ON metas FOR UPDATE USING (vendedor = current_setting(''app.current_user_name'', true))';
            EXECUTE 'CREATE POLICY "metas_delete_own" ON metas FOR DELETE USING (vendedor = current_setting(''app.current_user_name'', true))';
            RAISE NOTICE 'RLS para METAS criado com sucesso!';
        ELSE
            EXECUTE 'CREATE POLICY "metas_allow_all" ON metas FOR ALL USING (true) WITH CHECK (true)';
            RAISE NOTICE 'METAS: Coluna vendedor não encontrada - usando política permissiva';
        END IF;
    END IF;
END $$;

-- 6. POLÍTICAS PARA CUSTOS (se a tabela existir)
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'custos') THEN
        IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'custos' AND column_name = 'vendedor') THEN
            EXECUTE 'CREATE POLICY "custos_select_all" ON custos FOR SELECT USING (true)';
            EXECUTE 'CREATE POLICY "custos_insert_own" ON custos FOR INSERT WITH CHECK (vendedor = current_setting(''app.current_user_name'', true))';
            EXECUTE 'CREATE POLICY "custos_update_own" ON custos FOR UPDATE USING (vendedor = current_setting(''app.current_user_name'', true))';
            EXECUTE 'CREATE POLICY "custos_delete_own" ON custos FOR DELETE USING (vendedor = current_setting(''app.current_user_name'', true))';
            RAISE NOTICE 'RLS para CUSTOS criado com sucesso!';
        ELSE
            EXECUTE 'CREATE POLICY "custos_allow_all" ON custos FOR ALL USING (true) WITH CHECK (true)';
            RAISE NOTICE 'CUSTOS: Coluna vendedor não encontrada - usando política permissiva';
        END IF;
    END IF;
END $$;

-- 7. TABELAS SEM RESTRIÇÃO DE VENDEDOR (se existirem)
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'activity_logs') THEN
        EXECUTE 'CREATE POLICY "activity_logs_all" ON activity_logs FOR ALL USING (true) WITH CHECK (true)';
        RAISE NOTICE 'RLS para ACTIVITY_LOGS criado com sucesso!';
    END IF;
    
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'configuracoes') THEN
        EXECUTE 'CREATE POLICY "configuracoes_all" ON configuracoes FOR ALL USING (true) WITH CHECK (true)';
        RAISE NOTICE 'RLS para CONFIGURACOES criado com sucesso!';
    END IF;
    
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'notificacoes') THEN
        EXECUTE 'CREATE POLICY "notificacoes_all" ON notificacoes FOR ALL USING (true) WITH CHECK (true)';
        RAISE NOTICE 'RLS para NOTIFICACOES criado com sucesso!';
    END IF;
END $$;

-- 8. VERIFICAR políticas criadas
SELECT 
    schemaname, 
    tablename, 
    policyname, 
    permissive, 
    roles, 
    cmd, 
    CASE 
        WHEN cmd = 'SELECT' THEN '👁️ VER'
        WHEN cmd = 'INSERT' THEN '➕ CRIAR'
        WHEN cmd = 'UPDATE' THEN '✏️ EDITAR'
        WHEN cmd = 'DELETE' THEN '🗑️ DELETAR'
        WHEN cmd = 'ALL' THEN '🔓 TUDO'
    END as operacao
FROM pg_policies 
WHERE tablename IN ('vendas', 'leads', 'metas', 'custos', 'activity_logs', 'configuracoes', 'notificacoes')
ORDER BY tablename, cmd;

-- SUCESSO!
SELECT 'SMART RLS POLICIES APLICADAS COM SUCESSO!' as status;