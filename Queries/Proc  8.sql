CREATE OR REPLACE FUNCTION primerafacturames(mes int, anio int)
	RETURNS TABLE (idfactura INTEGER,fecha TIMESTAMP WITHOUT TIME ZONE, ci INTEGER, monto INTEGER)
	AS $$
	BEGIN
		RETURN QUERY(
		SELECT f.numero, f.fechacompra, f.cicomprador, f.monto FROM factura AS f
		INNER JOIN primerfacturadia AS pf
			ON pf.idfactura = f.numero
		WHERE EXTRACT(MONTH FROM f.fechacompra)=mes
		AND EXTRACT(YEAR FROM f.fechacompra)=anio);
	END; $$
LANGUAGE plpgsql;