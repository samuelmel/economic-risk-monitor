
SELECT
    'raw_usuarios' AS tabela,
    COUNT(*) AS qtd
FROM raw_usuarios
UNION ALL

SELECT
    'silver_usuarios' AS tabela,
    COUNT(*) AS qtd
FROM silver_usuarios
UNION ALL

SELECT
    'raw_posts' AS tabela,
    COUNT(*) AS qtd
FROM raw_posts
UNION ALL

SELECT
    'silver_posts' AS tabela,
    COUNT(*) AS qtd
FROM silver_posts;