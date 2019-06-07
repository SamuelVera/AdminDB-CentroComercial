CREATE OR REPLACE VIEW top5franquiciasventas AS (
	SELECT fr.nombre,
    	sum(f.monto) AS total
   	FROM factura f
    	JOIN local l ON f.idlocal = l.id
     	JOIN franquicia fr ON l.idfranquicia = fr.id
  	WHERE date_part('month'::text, f.fechacompra) = (date_part('month'::text, CURRENT_DATE) - 1::double precision) AND date_part('year'::text, f.fechacompra) = date_part('year'::text, CURRENT_DATE)
  	GROUP BY fr.id
  	ORDER BY (sum(f.monto)) DESC
 LIMIT 5
);