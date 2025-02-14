-- Inserir ou atualizar as análises temporais
WITH analises AS (
    -- Seleção de métricas do mês atual
    SELECT 
        m1.unidade,
        m1.mes AS mes_atual,
        m2.mes AS mes_anterior,
        m1.investimento_total,
        m2.investimento_total AS investimento_mes_anterior,
        (m1.investimento_total - COALESCE(m2.investimento_total, 0)) / NULLIF(m2.investimento_total, 0) * 100 AS variacao_investimento,
        m1.cliques_total,
        m2.cliques_total AS cliques_mes_anterior,
        (m1.cliques_total - COALESCE(m2.cliques_total, 0)) / NULLIF(m2.cliques_total, 0) * 100 AS variacao_cliques,
        (m1.leads_total * 100.0 / NULLIF(m1.investimento_total, 0)) AS roi,
        (m1.leads_total * 100.0 / NULLIF(m1.conversas_total, 0)) AS taxa_conversao_lead,
        (m1.cadastros_total * 100.0 / NULLIF(m1.leads_total, 0)) AS taxa_conversao_cadastro
    FROM metricas_mensais m1
    -- Juntando com o mês anterior (1 mês atrás)
    LEFT JOIN metricas_mensais m2 
        ON m1.unidade = m2.unidade 
        AND m1.mes = m2.mes + INTERVAL '1 month'
)
-- Inserir ou atualizar as análises temporais
INSERT INTO analises_temporais (
    mes_atual, mes_anterior, unidade, investimento_total, investimento_mes_anterior, variacao_investimento,
    cliques_total, cliques_mes_anterior, variacao_cliques, roi, taxa_conversao_lead, taxa_conversao_cadastro
)
SELECT 
    mes_atual,
    mes_anterior,
    unidade,
    investimento_total,
    investimento_mes_anterior,
    variacao_investimento,
    cliques_total,
    cliques_mes_anterior,
    variacao_cliques,
    roi,
    taxa_conversao_lead,
    taxa_conversao_cadastro
FROM analises
ON CONFLICT (unidade, mes_atual) DO UPDATE
SET 
    investimento_total = EXCLUDED.investimento_total,
    investimento_mes_anterior = EXCLUDED.investimento_mes_anterior,
    variacao_investimento = EXCLUDED.variacao_investimento,
    cliques_total = EXCLUDED.cliques_total,
    cliques_mes_anterior = EXCLUDED.cliques_mes_anterior,
    variacao_cliques = EXCLUDED.variacao_cliques,
    roi = EXCLUDED.roi,
    taxa_conversao_lead = EXCLUDED.taxa_conversao_lead,
    taxa_conversao_cadastro = EXCLUDED.taxa_conversao_cadastro;

SELECT * 
FROM analises_temporais
ORDER BY unidade, mes_atual ASC;
