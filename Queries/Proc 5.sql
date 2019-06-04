CREATE OR REPLACE FUNCTION cantidadocupacionesmesa(id INTEGER, fecha TIMESTAMP)
	RETURNS BIGINT AS $$
	DECLARE
		datum BIGINT;
	BEGIN
		SELECT COUNT(*) INTO datum
			FROM estadomesa
			WHERE idmesa=id
			AND ocupado=true
			AND EXTRACT(DAY FROM fechaestado)=EXTRACT(DAY FROM fecha)
			AND EXTRACT(MONTH FROM fechaestado)=EXTRACT(MONTH FROM fecha)
			AND EXTRACT(YEAR FROM fechaestado)=EXTRACT(YEAR FROM fecha);
		RETURN datum;
	END; $$
LANGUAGE plpgsql;