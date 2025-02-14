-- Inserir ou atualizar as métricas mensais
WITH dados_anuais AS (
    SELECT 
        id_conta, 
        date_trunc('month', data_inicio) AS mes,
        SUM(investimento) AS investimento_total,
        SUM(cliques) AS cliques_total,
        SUM(leads) AS leads_total,
        SUM(conversas_iniciadas) AS conversas_total,
        SUM(cadastro_meta) AS cadastros_total,
        SUM(investimento) / NULLIF(SUM(conversas_iniciadas), 0) AS custo_por_conversa,
        SUM(investimento) / NULLIF(SUM(leads), 0) AS custo_por_lead,
        SUM(investimento) / NULLIF(SUM(cadastro_meta), 0) AS custo_por_cadastro
    FROM anuncios_json
    GROUP BY id_conta, date_trunc('month', data_inicio)
)
-- Inserir ou atualizar as métricas mensais
INSERT INTO metricas_mensais (
    mes, unidade, investimento_total, cliques_total, leads_total, conversas_total, cadastros_total,
    custo_por_conversa, custo_por_lead, custo_por_cadastro
)
SELECT 
    mes, 
    id_conta AS unidade, 
    investimento_total, 
    cliques_total, 
    leads_total, 
    conversas_total, 
    cadastros_total, 
    custo_por_conversa, 
    custo_por_lead, 
    custo_por_cadastro
FROM dados_anuais
ON CONFLICT (unidade, mes) DO UPDATE
SET 
    investimento_total = EXCLUDED.investimento_total,
    cliques_total = EXCLUDED.cliques_total,
    leads_total = EXCLUDED.leads_total,
    conversas_total = EXCLUDED.conversas_total,
    cadastros_total = EXCLUDED.cadastros_total,
    custo_por_conversa = EXCLUDED.custo_por_conversa,
    custo_por_lead = EXCLUDED.custo_por_lead,
    custo_por_cadastro = EXCLUDED.custo_por_cadastro
ORDER BY id_conta;

SELECT * 
FROM metricas_mensais
ORDER BY unidade, mes ASC;
