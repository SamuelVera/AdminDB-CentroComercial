CREATE OR REPLACE VIEW enccenmesaoenlocal AS (SELECT (
	SELECT COUNT(*) FROM
	recorrido AS r
	INNER JOIN estadia AS e
		ON r.idsmartphone = e.idsmartphone
	WHERE r.fechasalida IS NULL
		AND e.fechasalida IS NULL) AS inlocal,
(
		SELECT COUNT(*) FROM
	estadia AS e
	INNER JOIN monitoreomesa AS mm
		ON e.idsmartphone = mm.idsmartphone
	WHERE e.fechasalida IS NULL
		AND mm.fechadesocupado IS NULL) AS inmesa);