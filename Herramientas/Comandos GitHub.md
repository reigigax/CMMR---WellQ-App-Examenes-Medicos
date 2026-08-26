# Guia de Comandos de GitHub
##### Estos comandos nos serviran para trabajar con ramas para subir avances u archivos del proyecto
---
### Commandos Escenciales

##### | Links de Informacion:
##### | (1 - 2) https://git-scm.com/book/es/v2/Fundamentos-de-Git-Obteniendo-un-repositorio-Git
##### | (3 - 4) https://git-scm.com/book/es/v2/Fundamentos-de-Git-Guardando-cambios-en-el-Repositorio
##### | (5) https://git-scm.com/book/es/v2/Fundamentos-de-Git-Deshacer-Cosas
##### | (6 - 7) https://git-scm.com/book/es/v2/Fundamentos-de-Git-Trabajar-con-Remotos
##### | (8) https://git-scm.com/book/es/v2/Ramificaciones-en-Git-Procedimientos-B%C3%A1sicos-para-Ramificar-y-Fusionar

---
#### 1.- ***git init***
> Este comando nos sirve para iniciar el programa de GitHub en el proyecto actual *(se recomienda usarlo al principio de la subida de archivos)*

#### 2.- ***git add {nombre de archivo o carpeta}***
> Este comnado se utiliza para seleccionar que archivos se subiran a la rama o repositorio de destino.
>
> Se pueden seleccionar de uno a uno los archivos los cuales se subiran indicando `el nombre del archivo o carpeta`, o por el contrario poner un punto el cual automaticamente seleccionara todos los archivos de la carpeta los cuales sean nuevos o se hayan modificado.

> Ejempos del comando:
>> - **`git add Fase 1`** *(este comando seleccionara todos los archivos de la carpeta `Fase 1`)*
>> - **`git add .`** *(este comando seleccionara los archivos de `la carpeta base que te encuentres`, la carpeta en custion lograndose ver en la terminal)*

#### 3.- ***git commit -m "{mensaje}"***
> Este comando es el cual nos permite confirmar los archivos seleccionados los cuales se agregaran a la rama o repositorio de destino.
>
> En este comando el apartado de `{mensaje}` es necesario que se describa brevemente lo que se agrego o se cambio, ya que este queda registrado en el historial en el GitHub, ademas este mensaje puede ser el mismo independiente de la cantidad de veces que se utilice*

#### 4.- ***git status***
> Este comando nos sirve para visualizar cuales son los archivos los cuales fueron seleccionados para subirse y los archivos que no se han seleccionado aun y oresentan un cambio pendiente por subir. *(principalmente nos puede servir para verificar cuales archivos tenemos confirmados para subir y cuales no)*

#### 5.- ***git reset HEAD***
> Este comando nos permite quitar de la confirmacion un archivo seleccionado previamente. *(nos sirve para quitar algun archivo que no queremos subir porque esta incompleto o no es relevante)* 

#### 6.- ***git remote add origin {link del repositorio}***
> Este comando nos permite definir a que repositorio estaremos mandando los archivos o cambios realizados.
>
> Ejemplo de nuestro caso:
>> - **`git remote add origin https://github.com/reigigax/CMMR---WellQ-App-Examenes-Medicos`**

#### 7.- ***git push -u origin {nombre de la rama}***
> Este comando realiza la subida de archivos previamente seleccionados y confirmados a la rama indicada. 

#### 8.- ***git checkout -b {nombre de la rama}***
> Este comando nos permite crear una nueva rama en el repositorio y de inmediato cambiarnos a esta.

> Este comando es lo mismo que realizar 2 comandos por separados, los cuales son:
>> 1. `git branch {nombre de la rama a crear}` *(crea la rama en cuestion)*
>> 2. `git checkout {nombre de la rama}` *(te cambias de la rama actual a la indicada en {nombre de la rama} )*


---
### Commandos de Manejo de Ramas
##### | Link de Informacion:
##### | (9 - 12) https://git-scm.com/book/es/v2/Ramificaciones-en-Git-Gesti%C3%B3n-de-Ramas
---

#### 9.- ***git branch***
> Este comando nos da una lista de las ramas existentes en el repositorio. *(ademas este indica con un `*` la rama activa o en la que te encuentras)*

#### 10.- ***git branch -v***
> Este comando nos permite ver los ultimos cambios realizados a cada rama existente en el repositorio.

#### 11.- ***git branch -d {nombre de la rama}***
> Este comando nos permite eliminar la rama indicada `solo si esta fue fusionada o juntada con otra rama`. *(solo se debe utilizar en el caso que no se necesite de utilizar mas la rama en cuestion, ejemplo subida de cambios ya realizados o subida de archivos de prueba los cuales fueron reemplazados)*

#### 12.- ***git branch -D {nombre de la rama}***
> Este comando nos permite eliminar la rama indicada `sin requisitos previos`. *(este comando elimina por completo la rama sin requerir de fusionarla o juntarla con otra)*


---
### Comandos de Manejo de Cambios entre Ramas
##### | Link de Informacion:
##### | (13) https://git-scm.com/book/es/v2/Ramificaciones-en-Git-Procedimientos-B%C3%A1sicos-para-Ramificar-y-Fusionar
---

#### 13.- ***git merge {nombre de la rama}***
> Este comando nos permite combinar cambios entre ramas, para realizar esto es necesario irse o estar en la rama la cual le queremos `aplicar los cambios`, *esto se puede realizar con el comando `git checkout`*, luego debemos indicar el nombre de la rama donde se presentan los cambios para asi aplicarlos a la rama correspondiente. *(este comando es importante manejarlo con cuidado ya que este es el que definira si se van a la rama principal los cambios o añadidos realizados)*
>
> Ejemplo de aplicacion de cambios de la rama "parche_01" a la rama principal "main":
>> - **`git branch`** *(este comando nos indicara en que rama estamos indicada por el simbolo `*` que se encontraria al lado izquierdo del nombre de la rama)*
>> - **`git checkout main`** *(este comando se realizaria solo en el caso de que no estubieramos en la rama main)*
>> - **`git merge parche_01`** *(una vez en la rama principal "main" aplicamos este comando el cual traera los cambios trabajados en la rama "parche_01" y los aplicara localmente a la rama principal "main" en la cual nos encontramos, para que se apliquen al repositorio es necesario de realizar un `git push -u origin main`)*


---