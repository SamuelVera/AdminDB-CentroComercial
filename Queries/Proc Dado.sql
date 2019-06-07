CREATE OR REPLACE FUNCTION proc0(idlocal INT, cicomprador INT, monto INT, idfactura INT)
	RETURNS VOID AS $$
	DECLARE entrada TIMESTAMP WITHOUT TIME ZONE;
	DECLARE macaddress VARCHAR(40);
	BEGIN
    	SELECT e.fechaentrada INTO entrada
        FROM estadia AS e
        	INNER JOIN factura AS f ON f.idsmartphone = e.idsmartphone
        WHERE f.numero = idfactura
        	AND e.fechasalida IS NULL
        ORDER BY e.fechaentrada DESC
        LIMIT 1;

    	SELECT s.macaddress INTO macaddress
    	FROM smartphone AS s
    		INNER JOIN factura AS f ON f.idsmartphone = s.id
	    WHERE f.numero = idfactura;
		
		INSERT INTO facturaespecial(macaddress, entrada, monto, cicomprador, idfactura, idlocal)
	    VALUES (macaddress, entrada, monto, cicomprador, idfactura, idlocal);
		
	END; $$
LANGUAGE plpgsql;