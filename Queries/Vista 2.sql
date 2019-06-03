SELECT DISTINCT ON (s.nombre) s.nombre AS sector,
        r.idsmartphone AS smartphone, 
        SUM(r.fechasalida - r.fechaentrada) AS tiempo
        FROM recorrido AS r
        INNER JOIN local AS l
            ON r.idlocal=l.id
        INNER JOIN sector AS s
            ON l.idsector=s.id
        WHERE r.fechasalida IS NOT NULL
        AND EXTRACT(MONTH FROM r.fechaentrada) = EXTRACT(MONTH FROM current_timestamp)-1
        AND EXTRACT(YEAR FROM r.fechaentrada) = EXTRACT(YEAR FROM current_timestamp)
        GROUP BY smartphone, s.nombre
        ORDER BY s.nombre DESC, tiempo DESC;