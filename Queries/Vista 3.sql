CREATE OR REPLACE VIEW smartphonesencc AS (
 	SELECT count(*) AS count
   	FROM estadia
  	WHERE estadia.fechasalida IS NULL
);