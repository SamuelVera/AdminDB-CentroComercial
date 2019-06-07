CREATE OR REPLACE FUNCTION verificarsmartphoneinmesaincc()
	RETURNS TRIGGER AS $$
    BEGIN
         IF (NEW.idsmartphone NOT IN 
                (SELECT idsmartphone 
                FROM estadia 
                WHERE fechasalida IS NULL
                AND idsmartphone = NEW.idsmartphone
                ORDER BY fechaentrada
                LIMIT 1)) THEN
            RAISE EXCEPTION 
                'El smartphone % no se encuentra en el cc, a las % se detecto en mesa %'
				,NEW.idsmartphone,NEW.fechaocupado,NEW.idmesa;
        END IF;
        RETURN NEW;
    END; $$
LANGUAGE plpgsql;

CREATE TRIGGER verificarsmartphoneinmesaincctrig
BEFORE INSERT ON monitoreomesa
FOR EACH ROW EXECUTE PROCEDURE verificarsmartphoneinmesaincc();