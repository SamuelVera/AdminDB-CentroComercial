CREATE VIEW top5localesflujopersonas AS 
(SELECT f.nombre AS franquicia, COUNT(*) AS flujopersonas
	FROM franquicia AS f
	INNER JOIN local AS l
		ON f.id=l.idfranquicia
	INNER JOIN accesolocal AS al
		ON l.id=al.idlocal
	WHERE EXTRACT(MONTH FROM al.fechaacceso) = EXTRACT(MONTH FROM current_date)-1
	AND EXTRACT(YEAR FROM al.fechaacceso) = EXTRACT(YEAR FROM current_date)
	GROUP BY f.id
	ORDER BY flujopersonas DESC
	LIMIT 5);