CREATE OR REPLACE FUNCTION verificarsmartphoneinlocalincc()
	RETURNS TRIGGER AS $$
    BEGIN
         IF (NEW.idsmartphone NOT IN 
                (SELECT idsmartphone 
                FROM estadia 
                WHERE fechasalida IS NULL	
				AND idsmartphone=NEW.idsmartphone
				ORDER BY fechaentrada DESC
				LIMIT 1)) THEN
            RAISE EXCEPTION 
                'El smartphone % no se encuentra en el cc, a las % se detecto en el local %'
                ,NEW.idsmartphone,NEW.fechaentrada,NEW.idlocal;
        END IF;
        RETURN NEW;
    END; $$
LANGUAGE plpgsql;

CREATE TRIGGER verificarsmartphoneinlocalincctrig
BEFORE INSERT ON recorrido
FOR EACH ROW EXECUTE PROCEDURE verificarsmartphoneinlocalincc();