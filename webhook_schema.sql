-- Script SQL para adicionar suporte a webhooks no banco de dados
-- Execute este script no SQL Editor do Supabase APÓS o schema.sql principal

-- Tabela para armazenar eventos de webhook
CREATE TABLE IF NOT EXISTS webhooks (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    source VARCHAR(50) NOT NULL DEFAULT 'instagram',
    event_type VARCHAR(100) NOT NULL,
    webhook_id VARCHAR(100),
    object_id VARCHAR(100),
    data JSONB,
    signature VARCHAR(255),
    verified BOOLEAN DEFAULT FALSE,
    processed BOOLEAN DEFAULT FALSE,
    processed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'received',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela para configurações de webhook
CREATE TABLE IF NOT EXISTS webhook_configs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,
    webhook_url TEXT,
    verify_token TEXT,
    app_secret TEXT,
    enabled BOOLEAN DEFAULT TRUE,
    auto_create_leads BOOLEAN DEFAULT TRUE,
    auto_notifications BOOLEAN DEFAULT TRUE,
    events_subscribed TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(platform)
);

-- Tabela para estatísticas de webhook
CREATE TABLE IF NOT EXISTS webhook_stats (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    events_received INTEGER DEFAULT 0,
    events_processed INTEGER DEFAULT 0,
    leads_created INTEGER DEFAULT 0,
    comments_processed INTEGER DEFAULT 0,
    dms_processed INTEGER DEFAULT 0,
    mentions_processed INTEGER DEFAULT 0,
    errors_count INTEGER DEFAULT 0,
    avg_processing_time DECIMAL(8,3),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(platform, date)
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_webhooks_source ON webhooks(source);
CREATE INDEX IF NOT EXISTS idx_webhooks_event_type ON webhooks(event_type);
CREATE INDEX IF NOT EXISTS idx_webhooks_processed ON webhooks(processed);
CREATE INDEX IF NOT EXISTS idx_webhooks_created_at ON webhooks(created_at);
CREATE INDEX IF NOT EXISTS idx_webhooks_status ON webhooks(status);
CREATE INDEX IF NOT EXISTS idx_webhook_stats_date ON webhook_stats(date);
CREATE INDEX IF NOT EXISTS idx_webhook_stats_platform ON webhook_stats(platform);

-- Triggers para updated_at
CREATE TRIGGER update_webhooks_updated_at BEFORE UPDATE ON webhooks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_webhook_configs_updated_at BEFORE UPDATE ON webhook_configs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_webhook_stats_updated_at BEFORE UPDATE ON webhook_stats
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Inserir configurações iniciais de webhook
INSERT INTO webhook_configs (platform, enabled, auto_create_leads, auto_notifications, events_subscribed) VALUES
('instagram', true, true, true, ARRAY['messages', 'comments', 'mentions']),
('whatsapp', false, true, true, ARRAY['messages'])
ON CONFLICT (platform) DO NOTHING;

-- View para estatísticas agregadas
CREATE OR REPLACE VIEW webhook_stats_summary AS
SELECT 
    platform,
    SUM(events_received) as total_events,
    SUM(events_processed) as total_processed,
    SUM(leads_created) as total_leads_created,
    SUM(errors_count) as total_errors,
    AVG(avg_processing_time) as avg_processing_time,
    MAX(date) as last_activity
FROM webhook_stats
GROUP BY platform;

-- View para eventos recentes
CREATE OR REPLACE VIEW recent_webhook_events AS
SELECT 
    id,
    source,
    event_type,
    processed,
    status,
    error_message,
    created_at,
    data->'from'->>'username' as username,
    data->'message'->>'text' as message_text,
    data->'value'->>'text' as comment_text
FROM webhooks
ORDER BY created_at DESC
LIMIT 50;

-- Função para limpar webhooks antigos (manter apenas últimos 30 dias)
CREATE OR REPLACE FUNCTION cleanup_old_webhooks()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM webhooks 
    WHERE created_at < (NOW() - INTERVAL '30 days');
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Função para processar estatísticas diárias
CREATE OR REPLACE FUNCTION update_webhook_daily_stats(platform_name VARCHAR, stat_date DATE)
RETURNS VOID AS $$
BEGIN
    INSERT INTO webhook_stats (
        platform, 
        date, 
        events_received,
        events_processed,
        leads_created,
        comments_processed,
        dms_processed,
        mentions_processed,
        errors_count
    )
    SELECT 
        platform_name,
        stat_date,
        COUNT(*) as events_received,
        COUNT(*) FILTER (WHERE processed = true) as events_processed,
        -- Contar leads criados baseado nos logs
        (SELECT COUNT(*) FROM activity_logs 
         WHERE action = 'webhook_lead_created' 
         AND timestamp::date = stat_date) as leads_created,
        COUNT(*) FILTER (WHERE event_type = 'new_comment') as comments_processed,
        COUNT(*) FILTER (WHERE event_type = 'new_message') as dms_processed,
        COUNT(*) FILTER (WHERE event_type = 'mention') as mentions_processed,
        COUNT(*) FILTER (WHERE status = 'error') as errors_count
    FROM webhooks 
    WHERE source = platform_name 
    AND created_at::date = stat_date
    ON CONFLICT (platform, date) DO UPDATE SET
        events_received = EXCLUDED.events_received,
        events_processed = EXCLUDED.events_processed,
        leads_created = EXCLUDED.leads_created,
        comments_processed = EXCLUDED.comments_processed,
        dms_processed = EXCLUDED.dms_processed,
        mentions_processed = EXCLUDED.mentions_processed,
        errors_count = EXCLUDED.errors_count,
        updated_at = NOW();
END;
$$ LANGUAGE plpgsql;

-- RLS (Row Level Security) para webhooks
ALTER TABLE webhooks ENABLE ROW LEVEL SECURITY;
ALTER TABLE webhook_configs ENABLE ROW LEVEL SECURITY;
ALTER TABLE webhook_stats ENABLE ROW LEVEL SECURITY;

-- Políticas RLS (todos os usuários autenticados podem ver)
CREATE POLICY "All users can view webhooks" ON webhooks
    FOR SELECT USING (true);

CREATE POLICY "All users can insert webhooks" ON webhooks
    FOR INSERT WITH CHECK (true);

CREATE POLICY "All users can view webhook configs" ON webhook_configs
    FOR SELECT USING (true);

CREATE POLICY "All users can view webhook stats" ON webhook_stats
    FOR SELECT USING (true);

-- Configurações iniciais de exemplo
INSERT INTO webhook_stats (platform, date, events_received, events_processed, leads_created) VALUES
(
    'instagram', 
    CURRENT_DATE, 
    12, 
    12, 
    4
),
(
    'instagram', 
    CURRENT_DATE - INTERVAL '1 day', 
    8, 
    8, 
    2
)
ON CONFLICT (platform, date) DO NOTHING;

-- Comentário final
COMMENT ON TABLE webhooks IS 'Armazena todos os eventos recebidos via webhook do Instagram/WhatsApp';
COMMENT ON TABLE webhook_configs IS 'Configurações dos webhooks por plataforma';
COMMENT ON TABLE webhook_stats IS 'Estatísticas diárias dos webhooks';