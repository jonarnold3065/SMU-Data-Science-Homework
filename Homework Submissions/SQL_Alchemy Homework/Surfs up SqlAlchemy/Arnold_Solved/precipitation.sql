SELECT
    date,
    avg(prcp) as avg_prcp
    FROM
        measurement
    GROUP BY
        date
    ORDER BY
        date asc;