CREATE VIEW flujoporsectorporpiso AS
(SELECT COUNT(*) AS flujo,
	s.nombre AS sector,
	p.nombre AS piso
	FROM accesolocal AS a
	INNER JOIN local AS l
		ON a.idlocal=l.id
	INNER JOIN sector AS s
		ON l.idsector=s.id
	INNER JOIN piso AS p
		ON l.idpiso=p.numero
	WHERE 
 		EXTRACT(MONTH FROM a.fechaacceso) = EXTRACT(MONTH FROM current_date)-1
 		AND
 		EXTRACT(YEAR FROM a.fechaacceso) = EXTRACT(YEAR FROM current_date)
	GROUP BY s.id, p.numero
	ORDER BY flujo DESC);
