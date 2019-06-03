CREATE VIEW clientemasvisitasalocal AS
(SELECT DISTINCT ON (l.id) l.id AS local,
	r.idsmartphone AS smartphone,
	COUNT(*) AS visitas
	FROM recorrido AS r
	INNER JOIN local AS l
		ON r.idlocal=l.id
 	WHERE EXTRACT(YEAR FROM r.fechaentrada)=EXTRACT(YEAR FROM current_date)
	GROUP BY local, smartphone
	ORDER BY local ASC, visitas DESC, smartphone ASC);