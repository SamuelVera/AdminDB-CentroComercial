CREATE OR REPLACE FUNCTION verificarincc()
	RETURNS TRIGGER AS $$
	BEGIN
		IF(NEW.idsmartphone IS NOT NULL) THEN
			IF (NEW.idsmartphone NOT IN 
				(SELECT idsmartphone 
				   FROM estadia 
				   WHERE fechasalida IS NULL
					AND idsmartphone = NEW.idsmartphone
					LIMIT 1)) THEN
				RAISE EXCEPTION 'El smartphone % no se encuentra en el cc, compra rechazada',NEW.idsmartphone;
			END IF;
		END IF;
		RETURN NEW;
	END; $$
LANGUAGE plpgsql;

CREATE TRIGGER verificarincctrigger
BEFORE INSERT ON factura
FOR EACH ROW EXECUTE PROCEDURE verificarincc();