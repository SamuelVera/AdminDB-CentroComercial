CREATE OR REPLACE FUNCTION checkfacturaespecial()
	RETURNS TRIGGER AS $$
	BEGIN
		IF(NEW.idsmartphone IS NOT NULL) THEN
			IF(
				NOT EXISTS 
				(
					SELECT numero
					FROM factura
					WHERE EXTRACT(DAY FROM fechacompra) = EXTRACT(DAY FROM NEW.fechacompra) 
					AND EXTRACT(MONTH FROM fechacompra) = EXTRACT(MONTH FROM NEW.fechacompra)
					AND EXTRACT(YEAR FROM fechacompra) = EXTRACT(YEAR FROM NEW.fechacompra)
					AND idsmartphone IS NOT NULL
				)
			)THEN
				EXECUTE insertprimerfacturadia(NEW.numero,NEW.fechacompra);
			END IF;
		END IF;
        RETURN NEW;
    END; $$
LANGUAGE plpgsql;

CREATE TRIGGER primerfacturadiatrigger
AFTER INSERT ON factura
FOR EACH ROW EXECUTE PROCEDURE checkfacturaespecial();