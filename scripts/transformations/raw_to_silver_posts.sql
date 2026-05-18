INSERT INTO silver_posts (
    post_id,
    user_id,
    titulo,
    conteudo,
    qtd_palavras_titulo,
    dt_processamento
)
SELECT
    id AS post_id,
    user_id,
    title AS titulo,
    LEFT(REPLACE(body, E'\n', ' '), 500) AS conteudo,
    LENGTH(TRIM(title)) - LENGTH(REPLACE(TRIM(title), ' ', '')) + 1 AS qtd_palavras_titulo,
    CURRENT_DATE AS dt_processamento
FROM raw_posts;