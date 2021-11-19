**NOMBRE DE LA INTEGRACIÓN O DEL API**

**Área:** Soluciones de Clientes

**Analista Ágil:** Juan Guillermo Montoya

**Dominio:** Clientes

**Proyecto:** Móvil Éxito

**Palabras Clave:** redención, PCO, acumulación

**Infraestructura de despliegue:** AKS,OKS, GCP, ODI, OSB

**Sistemas Origen:** Clifre, Teradata, Sinco 

**Sistemas Destino:** Clifre, Teradata, Sinco, Kafka

**Tipo desarrollo:** Api, Worker, Batch, Modelo, Portal Web, Móvil ** main-pipeline.yml

**Versión Lenguaje:** NetCore, Java, Angular, Python, R

**URL Consumo Api:** https://wolframio.grupo-exito.com/apiew/producto/v1/HLZKHMELSEVH/swagger/index.html

#### Tabla de contenido

- [Descripción de la necesidad](#descripción-de-la-necesidad)
- [Diagrama de la necesidad](#diagrama-de-la-necesidad)
- [Clasificacion de las Interfaces](#clasificacion-de-las-interfaces)
- [Atributos de calidad de la solucion](#atributos-de-calidad-de-la-solucion)
- [Diagrama de componentes de la Interfaz](#diagrama-de-componentes-de-la-interfaz)
- [Consideraciones](#consideraciones)
- [Mapeo de datos](#mapeo-de-datos)
  - [Mapeo Movil_Exito_Bolsillo](#mapeo_movil_exito_bolsillo)
  - [Mapeo Movil_Exito_Gestores](#mapeo_movil_exito_gestores)
  - [Mapeo Movil_Exito_Tipoajuste](#mapeo_movil_exito_tipoajuste)
- [Características técnicas de la Interfaz](#características-técnicas-de-la-interfaz)
- [Manejo de Errores](#manejo-de-errores)
- [Manejo de reproceso](#manejo-de-reproceso)
- [Manual de despliegue](#manual-de-despliegue)

* [Inventario de Artefactos](#inventario-de-artefactos)
* [Topologías](#topologías) 
* [Directorios](#directorios)
* [Operaciones de la Interfaz (Servicio)](#Operaciones-de-la-Interfaz-(Servicio))

#### Descripción de la necesidad

En esta sección, se debe especificar cual es la necesidad del negocio que se quiere solucionar, para describir la necesidad de acuerdo a los siguientes ítems:

| **Nombre de la interfaz:** | **NOMBRE DE LA INTERACIÓN O API**                            |
| -------------------------- | ------------------------------------------------------------ |
| **Qué**                    | Especifique la necesidad que se quiere solucionar            |
| **Porqué**                 | Especifique el por qué se necesita solucionar la necesidad   |
| **Para que**               | Especifique el objetivo que se desea alcanzar con la solución a implementar. |

#### Diagrama de la necesidad

A continuación mostramos algunos ejemplos:

![Diagrama](./Documentacion/diagrama-necesidad.png)

![Diagrama](./Documentacion/diagrama-necesidad-actividades.png)

- Especifique las notas puntales que sean relevantes para el proceso.
- Identifique las integraciones del diagrama de la necesidad y defina cuales están al alcance de este desarrollo.
- Una vez identificadas las integraciones dentro del alcance, defina una breve descripción de estas integraciones.



#### Atributos de calidad de la solución

Estas preguntas se puedes realizar enfocadas en el proceso de negocio que se está analizando para identificar los atributos de calidad:

1.	¿Con qué frecuencia se generan los mensajes o registros en un día?
2.	¿Qué cantidad de registros o mensajes se generan?
3.	¿Cuál es el crecimiento esperado para la generación de estos registros o mensajes?
4.	¿Cuánto tiempo se necesita para ejecutar el proceso?
5.	¿Cuál es el tiempo en que se espera tener la información?
6.	¿Cómo se comporta la información en un evento especial? En promociones, un día, hora en particular?

En el siguiente link se encuentra una guía de preguntas....

En la siguiente tabla se relacionan los atributos de calidad asociados a la solución:

| **Seguridad**                                                |                 |      |
| ------------------------------------------------------------ | --------------- | ---- |
| **Característica**                                           | **Observación** |      |
| Identificación y Autenticación                               |                 |      |
| Autorización                                                 |                 |      |
| Confidencialidad                                             |                 |      |
| Integridad                                                   |                 |      |
| Auditabilidad                                                |                 |      |
| **Desempeño**                                                |                 |      |
| **Característica**                                           | **Observación** |      |
| Transacciones por Segundo                                    |                 |      |
| Tiempo de Respuesta Máximo en Segundos                       |                 |      |
| Tiempo de Respuesta Promedio en Segundos                     |                 |      |
| Frecuencia                                                   |                 |      |
| Registros entregados en orden                                |                 |      |
| **Escalamiento**                                             |                 |      |
| **Característica**                                           | **Observación** |      |
| Cantidad Estimada de Transacciones por Día/Mes/Año           |                 |      |
| Porcentaje de Crecimiento Estimado de Transacciones por Día/Mes/Año (%) |                 |      |
| **Disponibilidad**                                           |                 |      |
| **Característica**                                           | **Observación** |      |
| Horario de Disponibilidad de la Solución                     |                 |      |
| Contingencia                                                 |                 |      |
| **Manejo de errores**                                        |                 |      |
| **Característica**                                           | **Observación** |      |
| Trazabilidad                                                 |                 |      |
| Endpoint o Partition Key                                     |                 |      |
| Errores                                                      |                 |      |
| Alertamiento                                                 |                 |      |
| Monitoreo                                                    |                 |      |
| Reintentos                                                   |                 |      |

#### Diagrama de componentes de la Interfaz

En el siguiente diagrama de componentes se muestra el diseño de la integración y la relación con los diferentes componentes:
Diagrama ejemplo para ODI:

![Diagrama](./Documentacion/diagrama-arquitectura.png)

Diagrama ejemplo para Azure:

![Diagrama](./Documentacion/diagrama-arquitectura-azure.png)

| **Nombre Componente**          | **Descripción del componente** | **Responsabilidad**                                          | **Tipo** | **Herramienta**      |
| ------------------------------ | ------------------------------ | ------------------------------------------------------------ | -------- | -------------------- |
| Bolsillo                       | Tabla fuente de SIME           | Almacena la información de SIME con respecto a los Bolsillos | Tabla    | Microsoft SQL Server |
| TipoBolsillo                   | Tabla fuente de SIME           | Almacena la información de SIME con respecto a los TipoBolsillos | Tabla    | Microsoft SQL Server |
| Gestor                         | Tabla fuente de SIME           | Almacena la información de SIME con respecto a los Gestores  | Tabla    | Microsoft SQL Server |
| TipoAjuste                     | Tabla fuente de SIME           | Almacena la información de SIME con respecto a los TipoAjustes | Tabla    | Microsoft SQL Server |
| PKG_SIME_TERA                  | Paquete principal de ODI.      | Paquete el cual invoca la ejecución de los paquetes PKG_SIME_TERA_BOLSILLO,  PKG_SIME_TERA_GESTORES y PKG_SIME_TERA_TIPOAJUSTE | Paquete  | ODI                  |
| PKG_SIME_TERA_BOLSILLO         | Paquete secundario de ODI.     | Paquete de ODI encargado de transportar la información de los bolsillos desde la aplicación SIME hacia Teradata. | Paquete  | ODI                  |
| PKG_SIME_TERA_GESTORES         | Paquete secundario de ODI.     | Paquete de ODI encargado de transportar la información de los gestores desde la aplicación SIME hacia Teradata. | Paquete  | ODI                  |
| PKG_SIME_TERA_TIPOAJUSTE       | Paquete secundario de ODI.     | Paquete de ODI encargado de transportar la información de los tipos de ajuste desde la aplicación SIME hacia Teradata. | Paquete  | ODI                  |
| DEFINED_VALUE_TYPE_NEW         | Tabla destino Teradata         | Tabla de TERADATA que almacena los datos de Bolsillos junto con los Tipos de bolsillos | Tabla    | Teradata             |
| GESTORES_TELEFONIA_NEW         | Tabla destino Teradata         | Tabla de TERADATA que almacena los datos de Gestores telefonia | Tabla    | Teradata             |
| TIPO_AJUSTE_RECARGAS_TELEFONIA | Tabla destino Teradata         | Tabla de TERADATA que almacena los datos de los ajustes de las recargas | Tabla    | Teradata             |



#### Consideraciones 

​	En esta sección especificar  las consideraciones relevantes de la solución a construir.

-	Este diagrama no es necesario cuando se construye un servicio simple, se crearía el diagrama de secuencia.
-	Este diagrama debe contemplar el reproceso de la información y el punto desde donde reenviaría la información.
-	Especificar si es una cola, un servicio que se debe definir.

#### Mapeo de datos

En las siguientes tablas se relacionan el mapeo de datos entre el mensaje interno capa integración y el mensaje de los proveedores de la Interfaz:

| **Mapeo de datos**                                           |                        |                     |                       |                                                  |
| ------------------------------------------------------------ | ---------------------- | ------------------- | --------------------- | ------------------------------------------------ |
| **Nombre del componente:** escriba el nombre del componente  |                        |                     |                       |                                                  |
| **Nombre Del destino:** especifique el nombre del componente destino |                        |                     |                       |                                                  |
| **Enrutamiento:** /                                          |                        |                     |                       |                                                  |
| **Campo Destino**                                            | **Transformación**     | **Origen**          | **Campo Origen**      | **Comentarios**                                  |
| nombre campo destino 1                                       | tipo de transformación | Tipo campo origen 1 | Nombre campo origen 1 | Especifique algun comentario releventa del campo |

#### Características técnicas de la Interfaz (Aplica para integraciones ODI)

Las hojas técnicas de infraestructura son relacionadas en la siguiente tabla:

| **Características Técnicas Desarrollo** |                          |                               |          |             |              |                        |
| --------------------------------------- | ------------------------ | ----------------------------- | -------- | ----------- | ------------ | ---------------------- |
| **Sistema**                             | **Tipo**                 | **Host**                      | **Port** | **Usuario** | **Password** | **Nombre del recurso** |
| Staging de ODI                          | Base de datos            | OSBDLLODB                     | 1541     | ODIV12213   |              | ODIDEV12               |
| Servidor de aplicaciones de ODI         | Servidor de aplicaciones | ODIDLLO                       |          |             |              |                        |
| SIME                                    | Base de datos            | 296SQLP03                     | 1433     | usrodidev   |              | SIME_CUBE              |
| TERADATA                                | Base de datos            | exitocol6-3-2.grupo-exito.com |          | usrodidev   |              | bd_rdb                 |



| **Características Técnicas Calidad** |                          |                               |          |             |              |                        |
| ------------------------------------ | ------------------------ | ----------------------------- | -------- | ----------- | ------------ | ---------------------- |
| **Sistema**                          | **Tipo**                 | **Host**                      | **Port** | **Usuario** | **Password** | **Nombre del recurso** |
| Staging de ODI                       | Base de datos            | BDQA                          | 1521     | ODIV12213   |              | ODIQASTG               |
| Servidor de aplicaciones de ODI      | Servidor de aplicaciones | odiqa01                       |          |             |              |                        |
| SIME                                 | Base de datos            | 296SQLP03                     | 1433     | usrodiqa    |              | SIME_CUBE              |
| TERADATA                             | Base de datos            | exitocol6-3-2.grupo-exito.com |          | usrodiqa    |              | bd_rdb                 |

**Nota: las aplicaciones SIME y TERADATA no cuentan con ambiente de calidad.**

Esta integración esta orquestada por OPCON:

| **Parámetros OPCON**      |                                        |             |             |
| ------------------------- | -------------------------------------- | ----------- | ----------- |
| **Nombre de la Malla**    | NFORMACION-MAESTRAS-MOVIL-EXITO-A-TERA |             |             |
| **Tipo de Ejecución**     | Secuencial                             |             |             |
| **Frecuencia**            | Diario - 8:00 am - 12:00 pm - 5:00 pm  |             |             |
| **Escenario**             | **Proyecto**                           | **Fuente**  | **Destino** |
| PKG_SIME_TERA_BOLSILLO    | MOVIL EXITO                            | BOLSILLOS   | TERADATA    |
| PKG_SIME_TERA_GESTORES    | MOVIL EXITO                            | GESTORES    | TERADATA    |
| PKG_SIME_TERA_TIPOAJUSTES | MOVIL EXITO                            | TIPO AJUSTE | TERADATA    |

#### Manejo de Errores  (Aplica para integraciones ODI)

|                | **Si/No** | **Cómo se realiza**                                    |
| -------------- | --------- | ------------------------------------------------------ |
| Notificaciones | Si        | A través de Opcon                                      |
| Reintentos     | Si        | Se ejecuta de nuevo el proceso manualmente desde Opcon |
| Trazabilidad   | Si        | En la tabla TBL_TRAZABILIDAD_ODI del satging de ODI.   |
| Contingencia   | No        |                                                        |

#### Manejo de reproceso  (Aplica para integraciones ODI)

Especificar los puntos en que se debe hacer el reproceso y cómo hacerlo.

| **Punto**                 | **Como se reprocesa**                                       | **Aplicabilidad** |
| ------------------------- | ----------------------------------------------------------- | ----------------- |
| PKG_SIME_TERA_BOLSILLO    | Se debe ejecutar manualmente el paquete de ODI desde Opcon. |                   |
| PKG_SIME_TERA_GESTORES    | Se debe ejecutar manualmente el paquete de ODI desde Opcon. |                   |
| PKG_SIME_TERA_TIPOAJUSTES | Se debe ejecutar manualmente el paquete de ODI desde Opcon. |                   |

**Documentación del Api:** a continuación se comparte la URL con la especificación técnica del Api

**URL Consumo Api:** https://wolframio.grupo-exito.com/apiew/producto/v1/HLZKHMELSEVH/swagger/index.html



**Depuración de Archivos** (Validar si ponerlo en el MAOS)

...



### Instructivo despliegue

###### Prerequisitos:

1. Creación de BD en Calidad y Producción, validar versiones entre ambientes.

   **Nota: Cómo validar las conexiones entre sistemas por ambientes, ambiente preproductivo.**

2. Creación y validación de conexión de usuarios genéricos para:

   - BD
   - Mongo
   - Rabbit

3. Ejecutar los scripts en bases de datos en el siguiente orden:

   - scripts

4. Setear en la librería stage-nombre-libreria  las variables para ambiente caliad y producción:

   - variable1
   - variable2
   - variable3

3. Ajustar los recursos necesarios para los namespaces de calidad y producción basado en informe de consumo de recursos, autoescalamientos, etc.
4. Creación de Path par Logs y Archivos



