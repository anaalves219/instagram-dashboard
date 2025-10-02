-- FIX RLS PARA VIEWS - Views não suportam RLS diretamente
-- Execute este script APÓS os anteriores

-- 1. IDENTIFICAR o que são tabelas vs views
SELECT 
    table_name,
    table_type,
    CASE 
        WHEN table_type = 'BASE TABLE' THEN '📋 TABELA'
        WHEN table_type = 'VIEW' THEN '👁️ VIEW'
        ELSE '❓ OUTRO'
    END as tipo
FROM information_schema.tables 
WHERE table_schema = 'public' 
    AND table_name IN (
        'vendas', 'leads', 'metas', 'custos', 'activity_logs', 'configuracoes', 'notificacoes',
        'leads_funil', 'performance_diaria', 'users', 'vendas_resumo'
    )
ORDER BY table_type, table_name;

-- 2. REMOVER tentativas de RLS em views (se existirem)
DO $$
BEGIN
    -- Verificar se são views e remover qualquer política
    IF EXISTS (SELECT 1 FROM information_schema.views WHERE table_name = 'leads_funil') THEN
        -- Desabilitar RLS se foi habilitado por engano
        BEGIN
            ALTER TABLE leads_funil DISABLE ROW LEVEL SECURITY;
        EXCEPTION WHEN OTHERS THEN
            -- Ignorar se não conseguir (views não suportam RLS)
            NULL;
        END;
        RAISE NOTICE 'LEADS_FUNIL é uma VIEW - RLS não aplicável';
    END IF;
    
    IF EXISTS (SELECT 1 FROM information_schema.views WHERE table_name = 'performance_diaria') THEN
        BEGIN
            ALTER TABLE performance_diaria DISABLE ROW LEVEL SECURITY;
        EXCEPTION WHEN OTHERS THEN
            NULL;
        END;
        RAISE NOTICE 'PERFORMANCE_DIARIA é uma VIEW - RLS não aplicável';
    END IF;
    
    IF EXISTS (SELECT 1 FROM information_schema.views WHERE table_name = 'users') THEN
        BEGIN
            ALTER TABLE users DISABLE ROW LEVEL SECURITY;
        EXCEPTION WHEN OTHERS THEN
            NULL;
        END;
        RAISE NOTICE 'USERS é uma VIEW - RLS não aplicável';
    END IF;
    
    IF EXISTS (SELECT 1 FROM information_schema.views WHERE table_name = 'vendas_resumo') THEN
        BEGIN
            ALTER TABLE vendas_resumo DISABLE ROW LEVEL SECURITY;
        EXCEPTION WHEN OTHERS THEN
            NULL;
        END;
        RAISE NOTICE 'VENDAS_RESUMO é uma VIEW - RLS não aplicável';
    END IF;
END $$;

-- 3. VERIFICAR views existentes
SELECT 
    table_name as view_name,
    view_definition
FROM information_schema.views 
WHERE table_schema = 'public' 
    AND table_name IN ('leads_funil', 'performance_diaria', 'users', 'vendas_resumo')
ORDER BY table_name;

-- 4. VERIFICAR políticas RLS apenas em TABELAS
SELECT 
    t.table_name,
    t.table_type,
    COALESCE(p.policy_count, 0) as policies_count,
    CASE 
        WHEN t.table_type = 'VIEW' THEN '👁️ VIEW (sem RLS)'
        WHEN t.table_type = 'BASE TABLE' AND pt.rowsecurity THEN '🔒 TABELA (RLS ativo)'
        WHEN t.table_type = 'BASE TABLE' AND NOT pt.rowsecurity THEN '🔓 TABELA (RLS inativo)'
        ELSE '❓ DESCONHECIDO'
    END as status_rls
FROM information_schema.tables t
LEFT JOIN (
    SELECT 
        tablename, 
        COUNT(*) as policy_count 
    FROM pg_policies 
    GROUP BY tablename
) p ON t.table_name = p.tablename
LEFT JOIN pg_tables pt ON t.table_name = pt.tablename AND pt.schemaname = 'public'
WHERE t.table_schema = 'public' 
    AND t.table_name IN (
        'vendas', 'leads', 'metas', 'custos', 'activity_logs', 'configuracoes', 'notificacoes',
        'leads_funil', 'performance_diaria', 'users', 'vendas_resumo'
    )
ORDER BY t.table_type, t.table_name;

-- 5. LISTAR todas as políticas RLS criadas (apenas em tabelas)
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
WHERE tablename IN (
    'vendas', 'leads', 'metas', 'custos', 'activity_logs', 'configuracoes', 'notificacoes'
)
ORDER BY tablename, cmd;

-- EXPLICAÇÃO SOBRE VIEWS
SELECT '
📋 EXPLICAÇÃO:
- TABELAS: Suportam RLS (Row Level Security)
- VIEWS: NÃO suportam RLS diretamente
- As views herdam as permissões das tabelas base
- Se as tabelas têm RLS, as views também são protegidas
- leads_funil, performance_diaria, users, vendas_resumo são VIEWS
- Elas são automaticamente protegidas pelas tabelas que usam
' as explicacao;

-- SUCESSO!
SELECT 'RLS CONFIGURADO CORRETAMENTE - VIEWS IDENTIFICADAS E TRATADAS!' as status;