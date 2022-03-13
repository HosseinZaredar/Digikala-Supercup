SELECT
    
    query,

    SUM (click_count / log2(position + 1)) / 
    SUM (click_count / log2(rank + 1))
    AS ndcg

FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY query ORDER BY click_count DESC) as rank
    FROM dk_table
)

GROUP BY (query)