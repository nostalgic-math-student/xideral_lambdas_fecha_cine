# xideral_lambdas_fecha_cine
Por Josue Rojas Noble

## Objetivo

Diseñar y publicar una solución de funciones lambda que otorgue formato a la información publicada por los puntos de venta (POS) de un cine dado. 
Esta solución debe formatear bien la fecha y hora al mismo tiempo que publicar los datos en la página index.html

## Funcionamiento de la solución

Tenemos dos lambdas: **json_loader_data** y **lambda_5** (convención de mi perfil para ordenar las prácticas)

La función **json_loader_data** se encarga de formatear los datos cargados al bucket del POS designado, en este ejemplo el nombre es "xideralcinedata".
En este bucket se reciben los datos, y por medio de un trigger de S3 obtenemos la información del archivo en la lambda y lo operamos separando la fecha. 
A su finalización, creamos un archivo de guardado ordenado mediante directorios por año/mes/dia la información procesada en archivo .json y .csv para su futuro manejo.

Después, en la función **lambda_5** se publica una API publica configurada para accesar a los datos ya procesados, esto mediante un formateo de strings se obtiene siempre el archivo de la fecha del día actual. 
Esta API es consumida por otro bucket con una página estática, para que el archivo de visualización "index.html" (anexado para evidencia) se muestre el formato adecuado de la tabla con la información actualizada.



