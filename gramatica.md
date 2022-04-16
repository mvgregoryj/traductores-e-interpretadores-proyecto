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
        -> <número>
        -> <identificador>
        -> (<expresion>)
        -> [<expresion>]
        -> <expresion>^<expresion>
        -> +<expresion>
        -> -<expresion>
        -> <expresion> * <expresion>
        -> <expresion> / <expresion>
        -> <expresion> % <expresion>
        -> <expresion> + <expresion>
        -> <expresion> - <expresion>
        -> <booleano>
        -> !<expresion>
        -> <expresion> < <expresion>
        -> <expresion> <= <expresion>
        -> <expresion> >= <expresion>
        -> <expresion> > <expresion>
        -> <expresion> = <expresion>
        -> <expresion> <> <expresion>
        -> <expresion> && <expresion>
        -> <expresion> || <expresion> 
        -> [<expresion>]
        -> <identificador>[<expresion>]          
        -> <expresion> , <expresion>
        -> <identificador>(<expresion>)     
        -> '<expresion>'

# <funcion>
#         -> if(<condición>, < expT>, < expF>)
#         -> type(<exp>)
#         -> ltype(<exp>)
#         -> reset()
#         -> uniform()
#         -> floor(<exp>)
#         -> length(<exp>)
#         -> sum(<exp>)
#         -> avg(<exp>)
#         -> pi()
#         -> now()
```

##  Segunda gramática: Utilizada para la construcción del reconocedor.

```bash
<entrada> -> 
          -> <instruccion> 
          -> <expresion>
          
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
        -> <numero>
        -> <identificador>
        -> TkOpenPar <expresionNormal> TkClosePar
        -> TkOpenBrace <expresionNormal> TkCloseBrace
        -> <expresionNormal> TkPower <expresionNormal>
        -> TkPlus <expresionNormal>
        -> TkMinus <expresionNormal>
        -> <expresionNormal> TkMult <expresionNormal>
        -> <expresionNormal> TkDiv <expresionNormal>
        -> <expresionNormal> TkMod <expresionNormal>
        -> <expresionNormal> TkPlus <expresionNormal>
        -> <expresionNormal> TkMinus <expresionNormal>
        -> <booleano>
        -> TkNot <expresionNormal>
        -> <expresionNormal> TkLT <expresionNormal>
        -> <expresionNormal> TkLE <expresionNormal>
        -> <expresionNormal> TkGE <expresionNormal>
        -> <expresionNormal> TkGT <expresionNormal>
        -> <expresionNormal> TkEQ <expresionNormal>
        -> <expresionNormal> TkNE <expresionNormal>
        -> <expresionNormal> TkAnd <expresionNormal>
        -> <expresionNormal> TkOr <expresionNormal>   
        -> <expresionArreglo>
        -> <expresionFunciones>


<numero> -> TkNumber

<identificador> -> TkId

<booleano>
        -> TkTrue
        -> TkFalse

<expresionArreglo>
        -> TkOpenBracket <expresionArgs> TkCloseBracket
        -> <identificador> TkOpenBracket <expresionNormal> TkCloseBracket

<expresionArgs>
        -> 
        -> <expresionNormal>  
        -> <expresionNormal> , <expresionArgs>

<expresionFunciones>
        -> <identificador> TkOpenPar <expresionArgs> TkClosePar 

        # -> if(<condicion>, <expT>, <expF>)
        # -> type(<expresion>)
        # -> ltype(<expresion>)
        # -> reset()
        # -> uniform()
        # -> floor(<expresionNormal>)
        # -> length(<expresionArreglo>)
        # -> sum(<expresionNormal>)
        # -> avg(<expresionNormal>)
        # -> pi()
        # -> now()

# <condicion>
#         -> <expresionNormal>

# <expT>
#         -> <expresion>

# <expF>
#         -> <expresion>
```