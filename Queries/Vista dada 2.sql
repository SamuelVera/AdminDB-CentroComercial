CREATE OR REPLACE VIEW top5mastiempo AS (
	SELECT estadia.idsmartphone,
    	sum(estadia.fechasalida - estadia.fechaentrada) AS "Tiempo de estadia"
   		FROM estadia
  		WHERE estadia.fechasalida IS NOT NULL AND date_part('month'::text, estadia.fechaentrada) = (date_part('month'::text, CURRENT_DATE) - 1::double precision) AND date_part('year'::text, estadia.fechaentrada) = date_part('year'::text, CURRENT_DATE)
  		GROUP BY estadia.idsmartphone
  		ORDER BY (sum(estadia.fechasalida - estadia.fechaentrada)) DESC
 		LIMIT 5
);