CREATE VIEW accesosporedadpuerta AS
(SELECT COUNT(*) AS flujo,
	CASE
		WHEN a.edad <= 12 THEN 'Infantes'
		WHEN (a.edad BETWEEN 12 AND 20) THEN 'Adolescentes'
		WHEN (a.edad BETWEEN 20 AND 30) THEN 'Jovenes'
		WHEN (a.edad BETWEEN 30 AND 60) THEN 'Adultos'
		WHEN (a.edad >= 60) THEN 'Tercera Edad'
	END AS edad,
	p.localizacion AS puerta
	FROM accesoentrada AS a
	INNER JOIN puerta AS p
	ON a.idpuerta=p.numero
	WHERE EXTRACT (MONTH FROM a.fechaacceso)=EXTRACT (MONTH FROM current_date)-1
	AND EXTRACT (YEAR FROM a.fechaacceso)=EXTRACT (YEAR FROM current_date)
	GROUP BY (	CASE
		WHEN a.edad <= 12 THEN 'Infantes'
		WHEN (a.edad BETWEEN 12 AND 20) THEN 'Adolescentes'
		WHEN (a.edad BETWEEN 20 AND 30) THEN 'Jovenes'
		WHEN (a.edad BETWEEN 30 AND 60) THEN 'Adultos'
		WHEN (a.edad >= 60) THEN 'Tercera Edad'
	END), p.numero
	ORDER BY flujo DESC);