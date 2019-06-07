CREATE OR REPLACE FUNCTION ventasdetienda(idfran INTEGER)
	RETURNS TABLE (
		nombre VARCHAR(40),
		local VARCHAR(10),
		montoenventas BIGINT
	)AS $$
	BEGIN
		RETURN QUERY (
			SELECT fr.nombre, l.codigo, CAST( SUM(f.monto) AS BIGINT) AS montoenventas
			FROM local AS l
			INNER JOIN factura AS f
				ON l.id = f.idlocal
			INNER JOIN franquicia AS fr
				ON fr.id = l.idfranquicia
			WHERE l.idfranquicia=idfran
			GROUP BY l.id, fr.id
			ORDER BY montoenventas DESC
		);
	END; $$
LANGUAGE plpgsql;