# Ejecucion del proyecto (07-10)
#### Aqui se indicaran los pasos e instalaciones necesarias para ejecutar el proyecto

### Software necesario
>   1. Python 3.12 o una más actualizada
>>         Link de descarga (en el raro caso que no lo tengas instalado xd):
>>         `https://www.python.org/downloads/release/python-3120/`
>
>   2. Docker de Escritorio (Docker Desktop)
>>         Link de descarga: `https://docs.docker.com/desktop/setup/install/windows-install/`
>
>
### Instalaciones necesarias
> Lo primero que necesitaremos para poder ejecutar el proyecto es crear un entorno virtual de Python,
> esto principalmente se realiza para que las librerias que ya presentes en tu equipo no afecten en la
> ejecucion y desarrollo de este proyecto.
>
>
> 1. Entorno Virtual
>> - Para crear este entorno virtual primero tendras que ubicarte en la carpeta `Aplicación`.
>> ***Para moverte a dicha carpeta utiliza el comando `cd` y con el tabulador selecciona la carpeta***
>> ***correspondiente hasta llegar a la carpeta.***
>>
>> - Luego en esta carpeta correras el comando `python -m venv .venv`, esto terminara generando una carpeta
>>   con el nombre `.venv`.
>> ***Si este comando no llegara a funcionar prueba cambiando `python` por `python3.12` o `python.exe`***
>> 
>> - Finalmente luego de que se termine de crear esta carpeta `.venv` tendras que ejecutar en la terminal el
>>   comando `.\.venv\Scripts\activate`, esto con el fin de activar este entorno virtual.
>>***Para verificar de que este activo el entorno virtual aparecera `(.venv)` al inicio de la linea de la***
>>***terminal***
>>
>> ## IMPORTANTE: Siempre que quieras trabajar en el proyecto deberas de estar en la carpeta 'Aplicación' y
>> ##             deberas de ejecutar el ultimo paso *(ejecutar el comando `.\.venv\Scripts\activate`)*.
>> ##
>> ##             Ya que de lo contrario el proyecto puede que tenga conflictos con las librerias que puedas
>> ##             tener instaladas en el equipo y no tendra acceso a el entorno virtual donde estaran instaladas
>> ##             las librerias necesarias para que funcione correctamente
>
> 
> El siguiente paso no requeriran de ejecutarse mas de 1 vez, a no ser que se modifique o se aguregen libreiras
> necesarias para otras funciones del proyecto.
>
> 2. Instalacion de Librerias 
>> - Una vez hayas activado el entorno virtual deberas de instalar las librerias necesarias para el proyecto,
>>   para realizar esto debes de encontrarte en la carpeta `Aplicación` y ejecutar en la terminal los siguientes
>>   comandos:
>>   
>>   1. `python.exe -m pip install --upgrade pip`
>>   2. `pip install -r requirements.txt`
>>   
>>   Estos comandos te terminaran de instalar las librerias necesarias para ya solo hacer correr el proyecto
>>
>> ## IMPORTANTE: Si por algun motivo necesitas agregar alguna libreria nueva, (esto sabiendose cuando necesitas
>> ##             de ejecutar el comando `pip install`), debes de realizar el siguiente comando en la terminal para
>> ##             dejar registrada la nueva libreria en el archivo `requirements.txt`:
>> ##
>> ##             pip freeze > requirements.txt
>> ##
>> ##             Este comando registrara todas las librerias instaladas en el archivo de texto mencionado, si no
>> ##             esta activo el entorno virtual dejara registrado todas las librerias instaladas en tu equipo
>> ##             asi que hay que manejar con cuidado este ultimo comando.
>
>
> 3. Ejecutar el proyecto
>> - Por ultimo para ejecutar el proyecto sera necesario de presentar instalado el Docker de Escritorio, lo importante
>>   de este prgrama es que este corriendo en tu computador, ya que si no lo esta no se ejecutara el proyecto.
>>
>>   Una vez verificado de que el Docker de escritorio este corriendo tendras que ejecutar el siguiente comando:
>> 
>>   `docker compose up --build`
>>
>>   Este comando lo que realizara es configurar los contenedores donde se encontraran la base de datos y el contenedor
>>   donde estara corriendo el servidor de la pagina web, la ventaja de correr el proyecto en Docker es que los cambios
>>   que realices se aplicaran automaticaente sin necesidad de volver a correr el servidor.
>
>

### Una vez realizado estos pasos ya podras trabajar en el proyecto, y cuando necesites reiniciar o se te apague el equipo
### deberas de ejecutar solo estos comandos en la terminal ubicado en la carpeta `Aplicación`
### 
###     `.\.venv\Scripts\activate`  ***Activa el entorno virtual***
###     `docker compose up --build` ***Ejecuta la base de datos y el servidor de la pagina (requiere que este corriendo Docker)***
### 
### Ultima vez actualizado el 07-10