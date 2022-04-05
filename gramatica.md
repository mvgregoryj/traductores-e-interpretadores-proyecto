# Gramáticas libres de contexto

##  Primera gramática: sintaxis de Stókhos

```bash
<entrada> -> <instruccion> | <expresion> | <funcion>

<instruccion> -> <definicion> | <asignacion>

<definicion> -> <tipo> <identificador> := <expresion> ;
<asignacion> -> <identificador> := <expresion> ;

<tipo>
        -> <tipoBasico>
        -> <tipoNoBasico>

<tipoBasico>
        -> num
        -> bool

<tipoNoBasico> -> [<tipoBasico>]

<expresion>
        -> <identificador>
        -> <número>
        -> <booleano>
        -> (<expresion>)
        -> [<expresion>]
        -> <identificador>[<number>]            <!-- Preguntar -->
        -> '<expresion>'
        -> <expresion>^<expresion>
        -> +<expresion>
        -> -<expresion>
        -> !<expresion>
        -> <expresion> * <expresion>
        -> <expresion> / <expresion>
        -> <expresion> % <expresion>
        -> <expresion> + <expresion>
        -> <expresion> - <expresion>
        -> <expresion> < <expresion>
        -> <expresion> <= <expresion>
        -> <expresion> >= <expresion>
        -> <expresion> > <expresion>
        -> <expresion> = <expresion>
        -> <expresion> <> <expresion>
        -> <expresion> && <expresion>
        -> <expresion> || <expresion>   
        -> <expresion> , <expresion>   

<funcion>
        -> if(<condición>, < expT>, < expF>)
        -> type(<exp>)
        -> ltype(<exp>)
        -> reset()
        -> uniform()
        -> floor(<exp>)
        -> length(<exp>)
        -> sum(<exp>)
        -> avg(<exp>)
        -> pi()
        -> now()
```

##  Segunda gramática: Utilizada para la construcción del reconocedor.

```bash
<entrada> -> 
          -> <instruccion> 
          -> <expresion>
          -> <funcion>
          
<instruccion> -> <definicion> | <asignacion>

<definicion> -> <tipo> <identificador> := <expresion> ;
<asignacion> -> <identificador> := <expresion> ;

<tipo>
        -> <tipoBasico>
        -> <tipoNoBasico>

<tipoBasico>
        -> num
        -> bool

<tipoNoBasico>
        -> [<tipoBasico>]

<expresion>
        -> <expresionAcotada>
        -> <expresionNormal>

<expresionAcotada>
        -> '<expresionNormal>'

<expresionNormal>
        -> <expresionNumerica>
        -> <expresionLogica>
        -> <expresionArreglo>

<expresionNumerica>
        -> <numero>
        -> <identificador>
        -> (<expresionNumerica>)
        -> {<expresionNumerica>}
        -> <expresionNumerica>^<expresionNumerica>
        -> +<expresionNumerica>
        -> -<expresionNumerica>
        -> <expresionNumerica> * <expresionNumerica>
        -> <expresionNumerica> / <expresionNumerica>
        -> <expresionNumerica> % <expresionNumerica>
        -> <expresionNumerica> + <expresionNumerica>
        -> <expresionNumerica> - <expresionNumerica>

<expresionLogica>  
        -> <booleano>
        -> <identificador>
        -> (<expresionLogica>)
        -> {<expresionLogica>}
        -> !<expresionLogica>
        -> <expresionNumerica> < <expresionNumerica>
        -> <expresionNumerica> <= <expresionNumerica>
        -> <expresionNumerica> >= <expresionNumerica>
        -> <expresionNumerica> > <expresionNumerica>
        -> <expresionNumerica> = <expresionNumerica>
        -> <expresionNumerica> <> <expresionNumerica>
        -> <expresionLogica> = <expresionLogica>
        -> <expresionLogica> <> <expresionLogica>
        -> <expresionLogica> && <expresionLogica>
        -> <expresionLogica> || <expresionLogica>   

<booleano>
        -> <true>
        -> <false>

<expresionArreglo>
        -> [<expresionArregloLLamada>]
        -> <expresionArregloInstruccion>

<expresionArregloLLamada>
        -> <expresionNormal> , <expresionArregloLLamada>
        -> <expresionNormal>  

<expresionArregloInstruccion>
        -> <identificador>[<expresionNumerica>]

<funcion>
        -> if(<condicion>, <expT>, <expF>)
        -> type(<expresion>)
        -> ltype(<expresion>)
        -> reset()
        -> uniform()
        -> floor(<expresionNumerica>)
        -> length(<expresionArreglo>)
        -> sum(<expresionNumerica>)
        -> avg(<expresionNumerica>)
        -> pi()
        -> now()

<condicion>
        -> <expresionLogica>

<expT>
        -> <expresion>

<expF>
        -> <expresion>
```