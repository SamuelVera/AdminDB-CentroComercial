CREATE OR REPLACE VIEW accesosporpuertaemergencia AS (
	SELECT COUNT(*) 
	FROM accesoentrada AS ae
	INNER JOIN puerta AS p
		ON ae.idpuerta = p.numero
	WHERE p.emergencia = TRUE
);