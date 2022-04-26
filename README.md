# Proyecto de la materia CI-37255 Traductores e Interpretadores

Implementación de un simple REPL de Stókhos (del griego στόχος) escrito en python.

## Integrantes Dacary:  
- Gregory Muñoz   16-11313  
- Daniela Ramirez 16-10940  
- Giancarlo Dente 15-10395

### Requerimientos:

* Python 3.8.10 o superior.
* Libreria PLY ya viene incluida en este repositorio y no es necesario descargar por otro medio.

### Ejecución

- Si se encuentra en Windows puede ejecutar el programa dando doble click al archivo "run.BAT", se abrirá la CMD y podrá ingresar los comandos que desee probar (ver ejemplos de ejecución). No es necesario tener la CMD abierta. El "run.BAT" ejecuta el comando 'python REPL.py'. Este archivo debe mantenerse dentro de la carpeta del proyecto para su correcto funcionamiento.

- Otra manera de ejecutar el programa es, dependiendo de su version de python y/o cómo este configurado en el PATH de Windows, Linux o macOS. Escriba uno de los siguientes comandos:

```bash
$ python REPL.py 
```
o  
```
$ python3 REPL.py
```
     
### Ejemplos de ejecucion en REPL

- Luego de ejecutar el REPL se podrán utilizar los diversos comandos ya descritos en etapa1.pdf, etapa2.pdf, etapa3.pdf y etapa4.pdf. A continuación se muestran ejemplos de los comandos que puede ingresar:

```bash
<Dacary> .lex num pi := 3.141592654
<Dacary> .load full
<Dacary> .failed
<Dacary> .reset
<Dacary> .ast 5*4-3+2/1
<Dacary> num x := 34+12;
<Dacary> x := 34;
<Dacary> [num] arreglo := [3,5,6];
<Dacary> [bool] booleanos := [true,false,5>3];
<Dacary> if(2<6,true,false)
<Dacary> type(-24324)
<Dacary> ltype(arreglo)
<Dacary> floor(pi())
<Dacary> length(booleanos)
<Dacary> sum(arreglo)
<Dacary> avg(arreglo)
<Dacary> ln(23)
<Dacary> exp(234)
<Dacary> sin(2*uniform())
<Dacary> cos(45)
<Dacary> tan(23)
<Dacary> formula(arreglo[1])
<Dacary> tick()
<Dacary> now()
```
