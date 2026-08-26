# Guia de Comandos de GitHub
### Estos comandos nos serviran para trabajar con ramas para subir avances u archivos del proyecto
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
---