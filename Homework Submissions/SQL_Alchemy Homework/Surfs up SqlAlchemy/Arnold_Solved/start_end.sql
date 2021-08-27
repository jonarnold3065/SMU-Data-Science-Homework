SELECT
        min(date) as start_date,
        max(date) as end_date,
        min(tobs) as min_temp,
        avg(tobs) as avg_temp,
        max(tobs) as max_temp
    FROM
        measurement
    where
        date >= '{start}'
        and date <= '{end}'