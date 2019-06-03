CREATE OR REPLACE FUNCTION localessectorpiso(numerosector INT, numeropiso INT)
	RETURNS TABLE(
		sector VARCHAR,
		piso VARCHAR,
		codigolocal VARCHAR,
		franquicias VARCHAR
	) AS $$
	BEGIN
		RETURN QUERY(
			SELECT s.nombre,
			p.nombre,
			l.codigo,
			f.nombre
			FROM local AS l
			INNER JOIN franquicia AS f
				ON l.idfranquicia=f.id
			INNER JOIN piso AS p
				ON l.idpiso=p.numero
			INNER JOIN sector AS s
				ON l.idsector=s.id
			WHERE
				l.idsector=numerosector
				AND p.numero=numeropiso
		);
	END; $$
LANGUAGE plpgsql;