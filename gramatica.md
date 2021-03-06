# Gramáticas libres de contexto

##  Primera gramática: sintaxis de Stókhos

```bash
<entrada> -> <instruccion> | <expresion>

<instruccion> -> <definicion> | <asignacion>

<definicion> -> <tipo> <lvalues> := <expresion> ;
<asignacion> -> <lvalues> := <expresion> ;

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
        #(acomodar para <expresion>[<expresion>])   
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

<definicion> -> <tipo> <lvalues> TkAssign <expresion> TkSemicolon
<asignacion> -> <lvalues> TkAssign <expresion> TkSemicolon

<tipo> -> <tipoBasico> 
       -> TkOpenBracket <tipo> TkCloseBracket

<tipoBasico> 
        -> TkNum
        -> TkBool

<lvalues> -> <identificador>
          -> <expresionArreglo>

<expresion>
        -> <numero>
        -> <identificador>
        -> TkOpenPar <expresion> TkClosePar
        -> TkOpenBrace <expresion> TkCloseBrace
        -> TkSingleQuote <expresion> TkSingleQuote
        -> TkOpenBracket expresionArgs TkCloseBracket
        -> <expresion> TkPower <expresion>
        -> TkPlus <expresion>
        -> TkMinus <expresion>
        -> <expresion> TkMult <expresion>
        -> <expresion> TkDiv <expresion>
        -> <expresion> TkMod <expresion>
        -> <expresion> TkPlus <expresion>
        -> <expresion> TkMinus <expresion>
        -> <booleano>
        -> TkNot <expresion>
        -> <expresion> TkLT <expresion>
        -> <expresion> TkLE <expresion>
        -> <expresion> TkGE <expresion>
        -> <expresion> TkGT <expresion>
        -> <expresion> TkEQ <expresion>
        -> <expresion> TkNE <expresion>
        -> <expresion> TkAnd <expresion>
        -> <expresion> TkOr <expresion>   
        -> <expresionArreglo>
        -> <expresionFunciones>


<numero> -> TkNumber

<identificador> -> TkId

<booleano>
        -> TkTrue
        -> TkFalse

<expresionArreglo>
        -> <identificador> TkOpenBracket <expresion> TkCloseBracket
        -> <expresionArreglo> TkOpenBracket <expresion> TkCloseBracket
        #-> <expresion> TkOpenBracket <expresion> TkCloseBracket
        #-> <identificador> TkOpenBracket <expresion> TkCloseBracket

<expresionArgs>
        -> 
        -> <expresion>  
        -> <expresion> , <expresionArgs>

<expresionFunciones>
        -> <identificador> TkOpenPar <expresionArgs> TkClosePar           
```