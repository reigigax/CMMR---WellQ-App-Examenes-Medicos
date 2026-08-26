# Guia de Comandos de GitHub
##### Estos comandos nos serviran para trabajar con ramas para subir avances u archivos del proyecto
---
### Commandos Escenciales
---
#### ***git init***
> Este comando nos sirve para iniciar el programa de GitHub en el proyecto actual *(se recomienda usarlo al principio de la subida de archivos)*

#### ***git add {nombre de archivo o carpeta}***
> Este comnado se utiliza para seleccionar que archivos se subiran a la rama o repositorio de destino.
>
> Se pueden seleccionar de uno a uno los archivos los cuales se subiran indicando `el nombre del archivo o carpeta`, o por el contrario poner un punto el cual automaticamente seleccionara todos los archivos de la carpeta los cuales sean nuevos o se hayan modificado.

>Ejempos del comando:
>> - **`git add Fase 1`** *(este comando seleccionara todos los archivos de la carpeta `Fase 1`)*
>> - **`git add .`** *(este comando seleccionara los archivos de `la carpeta base que te encuentres`, la carpeta en custion lograndose ver en la terminal)*

#### ***git commit -m "{mensaje}"***
> Este comando es el cual nos permite confirmar los archivos seleccionados los cuales se agregaran a la rama o repositorio de destino.
>
> En este comando el apartado de `{mensaje}` es necesario que se describa brevemente lo que se agrego o se cambio, ya que este queda registrado en el historial en el GitHub, ademas este mensaje puede ser el mismo independiente de la cantidad de veces que se utilice*

#### ***git remote add origin {link del repositorio}***
> Este comando nos permite definir a que repositorio estaremos mandando los archivos o cambios realizados.

> Ejemplo de nuestro caso:
>> - **`git remote add origin https://github.com/reigigax/CMMR---WellQ-App-Examenes-Medicos`**

#### ***git push -u origin {nombre de la rama}***
> Este comando realiza la subida de archivos previamente seleccionados y confirmados a la rama indicada. 

#### ***git checkout -b {nombre de la rama}***
> Este comando nos permite crear una nueva rama en el repositorio y de inmediato cambiarnos a esta.

> Este comando es lo mismo que realizar 2 comandos por separados, los cuales son:
>> 1. `git branch {nombre de la rama a crear}` *(crea la rama en cuestion)*
>> 2. `git checkout {nombre de la rama}` *(te cambias de la rama actual a la indicada en {nombre de la rama} )*

---
### Commandos de Manejo de Ramas
---
#### ***git branch***
> Este comando nos da una lista de las ramas existentes en el repositorio. *(ademas este indica con un `*` la rama activa o en la que te encuentras)*

#### ***git branch -v***
> Este comando nos permite ver los ultimos cambios realizados a cada rama existente en el repositorio.

#### ***git branch -d {nombre de la rama}***
> Este comando nos permite eliminar la rama indicada `solo si esta fue fusionada o juntada con otra rama`. *(solo se debe utilizar en el caso que no se necesite de utilizar mas la rama en cuestion, ejemplo subida de cambios ya realizados o subida de archivos de prueba los cuales fueron reemplazados)*

#### ***git branch -D {nombre de la rama}***
> Este comando nos permite eliminar la rama indicada `sin requisitos previos`. *(este comando elimina por completo la rama sin requerir de fusionarla o juntarla con otra)*
---