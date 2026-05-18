INSERT INTO gold_metricas_usuario (
    user_id,
    nome_usuario,
    cidade,
    empresa,
    total_posts,
    media_palavras_titulo,
    primeiro_post_titulo,
    dt_processamento
)

WITH posts_com_ranking AS (
    SELECT
        sp.post_id,
        sp.user_id,
        sp.titulo,
        sp.qtd_palavras_titulo,
        ROW_NUMBER() OVER (
            PARTITION BY sp.user_id
            ORDER BY sp.post_id ASC
        ) AS rn
    FROM silver_posts sp
),
primeiro_post AS (
    SELECT
        user_id,
        titulo AS primeiro_post_titulo
    FROM posts_com_ranking
    WHERE rn = 1
),
metricas_posts AS (
    SELECT
        user_id,
        COUNT(*) AS total_posts,
        AVG(qtd_palavras_titulo) AS media_palavras_titulo
    FROM silver_posts
    GROUP BY user_id
)
SELECT
    su.user_id,
    su.nome_completo AS nome_usuario,
    su.cidade,
    su.empresa,
    mp.total_posts,
    mp.media_palavras_titulo,
    pp.primeiro_post_titulo,
    CURRENT_DATE AS dt_processamento
FROM silver_usuarios su
JOIN metricas_posts mp
    ON su.user_id = mp.user_id
JOIN primeiro_post pp
    ON su.user_id = pp.user_id;