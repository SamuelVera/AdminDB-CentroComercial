CREATE OR REPLACE FUNCTION flujosexopuerta(numeropuerta INT)
	RETURNS TABLE(
		hombres BIGINT,
		mujeres BIGINT,
		puerta VARCHAR
	) AS $$
	BEGIN
		RETURN QUERY (
			SELECT (
				SELECT COUNT(*) 
				FROM accesoentrada AS a
				INNER JOIN puerta AS p
					ON a.idpuerta=p.numero
				WHERE 
					p.numero=numeropuerta
					AND
					a.sexo=0
					AND
					EXTRACT(MONTH FROM a.fechaacceso)=EXTRACT(MONTH FROM current_date)
					AND EXTRACT(YEAR FROM a.fechaacceso)=EXTRACT(YEAR FROM current_date)
				GROUP BY p.numero
			),
			(
				SELECT COUNT(*) 
				FROM accesoentrada AS a
				INNER JOIN puerta AS p
					ON a.idpuerta=p.numero
				WHERE 
					p.numero=numeropuerta
					AND
					a.sexo=1
					AND
					EXTRACT(MONTH FROM a.fechaacceso)=EXTRACT(MONTH FROM current_date)
					AND EXTRACT(YEAR FROM a.fechaacceso)=EXTRACT(YEAR FROM current_date)
				GROUP BY p.numero
			),
			(
				SELECT localizacion 
				FROM puerta 
				WHERE numero=numeropuerta
			)
		);
	END; $$
LANGUAGE plpgsql;