CREATE OR REPLACE FUNCTION verificaroneincc(smartphone INT)
	RETURNS VARCHAR AS $$
	BEGIN
		IF(smartphone IN (
			SELECT idsmartphone
			FROM estadia
			WHERE idsmartphone = smartphone
			AND fechasalida IS NULL
			ORDER BY fechaentrada DESC
			LIMIT 1
		))THEN
			RAISE INFO 'El smartphone se encuentra en el centro comercial'
			RETURN 'El smartphone se encuentra en el centro comercial';
		ELSE 
			RAISE INFO 'El smartphone no se encuentra en el centro comercial';
			RETURN 'El smartphone no se encuentra en el centro comercial';
		END IF;
		RETURN '';
	END; $$
LANGUAGE plpgsql;