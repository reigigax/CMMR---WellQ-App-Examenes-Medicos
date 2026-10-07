# Pasos para Realizar Acciones en GitHub

## IMPORTANTE: Todos estos comandos de git que ejecutes deben de ser en la carpeta RAIZ del proyecto, osea ser, 
##             la carpeta donde estan todas las demas carpetas de las otras fases, esto es necesario saberlo
##             para no generar algun conflicto con el estado de los archivos.
##
##             Lo mas probable es que la carpeta raiz al clonar el repositorio sea la carpeta "CMMR---WellQ-App-Examenes-Medicos",
##             asi que desde esa carpeta se deberan de ejecutar los comandos de git, esto se puede verificar
##             en la terminal de Visual Studio donde aparecera al final el nombre de la carpeta de esta manera
##             `....\CMMR---WellQ-App-Examenes-Medicos>`

#### - Asignar un repositorio -
##### Este comando nos permite definir a que repositorio al que estaremos mandando los archivos o cambios realizados
> 1. git init
> 2. git remote add origin { link del repositorio } ( en nuestro caso `https://github.com/reigigax/CMMR---WellQ-App-Examenes-Medicos`) 


#### - Traer todos los archivos de un repositorio -
##### Hay que tomar en cuenta que los archivos te lo dejara en una carpeta con el nombre de dicho repositorio
> ***Luego de clonar el repositorio se debe de abrir Visual Studio desde la carpeta '',***
> ***esto para evitar lo mencionado en el IMPORTANTE***
>> 1. git clone { link del repositorio } ( en nuestro caso `https://github.com/reigigax/CMMR---WellQ-App-Examenes-Medicos`)


#### - Revisar si hay cambios subidos en el repositorio -
##### Este comando es para saber si es que aguen subio algun cambio a la rama principal 
> ***si indica 'Your branch is up to date' significa que los archivos que presentas son los mismos que hay en el repositorio,***
> ***pero si indica 'Your branch is behind origin main by 'X' commits' significa que hay modificaciones en archivos que presentas en el repositorio***
>> 1. git status

#### - Realizar commits -
##### Estos commits se guardan y se mostraran en el repositorio luego de subirlos al repositorio
> 1. git init
> 2. git add .
> 3. git commit -m "{ mensaje de lo realizado o modificado }"


#### - Subir archivos o cambios al repositorio principal -
> 1. git init
> 2. git add .
> 3. git commit -m "{ mensaje de lo realizado o modificado }"
> 4. git push -u origin main


#### - Subir archivos o cambios al repositorio principal -
> 1. git init
> 2. git add .
> 3. git commit -m "{ mensaje de lo realizado o modificado }"
> 4. git push -u origin { nombre de la rama }


#### - Crear nuevas ramas en el repositorio -
##### Esto se puede realziar de 2 maneras
> ***La primera manera te creara la rama y te movera directamente a dicha rama***
>> 1. git init
>> 2. git checkout -b { nombre de la rama }

> ***La segunda manera te creara la rama pero no te moveras a ella hasta que realices el comando "git checkout { nombre de la rama }"***
>> 1. git init
>> 2. git branch { nombre de la rama }


#### - Cambiarse entre ramas -
##### Te permite moverte entre ramas existentes
> 1. git init
> 2. git checkout { nombre de la rama }

#### - Ver en cual rama nos ubicamos -
##### Este comando te permite saber en que rama te encuentras actualmente ( esto indicado por un '*' )
> 1. git branch 

#### - Aplicar cambios realizados en una rama a la rama actual de trabajo -
##### Esto lo que hace es traer los cambios de la rama que mencionas en el comando a tu rama actual
> ***Un ejemplo: si te encuentras el una rama llamada 'login_01' y necesitas traer cambios realizados en la rama principal del proyecto***
> ***tendras que escribir el comando de la siguiente manera ***`git pull main`*** esto traera los cambios hechos en la rama main a la rama login_01***
>> 1. git pull { nombre de la rama }
