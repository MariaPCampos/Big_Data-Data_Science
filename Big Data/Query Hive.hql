-- Cargamos los datos que previamente hemos subido a HDFS en dos tablas externas, una de contratos y otra de comunidades.

CREATE EXTERNAL TABLE contratos (
    codigo_mes int,
    provincia string,
    municipio string,
    total_contratos int,
    contratos_hombres int,
    contratos_mujeres int
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\u003B'
STORED AS TEXTFILE
LOCATION '/user/hive/contratos';


CREATE EXTERNAL TABLE comunidades (
    comunidad_autonoma string,
    provincia string
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\u003B'
STORED AS TEXTFILE
LOCATION '/user/hive/comunidades';

-- Para calcular el resultado, hacemos join de ambas tablas utilizando la columna provincia, agrupamos por comunidad y sumamos
-- las columnas contratos_hombres y contratos_mujeres para obtener el total de contratos por comunidad. Finalmente, utilizamos HAVING para
-- quedarnos con los registros de las comunidades que han hecho más contratos a mujeres que hombres.

SELECT
    comunidad_autonoma,
    sum(contratos_hombres) as num_contratos_hombres,
    sum(contratos_mujeres) as num_contratos_mujeres
FROM contratos
JOIN comunidades 
ON contratos.provincia = comunidades.provincia
GROUP BY comunidad_autonoma
HAVING num_contratos_mujeres > num_contratos_hombres