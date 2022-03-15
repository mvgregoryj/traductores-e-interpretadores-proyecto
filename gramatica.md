# Gramáticas libres de contexto

##  Primera gramática: sintaxis de Stókhos

<entrada> -> <instrucción> | <expresión>

<instrucción> -> <definición> | <asignación>

<definición> -> <tipo> <identificador> := <expresión> ;
<asignación> -> <identificador> := <expresión> ;

<tipo>
        -> <tipoBásico>
        -> <tipoNoBásico>

<tipoBásico>
        -> num
        -> bool

<tipoNoBásico>
        -> [<tipoBásico>]

<expresión>
        -> <identificador>
        -> <número>
        -> <booleano>
        -> (<expresión>)
        -> [<expresión>]
        -> <identificador>[<number>]            <!-- Preguntar -->
        -> '<expresión>'
        -> <expresión>^<expresión>
        -> +<expresión>
        -> -<expresión>
        -> !<expresión>
        -> <expresión> * <expresión>
        -> <expresión> / <expresión>
        -> <expresión> % <expresión>
        -> <expresión> + <expresión>
        -> <expresión> - <expresión>
        -> <expresión> < <expresión>
        -> <expresión> <= <expresión>
        -> <expresión> >= <expresión>
        -> <expresión> > <expresión>
        -> <expresión> = <expresión>
        -> <expresión> <> <expresión>
        -> <expresión> && <expresión>
        -> <expresión> || <expresión>   
        -> <expresión> , <expresión>   
