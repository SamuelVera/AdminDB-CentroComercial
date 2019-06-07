CREATE OR REPLACE VIEW procentajeventassmartphone AS (
	SELECT round((( SELECT count(*) AS count
           FROM factura
          WHERE factura.idsmartphone IS NULL))::numeric * 100::numeric / (( SELECT count(*) AS count
           FROM factura))::numeric, 2) AS sinsmartphone,
    round((( SELECT count(*) AS count
           FROM factura
          WHERE factura.idsmartphone IS NOT NULL))::numeric * 100::numeric / (( SELECT count(*) AS count
           FROM factura))::numeric, 2) AS consmartphone
);