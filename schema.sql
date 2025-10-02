-- Instagram Sales Dashboard - Supabase Schema
-- Execute este script no SQL Editor do Supabase

-- Habilitar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(20) DEFAULT 'vendedor',
    theme_primary VARCHAR(7) DEFAULT '#9D4EDD',
    theme_secondary VARCHAR(7) DEFAULT '#06FFA5',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de vendas
CREATE TABLE IF NOT EXISTS vendas (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    cliente_nome VARCHAR(200) NOT NULL,
    cliente_instagram VARCHAR(100),
    cliente_email VARCHAR(200),
    cliente_telefone VARCHAR(20),
    produto VARCHAR(200) NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    vendedor VARCHAR(50) NOT NULL,
    data_venda DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'pendente',
    meio_pagamento VARCHAR(50),
    comissao_pct DECIMAL(5,4) DEFAULT 0.30,
    comissao_valor DECIMAL(10,2) GENERATED ALWAYS AS (valor * comissao_pct) STORED,
    observacoes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de leads
CREATE TABLE IF NOT EXISTS leads (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    instagram VARCHAR(100),
    telefone VARCHAR(20),
    email VARCHAR(200),
    status VARCHAR(20) DEFAULT 'novo',
    origem VARCHAR(50),
    vendedor VARCHAR(50) NOT NULL,
    nota TEXT,
    score INTEGER DEFAULT 5 CHECK (score >= 1 AND score <= 10),
    ultima_interacao DATE,
    data_agendamento TIMESTAMP WITH TIME ZONE,
    valor_estimado DECIMAL(10,2),
    tags TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de metas
CREATE TABLE IF NOT EXISTS metas (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    vendedor VARCHAR(50) NOT NULL,
    ano INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    meta_vendas DECIMAL(10,2) NOT NULL,
    meta_leads INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(vendedor, ano, mes)
);

-- Tabela de custos
CREATE TABLE IF NOT EXISTS custos (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    descricao VARCHAR(200) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    data_custo DATE NOT NULL,
    responsavel VARCHAR(50),
    recorrente BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de logs de atividade
CREATE TABLE IF NOT EXISTS activity_logs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    action VARCHAR(100) NOT NULL,
    details TEXT,
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de configurações
CREATE TABLE IF NOT EXISTS configuracoes (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    chave VARCHAR(100) UNIQUE NOT NULL,
    valor TEXT,
    tipo VARCHAR(20) DEFAULT 'string',
    descricao TEXT,
    updated_by VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de notificações
CREATE TABLE IF NOT EXISTS notificacoes (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    mensagem TEXT,
    tipo VARCHAR(20) DEFAULT 'info',
    lida BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_vendas_vendedor ON vendas(vendedor);
CREATE INDEX IF NOT EXISTS idx_vendas_data ON vendas(data_venda);
CREATE INDEX IF NOT EXISTS idx_vendas_status ON vendas(status);
CREATE INDEX IF NOT EXISTS idx_leads_vendedor ON leads(vendedor);
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE INDEX IF NOT EXISTS idx_leads_created ON leads(created_at);
CREATE INDEX IF NOT EXISTS idx_activity_logs_user ON activity_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_activity_logs_timestamp ON activity_logs(timestamp);

-- Triggers para updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_vendas_updated_at BEFORE UPDATE ON vendas
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_leads_updated_at BEFORE UPDATE ON leads
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_metas_updated_at BEFORE UPDATE ON metas
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_custos_updated_at BEFORE UPDATE ON custos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_configuracoes_updated_at BEFORE UPDATE ON configuracoes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Inserir dados iniciais
INSERT INTO users (username, password_hash, name, role, theme_primary, theme_secondary) VALUES
('ana', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'Ana', 'vendedora', '#9D4EDD', '#06FFA5'),
('fernando', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'Fernando', 'vendedor', '#0EA5E9', '#F97316')
ON CONFLICT (username) DO NOTHING;

-- Inserir metas iniciais
INSERT INTO metas (vendedor, ano, mes, meta_vendas, meta_leads) VALUES
('ana', EXTRACT(YEAR FROM NOW()), EXTRACT(MONTH FROM NOW()), 50000.00, 100),
('fernando', EXTRACT(YEAR FROM NOW()), EXTRACT(MONTH FROM NOW()), 50000.00, 100)
ON CONFLICT (vendedor, ano, mes) DO NOTHING;

-- Inserir configurações iniciais
INSERT INTO configuracoes (chave, valor, tipo, descricao) VALUES
('produto_principal', 'Curso High Ticket', 'string', 'Nome do produto principal'),
('valor_produto', '1997.00', 'decimal', 'Valor padrão do produto'),
('comissao_padrao', '0.30', 'decimal', 'Percentual de comissão padrão'),
('meta_mensal_equipe', '100000.00', 'decimal', 'Meta mensal da equipe'),
('webhook_n8n', '', 'string', 'URL do webhook para n8n'),
('instagram_token', '', 'string', 'Token de acesso do Instagram API'),
('whatsapp_token', '', 'string', 'Token de acesso do WhatsApp API'),
('backup_enabled', 'true', 'boolean', 'Habilitar backup automático'),
('notifications_enabled', 'true', 'boolean', 'Habilitar notificações')
ON CONFLICT (chave) DO NOTHING;

-- RLS (Row Level Security) - Opcional para maior segurança
ALTER TABLE vendas ENABLE ROW LEVEL SECURITY;
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_logs ENABLE ROW LEVEL SECURITY;

-- Policies básicas (ajustar conforme necessário)
CREATE POLICY "Users can view own sales" ON vendas
    FOR SELECT USING (vendedor = current_setting('app.current_user', true));

CREATE POLICY "Users can view own leads" ON leads
    FOR SELECT USING (vendedor = current_setting('app.current_user', true));

-- Views úteis
CREATE OR REPLACE VIEW vendas_resumo AS
SELECT 
    vendedor,
    COUNT(*) as total_vendas,
    SUM(valor) as total_valor,
    SUM(comissao_valor) as total_comissao,
    AVG(valor) as ticket_medio,
    DATE_TRUNC('month', data_venda) as mes_ano
FROM vendas
WHERE status = 'confirmada'
GROUP BY vendedor, DATE_TRUNC('month', data_venda);

CREATE OR REPLACE VIEW leads_funil AS
SELECT 
    vendedor,
    status,
    COUNT(*) as quantidade,
    AVG(score) as score_medio
FROM leads
GROUP BY vendedor, status;

CREATE OR REPLACE VIEW performance_diaria AS
SELECT 
    data_venda,
    vendedor,
    COUNT(*) as vendas_dia,
    SUM(valor) as faturamento_dia
FROM vendas
WHERE status = 'confirmada'
AND data_venda >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY data_venda, vendedor
ORDER BY data_venda DESC;