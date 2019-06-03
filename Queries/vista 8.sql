CREATE VIEW accesosporsexopuerta AS 
(SELECT COUNT(*) AS flujo,
	CASE
 		WHEN a.sexo = 0 THEN 'Hombres'
 		WHEN a.sexo = 1 THEN 'Mujeres'
 		WHEN a.sexo = 2 THEN 'No identificado'
 	END AS sexo,
	p.localizacion AS puerta
FROM accesoentrada AS a
INNER JOIN puerta AS p
	ON a.idpuerta=p.numero
WHERE EXTRACT(MONTH FROM a.fechaacceso)=EXTRACT(MONTH FROM current_date)-1
	AND EXTRACT(YEAR FROM a.fechaacceso)=EXTRACT(YEAR FROM current_date)
GROUP BY p.numero, sexo
ORDER BY flujo DESC);