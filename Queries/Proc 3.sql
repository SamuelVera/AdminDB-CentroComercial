CREATE OR REPLACE FUNCTION gastosmartphone(smartphone INTEGER)
RETURNS BIGINT AS $$
	DECLARE
			monto BIGINT;
	BEGIN
		SELECT CAST(SUM(f.monto) AS BIGINT) INTO monto 
			FROM factura AS f
			WHERE 
				EXTRACT(MONTH FROM fechacompra) = EXTRACT(MONTH FROM current_timestamp)-1
				AND
				EXTRACT(YEAR FROM fechacompra) = EXTRACT(YEAR FROM current_timestamp)
				AND f.idsmartphone IS NOT NULL
				AND f.idsmartphone = smartphone;
		RETURN monto;
	END; $$
LANGUAGE plpgsql;