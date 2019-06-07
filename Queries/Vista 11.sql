CREATE OR REPLACE VIEW primerasventasultimomes AS (
	SELECT pf.idfactura AS "numeroFactura", pf.fecha AS fecha,
		f.cicomprador AS comprador, f.monto AS monto
	FROM primerfacturadia AS pf
	INNER JOIN factura AS f
		ON pf.idfactura=f.numero
	WHERE EXTRACT(MONTH FROM pf.fecha) = EXTRACT(MONTH FROM CURRENT_DATE)-1
	AND EXTRACT(YEAR FROM pf.fecha) = EXTRACT(YEAR FROM CURRENT_DATE)
	ORDER BY fecha ASC
);