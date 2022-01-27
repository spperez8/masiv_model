masiv_model
==============================

## Introducción

Un establecimiento de comercio en línea ha dispuesto un conjunto de datos transaccionales, los cuales corresponden a todas las transacciones que se realizaron entre diciembre de 2010 y diciembre de 2011. El conjunto de datos "Online Retail" puede descargarse desde la siguiente dirección electrónica: <https://archive.ics.uci.edu/ml/datasets/Online%20Retail>. En este repositorio encontrará una mejor y más detallada descripción de los datos.

## Requerimientos del negocio

En primer lugar, la compañía está interesada en entender el comportamiento (transaccional) de sus clientes. Para tal fin, se requiere realizar una segmentación de clientes a fin de identificar desde los mejores clientes hasta aquellos que ya no son clientes. ¿Acaso también se podrá realizar un pronóstico del número de transacciones que realizaron los clientes en el período de diciembre de 2011 a diciembre de 2012? De ser así, ¿se podrá pronosticar cuánto dinero gastaron los clientes en tales transacciones? (Obsérvese que los datos no comprenden transacciones en el período 2011 - 2012).

Por otro lado, la compañía está también interesada en incrementar sus ventas y el monto de las mismas ("cross selling" y "up selling", respectivamente). El gerente, un asiduo lector de "Fortune", ha [sabido](http://fortune.com/2012/07/30/amazons-recommendation-secret/) que parte significativa de las ventas de Amazon se debe a las recomendaciones de productos. Por lo tanto, le solicita implementar un sistema de recomendación de productos teniendo en cuenta las características de los datos provistos.

Organización del proyecto
------------
    ├── README.md
    ├── data
    │   ├── external       
    │   ├── interim        
    │   ├── processed      
    │   └── raw            
    │
    ├── notebooks
    │
    ├── references
    │
    ├── reports            
    │   └── figures 
    │
    ├── requirements.txt   
 --------
