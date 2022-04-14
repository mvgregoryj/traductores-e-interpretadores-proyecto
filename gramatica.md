# Gramáticas libres de contexto

##  Primera gramática: sintaxis de Stókhos

```bash
<entrada> -> <instruccion> | <expresion> | <funcion>

<instruccion> -> <definicion> | <asignacion>

<definicion> -> <tipo> <identificador> := <expresion> ;
<asignacion> -> <identificador> := <expresion> ;

<tipo> -> <tipoBasico> 
       -> [<tipo>]

<tipoBasico> 
        -> num
        -> bool

<expresion>
        -> <identificador>
        -> <número>
        -> <booleano>
        -> (<expresion>)
        -> [<expresion>]
        -> <identificador>(<expresionLista>)          
        -> <identificador>[<expresion>]          
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

<definicion> -> <tipo> <identificador> TkAssign <expresion> TkSemicolon
<asignacion> -> <identificador> TkAssign <expresion> TkSemicolon

<tipo> -> <tipoBasico> 
       -> TkOpenBracket <tipo> TkCloseBracket

<tipoBasico> 
        -> TkNum
        -> TkBool

<expresion>
        -> <expresionAcotada>
        -> <expresionNormal>

<expresionAcotada>
        -> TkSingleQuote <expresionNormal> TkSingleQuote

<expresionNormal>
        -> <expresionNumerica>
        -> <expresionLogica>
        -> <expresionArreglo>
        -> <expresionFunciones>

<expresionNumerica>
        -> <numero>
        -> <identificador>
        -> TkOpenPar <expresionNumerica> TkClosePar
        -> TkOpenBrace <expresionNumerica> TkCloseBrace
        -> <expresionNumerica> TkPower <expresionNumerica>
        -> TkPlus <expresionNumerica>
        -> TkMinus <expresionNumerica>
        -> <expresionNumerica> TkMult <expresionNumerica>
        -> <expresionNumerica> TkDiv <expresionNumerica>
        -> <expresionNumerica> TkMod <expresionNumerica>
        -> <expresionNumerica> TkPlus <expresionNumerica>
        -> <expresionNumerica> TkMinus <expresionNumerica>

<numero> -> TkNumber

<identificador> -> TkId

<expresionLogica>  
        -> <booleano>
        -> <identificador>
        -> TkOpenPar <expresionLogica> TkClosePar
        -> TkOpenBrace <expresionLogica> TkCloseBrace
        -> TkNot <expresionLogica>
        -> <expresionNumerica> TkLT <expresionNumerica>
        -> <expresionNumerica> TkLE <expresionNumerica>
        -> <expresionNumerica> TkGE <expresionNumerica>
        -> <expresionNumerica> TkGT <expresionNumerica>
        -> <expresionNumerica> TkEQ <expresionNumerica>
        -> <expresionNumerica> TkNE <expresionNumerica>
        -> <expresionLogica> TkEQ <expresionLogica>
        -> <expresionLogica> TkNE <expresionLogica>
        -> <expresionLogica> TkAnd <expresionLogica>
        -> <expresionLogica> TkOr <expresionLogica>   

<booleano>
        -> TkTrue
        -> TkFalse

<expresionArreglo>
        -> TkOpenBracket <expresionArgs> TkCloseBracket
        -> <identificador> TkOpenBracket <expresionNumerica> TkCloseBracket

<expresionArgs>
        -> 
        -> <expresionNormal>  
        -> <expresionNormal> , <expresionArgs>

<funcion>
        -> <identificador> TkOpenPar <expresionArgs> TkClosePar 

        # -> if(<condicion>, <expT>, <expF>)
        # -> type(<expresion>)
        # -> ltype(<expresion>)
        # -> reset()
        # -> uniform()
        # -> floor(<expresionNumerica>)
        # -> length(<expresionArreglo>)
        # -> sum(<expresionNumerica>)
        # -> avg(<expresionNumerica>)
        # -> pi()
        # -> now()

# <condicion>
#         -> <expresionLogica>

# <expT>
#         -> <expresion>

# <expF>
#         -> <expresion>
```