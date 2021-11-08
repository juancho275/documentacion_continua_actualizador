#### Nombre de la integración o del API

kc-audiencia-encabezado

**DUEÑO FUNCIONAL DE LA SOLUCIÓN**

| **Área**     | Soluciones Inteligencia de Negocio |
| ------------ | ------------------------------------ |
| **Contacto** | CLIFRE-Julian Alvarez    |
|              | Kafka-Lina Muñoz   |


#### Tabla de contenido

- [Descripción de la necesidad](#descripción-de-la-necesidad)
- [Diagrama de la necesidad](#diagrama-de-la-necesidad)
- [Atributos de calidad de la solución](#Atributos-de-calidad-de-la-solución)
- [Diagrama de componentes de la Interfaz](#Diagrama-de-componentes)
- [Mapeo de datos](#mapeo-de-datos)
- [Características técnicas de la Interfaz](#características-técnicas-de-la-interfaz)
- [Manejo de Errores](#manejo-de-errores)
- [Manejo de reproceso](#manejo-de-reproceso)
- [Manual de despliegue](#manual-de-despliegue)

* [Directorios](#directorios)

#### Descripción de la necesidad

En esta sección, se debe especificar cual es la necesidad del negocio que se quiere solucionar, para describir la necesidad de acuerdo a los siguientes ítems:

| **Audiencia integrator: ** | **kc-audiencia encabezado**                            |
| -------------------------- | ------------------------------------------------------------ |
| **Qué**                    | Es necesario leer la tabla de dbo.Audiencia de la base de datos CLIFRE de SQL Server para transformar y procesar la informacion de los encabezados de audiencia y disponibilizarlo en un topic de kafka.            |
| **Porqué**                 | Por que se necesita disponibilizar la informacion en el data lake en gcp.   |
| **Para que**               | Para ejecutar modelos analiticos y permitir la consulta de esta informacion que permita nuevos modelos|

#### Diagrama de la necesidad

![](diagrama-secuencia.png)

- Se desarrolla un kafka connect para transoformar y procesar los datos desde la tabla dbo.Audiencia al topic de kafka.

#### Clasificación de las Interfaces

#### Atributos de calidad de la solución




- La tabla de SQL Server puede tener hasta 2.000 registros de audiencia encabezado
- En un caso extremo de consumo de  2.000 de registros el kafka connect tardara un estimado de 4 segundos en verse reflejados los datos en el topic de kafka

En la siguiente tabla se relacionan los atributos de calidad asociados a la solución:

| **Seguridad**                                                |                 |      |
| ------------------------------------------------------------ | --------------- | ---- |
| **Característica**                                           | **Observación** |      |
| Identificación y Autenticación                               |        SI       |      |
| Autorización                                                 |        SI       |      |
| Confidencialidad                                             |        SI       |      |
| Integridad                                                   |        SI       |      |
| Auditabilidad                                                |        SI       |      |
| **Desempeño**                                                |                 |      |
| **Característica**                                           | **Observación** |      |
| Transacciones por Segundo                                    |       500       |      |
| Tiempo de Respuesta Máximo en Segundos                       |        5        |      |
| Tiempo de Respuesta Promedio en Segundos                     |        4        |      |
| Frecuencia                                                   |       24H       |      |
| Registros entregados en orden                                |        SI       |      |
| **Escalamiento**                                             |                 |      |
| **Característica**                                           | **Observación** |      |
| Cantidad Estimada de Transacciones por Día/Mes/Año           |2.000/60.000/720.000|      |
| Porcentaje de Crecimiento Estimado de Transacciones por Día/Mes/Año (%) |                 |      |
| **Disponibilidad**                                           |                 |      |
| **Característica**                                           | **Observación** |      |
| Horario de Disponibilidad de la Solución                     |       24/7      |      |
| Contingencia                                                 |        NO       |      |
| **Manejo de errores**                                        |                 |      |
| **Característica**                                           | **Observación** |      |
| Trazabilidad                                                 |En cola de kafka |      |
| Endpoint o Partition Key                                     |      N/A           |   |
| Errores                                                      |Envío a cola de errores en kafka         |      |
| Alertamiento                                                 |Matriz de escalamiento (MAO's)                  |     |
| Monitoreo                                                    |Validar que se ejecute cada día                 |      |
| Reintentos                                                   | NO                |      |


#### Diagrama de componentes

![](diagrama-arquitectura.png)

| **Nombre Componente**        | **Descripción del componente**                               | **Responsabilidad**                                          | **Tipo**      | **Herramienta** |
| ---------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------- | --------------- |
| dbo.Audiencia| Es la tabla que almacena las audiencias encabezado         | Procesa las audiencias encabezado                         | Tabla       | SQL Server         |
| streaming.clifre.audiencia.encabezado-{ambiente}.               | Es el kafka topic en el que quedan almacenadas las auciencias encabezado. | Contiene las audiencias encabezado                             | Topic         | Kafka           |
| kc-audiencia-encabezado   | Integra las audiencias encabezados de la tabla de SQL Server con kafka  | Este componente se encarga de procesar las audiencias y pasar los registros por una serie de filtros,validaciones y transformaciones para llevar un dato estructurado de audiencias encabezado a un Kafka Topic. Este Kafka Topic permite que otros servicios puedan reaccionar a los eventos de audiencia encabezado en un esquema pub/sub. Este componente es un Kafka connect. | Kafka Connect | Kubernetes      |    


#### Mapeo de datos

En las siguientes tablas se relacionan el mapeo de datos entre el mensaje interno capa integración y el mensaje de los proveedores de la Interfaz:

| **Mapeo de datos**                                           |                        |                     |                       |                                                  |
| ------------------------------------------------------------ | ---------------------- | ------------------- | --------------------- | ------------------------------------------------ |
| **Nombre del componente:** kc-audiencia encabezado  |                        |                     |                       |                                                  |
| **Nombre Del destino:** apache kafka cluster |                        |                     |                       |                                                  |
| **Enrutamiento:** /                                          |                        |                     |                       |                                                  |
| **Campo Destino**                                            | **Transformación**     | **Origen**          | **Campo Origen**      | **Comentarios**                                  |
| ID                                       | De string a Int | Int | ID | Es el campo que se usa como key en el registro del topic |
| Nombre                                       | N/A | String | Nombre | N/A |
| IDTipo                                       | N/A | Int | IDTipo | N/A |
| IDEstado                                       | N/A | Int | IDEstado | N/A |
| FechaInicial                                       | De date a String | date | FechaInicial | Fue necesario hacer una transfomacion de tipo de dato|
| FechaFinal                                       | De date a String | date | FechaFinal | Fue necesario hacer una transfomacion de tipo de dato |

#### Mapeo de datos

![](encabezado-sql-server.png)

#### Mensaje en el topic

```
1:{"ID":1,"Nombre":"DEV OKS","IDTipo":1,"IDEstado":1,"FechaInicial":"2020-09-12","FechaFinal":"2020-10-14"}
2:{"ID":2,"Nombre":"prueba","IDTipo":1,"IDEstado":1,"FechaInicial":"2020-04-10","FechaFinal":"2021-05-05"}
3:{"ID":3,"Nombre":"prueba 2","IDTipo":1,"IDEstado":1,"FechaInicial":"2020-04-10","FechaFinal":"2020-05-04"}
4:{"ID":4,"Nombre":"prueba 3","IDTipo":1,"IDEstado":1,"FechaInicial":"2020-04-10","FechaFinal":"2020-05-03"}
5:{"ID":5,"Nombre":"prueba 4","IDTipo":1,"IDEstado":1,"FechaInicial":"2020-04-10","FechaFinal":"2020-05-02"}
```

#### Características técnicas de la Interfaz

| **Características Técnicas Desarrollo** y QA |                             |          |          |             |              |                                             |
| -------------------------------------------- | --------------------------- | -------- | -------- | ----------- | ------------ | ------------------------------------------- |
| **Sistema**                                  | **Tipo**                    | **Host** | **Port** | **Usuario** | **Password** | **Nombre del recurso**                      |
| Kafka                                        | Streaming platform          | 10.2.97.145,10.2.97.168,10.2.97.177         |      9092    |             |              | namespace   dev-motor-recomendacion,qa-motor-recomendacion. |
| Sql server                                        | Base de datos        | 10.2.98.244\backend         |   1428       |     usrkafkaqa         |      dx3sdYEiLaHqixr        | namespace   dev-motor-recomendacion,qa-motor-recomendacion. |

#### Manejo de errores

|                | **Aplica** | **Procedimiento**                                     |
| -------------- | --------- | ------------------------------------------------------ |
| Notificaciones | No        |  N/A                                      |
| Reintentos     | No        | N/A                                       |
| Trazabilidad   | Si        | En el topic de reporte "streaming.clifre.audiencia.encabezado-error-{ambiente}".         |
| Manejo fallos  | Si        | Envía los registros corruptos a un dead letter queue   |

#### Manejo de reproceso

Especificar los puntos en que se debe hacer el reproceso y cómo hacerlo.

| **Punto**    | **Como se reprocesa**       | **Aplicabilidad** |
| ------------ | --------------------------- | ----------------- |
| Kafka connect| Por definir con operaciones |                   |

#### Manual de despliegue

#### Inventario de Artefactos

| **Tipo de artefacto** | **Nombre del artefacto**    | **Descripción**                                              |
| --------------------- | --------------------------- | ------------------------------------------------------------ |
| Código fuente         | kc-audiencia-encabezado     | Contiene el código fuentes del kafka connect       |

#### Prerrequisitos

Es importante que antes de hacer el despliegue se tengan en cuenta las siguientes consideraciones:

1. Los Kafka topics deben estar creados.
   1. streaming.clifre.audiencia.encabezado-{ambiente}
2. Debe estar creado el namespace en k8s.
   1. {ambiente}-motor-recomendacion
3. Usuario de base de datos para CLIFRE

- Asignación de los valores adecuados para el micro servicio

| Namespace     | Ambiente   | MemoryLimits | CpuLimits |
| ------------- | ---------- | ------------ | --------- |
| dev-motor-recomendacion | Desarrollo | 1000Mi        | 1000m      |
| qa-motor-recomendacion  | QA         | 1000Mi        | 1000m      |
| pnd-motor-recomendacion | Producción | 1000Mi        | 1000m      |

- Validación de las variables y propiedades de los pipelines.



##### Pipelines

| Yaml            | Ruta             |
| --------------- | ---------------- |
| deployment.yaml | charts\templates |
| monitoring.yaml | charts\templates |
| Chart.yaml      | charts           |
| values-dev.yaml | charts           |
| values-qa.yaml  | charts           |
| values-pdn.yaml | charts           |

Estas son las variables que se deben modificar en cada despliegue con los datos correspondientes al ambiente donde se realiza dicho despliegue.

| Variables                         | Descripción                                            |
| --------------------------------- | ------------------------------------------------------ |
| aplicacion                        | Nombre del microservicio                               |
| area.negocio                      | Area de negocio del microservicio                      |
| area.ti                           | Area ti del microservicio                              |
| cpu.limits                        | Limite de cpu del pod                                  |
| cpu.request                       | Request de cpu del pod                                 |
| deployType                        | Tipo de depliegue del pod                              |
| image.name                        | Nombre de la imagen docker                             |
| max.replicas                      | Numero maximo de replicas                              |
| memorylimits                      | Limite de memoria del pod                              |
| memoryrequest                     | Request de memoria del pod                             |
| min.replicas                      | Minimo de replicas para el pod                         |
| namespace                         | Nombre del namespace donde se despliega el pod         |
| pais                              | Nombre del país                                        |
| prefix                            | Prefijo del nombre del topic                           |
| replicas                          | Numero de replicas del pod                             |
| sql.clifre.database               | Nombre de la base de datos de donde se leeran los datos|
| sql.clifre.hostname               | Host donde esta la base de datos                       |
| sql.clifre.password               | Contraseña del usuario de la base de datos             |
| sql.clifre.port                   | Puerto por donde se conectara a la base de datos       |
| sql.clifre.username               | Nombre del usuario de la base de datos                 |
| topic                             | Nombre del topico de kafka                             |
| topic.error                       | Nombre del topico de error de kafka                    |

#### Inventario de Artefactos

| Tipo de artefacto | **Nombre del artefacto** | **Descripción**                                              |
| ----------------- | ------------------------ | ------------------------------------------------------------ |
| Micro servicio    | kc-audiencia-encabezado        | Micro servicio que contiene el desarrollo del kafka connect ejecutado por el OKS (Azure Kubernetes Service) |
|                   |                          |                                                              |


#### Secuencia de ejecución de despliegue de Artefactos

| **Secuencia** | **Tipo de artefacto** | **Nombre del artefacto** | **Servidor** | **Observaciones**                                            |
| ------------- | ----------------- | ------------------------ | ------------ | ------------------------------------------------------------ |
| 1             | Micro servicio    | kc-audiencia-encabezado        | OKS-PDN      | Se debe aprobar el pull request del repositorio y verificar que se ejecute el pipeline release kc-audiencia-encabezado |
|               |                   |                          |              |                                                              |


### **Monitoreo**
    |


#### Comportamientos Atípicos de la integración

| Comportamiento                                               | Acción                                     |
| ------------------------------------------------------------ | ------------------------------------------ |
| Llenado del topic de erro de kafka | Notificar y/o escalar al área responsable. |


## Campos extras

Dominio: Puntos Colombia100

Palabras Clave: redencion,PCO,acomulacion

Proyecto: Movil Exito Recarga Paquetes

Area: Soluciones de Clientes

Analista agil: Juan Guillermo Montoya


## Infrestructura Despliegue

Sistemas Origen: Clifre

Sistemas Destino: Kafka

Tipo desarrollo: Api

Version Lenguaje: NetCore

URL: https://wolframio.grupo-exito.com/apiew/producto/v1/HLZKHMELSEVH/swagger/index.html

Infra despliegue: AKS,OKS,GCp,OKS2

