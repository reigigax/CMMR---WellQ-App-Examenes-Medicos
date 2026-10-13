# Caracteristicas de la Base de Datos

##  Columnas

> ###     Identity Columns    (https://www.postgresql.org/docs/18/ddl-identity-columns.html)
>> An identity column is a special column that is generated automatically from an implicit sequence.
>> 
>> #### *** Asignar al valor que sea `Autoincrementable` cada que se registre un nuevo valor ***

> ###     Collations          (https://medium.com/@adarsh2801/understanding-collations-in-postgresql-648e4fa333e1)
>> Collations are set of rules that define how characters/strings are compared and ordered in PostgreSQL.
>> 
>> #### *** No es necesario para todas las tablas, solo define el orden en el que se mostraran los datos de dicha columna ***


> ###      Storage Types      (https://medium.com/@udbhavsinghnitw/storages-in-postgresql-7ed53b5a4fe8)
>> In PostgreSQL, every column in a table has a storage type associated with it. This tells the database how the column’s data should be stored on disk.
>>
>> #### *** El tipo de storage define como se almacenar cada registro en el disco (principalmente para la mejora del rendimiento y el manejo del espacio) ***
>>
>> - PLAIN      store direclty on the row           *** Su mejor uso es para datos simples como INTEGER, BOOLEAN, etc ***
>> - MAIN       store in the row (unless large)     *** Se usa para Tipos de Datos Largos, de los cuales deja lo mas posible registrado, osea sersi el valor que se registra sobrepasa el limite definido se agragara todo lo posible de ese valor ***
>> - EXTENDED   compression + store out-of-row      *** Utilizado principalmete para datos largos o complejos como JSON, XML, VARCHAR, TEXT y BYTEA ***
>> - EXTERNAL   store out-of-row, no compression    *** Lo mismo que el Extended pero este no aplica la compresion de los archivos o datos, util para almacenar Imagenes, PDF's  ***
