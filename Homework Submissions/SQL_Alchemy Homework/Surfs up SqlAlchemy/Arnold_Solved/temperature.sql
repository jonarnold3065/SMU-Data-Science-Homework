SELECT
        station,
        date,
        tobs as temperature
    FROM
        measurement
    WHERE
        station = 'USC00519281'
        and date >= '2016-08-23'
    ORDER BY
        date asc;