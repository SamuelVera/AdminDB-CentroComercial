CREATE OR REPLACE VIEW cantidadmesasocupadas AS (
	SELECT count(*) AS mesasocupadas
	FROM monitoreomesa
	WHERE monitoreomesa.fechadesocupado IS NULL
);