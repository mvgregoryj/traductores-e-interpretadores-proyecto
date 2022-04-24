'''
Grupo Dacary: 
                Gregory Muñoz   16-11313
                Daniela Ramirez 16-10940
                Giancarlo Dente 15-10395
'''

from ply.lex import lex
from ply.yacc import yacc
from Objetos import *
import random
import math
import time

ts_global = TablaDeSimbolos()
arr = []


# Función interna que construye una secuencia de tokens
def ejecutarLexer ():
    # Arreglo a usar
    arrayErrores = []
    
    # Tokens
    tokens  = (
        # Palabras reservadas:
        'TkNum', 'TkBool', 'TkFalse', 'TkTrue',

        # Constantes numéricas:
        'TkNumber',

        # Identificadores:
        'TkId',

        # Operadores:
        'TkOpenPar', 'TkClosePar',
        'TkOpenBracket', 'TkCloseBracket',
        'TkOpenBrace', 'TkCloseBrace',
        'TkSingleQuote',
        'TkNot',
        'TkPower',
        'TkMult', 'TkDiv', 'TkMod',
        'TkPlus', 'TkMinus',
        'TkLT', 'TkLE', 'TkGE', 'TkGT',
        'TkEQ', 'TkNE',
        'TkAnd',
        'TkOr',
        'TkQuote',
        'TkComma',
        'TkAssign',
        'TkSemicolon',
        'TkColon'

        # # Funciones predefinidas
        # 'TkIf',
        # 'TkType',
        # 'TkLtype',
        # 'TkReset',
        # 'TkUniform',
        # 'TkFloor',
        # 'TkLength',
        # 'TkSum',
        # 'TkAvg',
        # 'TkPi',
        # 'TkNow'
    )

    # Tokens con regex
    # Tokens palabras reservadas
    reservados = {
        'num' : 'TkNum',
        'bool' : 'TkBool',
        'false' : 'TkFalse',
        'true' : 'TkTrue'
        # 'if' : 'TkIf',
        # 'type' : 'TkType',
        # 'ltype' : 'TkLtype',
        # 'reset' : 'TkReset',
        # 'uniform' : 'TkUniform',
        # 'floor' : 'TkFloor',
        # 'length' : 'TkLength',
        # 'sum' : 'TkSum',
        # 'avg' : 'TkAvg',
        # 'pi' : 'TkPi',
        # 'now' : 'TkNow'
    }

    # Tokens Identificadores
    def t_TkId(t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.value = t.value
        t.type = reservados.get(t.value,'TkId')
        return t

    # Tokens Constantes numéricas
    def t_TkNumber(t):
        r'\d+(\.\d*)?'
        t.value = float(t.value) if '.' in t.value else int(t.value) 
        return t

    # Tokens operadores
    t_TkOpenPar         = r'\('
    t_TkClosePar        = r'\)'
    t_TkOpenBracket     = r'\['
    t_TkCloseBracket    = r'\]'
    t_TkOpenBrace       = r'\{'
    t_TkCloseBrace      = r'\}'
    t_TkSingleQuote     = r'\''
    t_TkNot             = r'\!'
    t_TkPower           = r'\^'
    t_TkMult            = r'\*'
    t_TkDiv             = r'\/'     # r'/'
    t_TkMod             = r'\%'
    t_TkPlus            = r'\+'
    t_TkMinus           = r'\-'     # r'-'
    t_TkLT              = r'\<'
    t_TkLE              = r'\<='
    t_TkGE              = r'\>='
    t_TkGT              = r'\>'
    t_TkEQ              = r'\='     # r'='
    t_TkNE              = r'\<>'
    t_TkAnd             = r'\&&'
    t_TkOr              = r'\|\|'
    t_TkQuote           = r'\.'     # r'.'
    t_TkComma           = r'\,'     # r','
    t_TkAssign          = r'\:='    # r':='
    t_TkSemicolon       = r'\;'     # r';'
    t_TkColon           = r'\:'     # r':'

    # Caracteres ignorados
    t_ignore = ' \t'

    # Comments ignored
    def t_comment(t):
        r'\#.*'
        pass

    # Ignored token with an action associated with it
    def t_ignore_newline(t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')

    # Error handler for illegal characters
    def t_error(t):
        arrayErrores.append(f'{t.value[0]!r}')
        t.lexer.skip(1)

    # Build the lexer object
    lexer = lex()



    return tokens, lexer, arrayErrores

# Funcion lexTest
def lexTest(data: str):

    # Arreglo a usar
    arrayTokens = []

    # Eliminamos los espacios antes y despues de la expresión
    data = data[4:].strip()

    # Construimos el objecto lexer y el arreglo de errores
    tokens, lexer, arrayErrores = ejecutarLexer()

    # Entrada para el lexer
    lexer.input(data)

    for tok in lexer:

        if (tok.type == 'TkNumber' or tok.type == 'TkId'):
            arrayTokens.append(f"{tok.type}({tok.value})")
            # arrayTokens.append(tok.type + "(" + tok.value + ")" if type(tok.value)==str else tok.type + "(" + str(tok.value) +")")

        else:
            arrayTokens.append(f"{tok.type}")
           
    return data, arrayTokens, arrayErrores
        
#########################################################

#Funcion que guarda el objeto Parse de la libreria PLY, gracias a yacc en la variable global parseador
def ejecutamosParseador():


    # Construimos el objecto lexer y el arreglo de errores
    tokens, lexer, arrayErrores = ejecutarLexer()
    
    global arr
        
    # # Entrada para el lexer
    # lexer.input(input)

    # --- Parser

    # Write functions for each grammar rule which is
    # specified in the docstring.

    precedence = (
        ('nonassoc', 'TkOr'),  # Nonassociative operators       
        ('nonassoc', 'TkAnd'),  # Nonassociative operators       
        ('nonassoc', 'TkEQ', 'TkNE'),  # Nonassociative operators     
        ('nonassoc', 'TkLT', 'TkLE', 'TkGE', 'TkGT'),  # Nonassociative operators        
        ('left', 'TkPlus', 'TkMinus'),
        ('left', 'TkMult', 'TkDiv', 'TkMod'),
        ('right', 'TkUMinus', 'TkUPlus', 'TkNot'),            # Unary minus operator
        ('right', 'TkPower')
    )

    def p_entrada(p):
        '''
        entrada : 
                | instruccion 
                | expresion
        '''
        if len(p) == 1:
            p[0] = ""
        else:
            p[0] = p[1]

    def p_instruccion(p):
        '''
        instruccion : definicion 
                    | asignacion
        '''
        p[0] = p[1]

    def p_definicion(p):
        '''
        definicion : tipo identificador TkAssign expresion TkSemicolon
        '''
        p[0] = Definition(p[1], p[2], p[4])

    def p_asignacion(p):
        '''
        asignacion : identificador TkAssign expresion TkSemicolon
        '''
        p[0] = Assignment(p[1], p[3])

    def p_tipo(p):
        '''
        tipo : tipoBasico
             | TkOpenBracket tipo TkCloseBracket
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Grouped("Bracket", p[1], p[2], p[3])

    def p_tipoBasico(p):
        '''
        tipoBasico : TkNum
                   | TkBool
        '''
        p[0] = BasicType(p[1])
    
    def p_expresion(p):
        '''
        expresion : numero 
                  | identificador
                  | TkOpenPar expresion TkClosePar
                  | TkOpenBrace expresion TkCloseBrace
                  | TkSingleQuote expresion TkSingleQuote 
                  | expresion TkPower expresion
                  | TkPlus expresion %prec TkUPlus
                  | TkMinus expresion %prec TkUMinus
                  | expresion TkMult expresion
                  | expresion TkDiv expresion
                  | expresion TkMod expresion
                  | expresion TkPlus expresion
                  | expresion TkMinus expresion
                  | booleano
                  | TkNot expresion
                  | expresion TkLT expresion
                  | expresion TkLE expresion
                  | expresion TkGE expresion
                  | expresion TkGT expresion
                  | expresion TkEQ expresion
                  | expresion TkNE expresion
                  | expresion TkAnd expresion
                  | expresion TkOr expresion   
                  | expresionArreglo
                  | expresionFunciones
        '''
        if len(p) == 2:
            p[0] = p[1]

        elif len(p) == 3:
            p[0] = UnaOp(p[1], p[2])

        elif len(p) == 4:
            if (p[1]=='(' and p[3]==')'):
                p[0] = Grouped("Par", p[1], p[2], p[3])
            elif  (p[1]=='{' and p[3]=='}'):
                p[0] = Grouped("Brace", p[1], p[2], p[3])
            elif (p[1]=="'" and p[3]=="'"):
                p[0] = Grouped("SingleQuote", p[1], p[2], p[3])
            else:
                p[0] = BinOp(p[1], p[2], p[3])
    
    def p_numero(p):
        '''
        numero : TkNumber
        '''
        p[0] = Number(p[1])

    def p_identificador(p):
        '''
        identificador : TkId
        '''
        p[0] = Identifier(p[1])
        
    def p_booleano(p):
        '''
        booleano : TkTrue
                 | TkFalse
        '''
        if p[1] == 'true':
            p[0] = Boolean(True)
        elif p[1] == 'false':
            p[0] = Boolean(False)
    
    def p_expresionArreglo(p):
        '''
        expresionArreglo : TkOpenBracket expresionArgs TkCloseBracket
                         | identificador TkOpenBracket expresion TkCloseBracket
        '''
        if len(p) == 4:
            if (p[1]=='[' and p[3]==']'):
                p[0] = Grouped("Bracket", p[1], p[2], p[3])
        else:
            p[0] = ArrayExpression(p[1], p[3])
                
    def p_expresionArgs(p):
        '''
        expresionArgs : 
                      | expresion  
                      | expresion TkComma expresionArgs
        '''
        if len(p) == 1:
            p[0] = ""
        elif len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = BinOp(p[1], p[2], p[3])

    def p_expresionFunciones(p):
        '''
        expresionFunciones : identificador TkOpenPar expresionArgs TkClosePar 
        '''
        p[0] = Function(p[1], p[3])

    def p_error(p):
        
        if p == None:
            token = 'Unexpected end of input'
        else:
            token = f"{p.type}({p.value}) at line {p.lineno}"
            
        arr.append(token)               
                        
    # Retornamos el parser de yacc
    return yacc(), arrayErrores

# print(arreglo)

# Funcion parse:
# Parse recibe la secuencia de caracteres correspondiente a la entrada 
# indicada por el usuario y retorna el AST correspondiente
def parse(input: str):

    parseador , arrayErrores = ejecutamosParseador()
    ast = parseador.parse(input)

    return ast, arrayErrores

# Funcion ast2str:
# Técnicamente, ast2str implementa una traducción. Para simplificar la 
# traducción, y hacerla amigable, las expresiones deben ser regeneradas con 
# paréntesis redundantes usando notación infija:
def ast2str(input: str, ast) -> str:
    
    return f'OK: ast("{input}") ==> {ast}'

# Funcion testParser:
# Llama a parse y convierte el AST resultante en un string que puede ser 
# consumido por el REPL
def testParser(input: str) -> str:
    
    global arr
    
    # Eliminamos los espacios antes y despues de la expresión
    input = input[4:].strip()

    # Colocamos el arreglo vacio
    arr = []
    
    # Llamamos a parser con el input ingresado por el usuario
    ast, arrayErrores = parse(input)


    # Si los arreglos no estan vacios, entonces hubo un error
    if len(arrayErrores) > 0:
        return f"ERROR: caracter inválido ({arrayErrores[0]}) en la entrada"
    elif len(arr) > 0:
        return f"ERROR: syntax error {arr[0]}"
    else:
        astString = ast2str(input, ast)
        return astString

        

#########################################################

def procesarDefinicion(data: str, instruccion: Definition, ts: TablaDeSimbolos) -> str:
    if ts.existe_simbolo_en_ts(instruccion.id):
        return f"ERROR: identificador {instruccion.id} ya está definido"
    else:
        resultado = funcionEval(data, instruccion.expression, ts)
        tipoResultado = procesarType(data, resultado, ts)

        # # print(tipoResultado)
        # # print(instruccion.type)

        if tipoResultado.type == instruccion.type.type:
            # Si resultado es un ERROR no se agrega a la tabla de simbolos.
            if f"{resultado}".startswith("ERROR"):
                return resultado
            else:
            # Se actualiza el simbolo en la tabla de simbolos resultado es del tipo Number, Boolean o list gracias al return de funcionEval                
                simbolo = Definition(instruccion.type, instruccion.id, resultado)
                ts.agregar_simbolo(simbolo)

                return f"ACK: {simbolo.type} {simbolo.id} := {simbolo.expression};"
        else: 
            return f"ERROR: tipo de dato de la expresión {instruccion.expression} no coincide con el tipo de dato de {instruccion.type}"


def procesarAsignacion(data: str, instruccion: Assignment, ts: TablaDeSimbolos) -> str:
    if ts.existe_simbolo_en_ts(instruccion.id):

        resultado = funcionEval(data, instruccion.expression, ts)
        tipoResultado = procesarType(data, resultado, ts)

        simbolo = ts.obtener_simbolo(instruccion.id)
        tipoSimbolo = simbolo.type

        if tipoResultado.type == tipoSimbolo.type:

            # Si resultado es un ERROR no se agrega a la tabla de simbolos.
            if f"{resultado}".startswith("ERROR"):
                return resultado
            else:
            # Se actualiza el simbolo en la tabla de simbolos, el resultado es del tipo Number, Boolean o list gracias al return de funcionEval                
                simbolo = Assignment(instruccion.id, resultado)
                ts.actualizar_simbolo(simbolo)

                return f"ACK: {instruccion.id} := {resultado};"
        else: 
            return f"ERROR: tipo de dato de la expresión {instruccion.expression} no coincide con el tipo de dato de {instruccion.id}"
    else:
        return f"ERROR: identificador {instruccion.id} no definido"
    
def procesarOperacionBinaria(data: str, instruccion: BinOp, ts: TablaDeSimbolos) -> str or Number or Boolean:

    expLeft = funcionEval(data, instruccion.left, ts)
    expRight = funcionEval(data, instruccion.right, ts)
    

    # Se verifica que la operacion sea valida
    if isinstance(expLeft, str) & isinstance(expRight, str):
        if expLeft.startswith("ERROR") & expRight.startswith("ERROR"):
            return f"{expLeft}\n{expRight}"
    elif isinstance(expLeft, str):
        if expLeft.startswith("ERROR"):
            return expLeft
    elif isinstance(expRight, str):
        if expRight.startswith("ERROR"):
            return expRight
    elif isinstance(expLeft, Number) & isinstance(expRight, Number):
        if instruccion.op == "^" : respuesta = Number(expLeft.value ** expRight.value)
        elif instruccion.op == "*" : respuesta = Number(expLeft.value * expRight.value)
        elif instruccion.op == "/" : respuesta = Number(expLeft.value // expRight.value)
        elif instruccion.op == "%" : respuesta = Number(expLeft.value % expRight.value)
        elif instruccion.op == "+" : respuesta = Number(expLeft.value + expRight.value)
        elif instruccion.op == "-" : respuesta = Number(expLeft.value - expRight.value)
        elif instruccion.op == "<" : respuesta = Boolean(expLeft.value < expRight.value)
        elif instruccion.op == "<=" : respuesta = Boolean(expLeft.value <= expRight.value)
        elif instruccion.op == ">=" : respuesta = Boolean(expLeft.value >= expRight.value)
        elif instruccion.op == ">" : respuesta = Boolean(expLeft.value > expRight.value)
        elif instruccion.op == "=" : respuesta = Boolean(expLeft.value == expRight.value)
        elif instruccion.op == "<>" : respuesta = Boolean(expLeft.value != expRight.value)

        return respuesta

    elif isinstance(expLeft, Boolean) & isinstance(expRight, Boolean):
        if instruccion.op == "=" : respuesta = Boolean(expLeft.value == expRight.value)
        elif instruccion.op == "<>" : respuesta = Boolean(expLeft.value != expRight.value)
        elif instruccion.op == "&&" : respuesta = Boolean(expLeft.value & expRight.value)
        elif instruccion.op == "||" : respuesta = Boolean(expLeft.value | expRight.value)

        return respuesta

    else:
        return f"ERROR: no hay coincidencia de tipo entre {expLeft} y {expRight}"

def procesarNumero(data: str, instruccion: Number, ts: TablaDeSimbolos) -> Number:
    return instruccion

def procesarIdentificador(data: str, instruccion: Identifier, ts: TablaDeSimbolos) -> Number or Boolean or list or str:
    # Verifiquemos que el identificador exista en la tabla de simbolos
    if ts.existe_simbolo_en_ts(instruccion):
        valorEncontrado = ts.obtener_simbolo(instruccion)
        return funcionEval(data, valorEncontrado.expression, ts)
    else:
        return f"ERROR: identificador {instruccion} no definido"

def procesarOperacionUnaria(data: str, instruccion: UnaOp, ts: TablaDeSimbolos) -> str:
    exp = funcionEval(data, instruccion.right, ts)
    if isinstance(exp, Number):

        if instruccion.op == "+" : return Number(exp.value)
        elif instruccion.op == "-" : return Number(-exp.value)
        else: return f"ERROR: operador {instruccion.op} no válido"

    elif isinstance(exp, Boolean):
        if instruccion.op == "!" : return Boolean(not exp.value)
        else: return f"ERROR: operador {instruccion.op} no válido"

    else: 
        return f"ERROR: expresion {instruccion.right} no es valida para operaciones unarias."

def procesarAgrupacion(data: str, instruccion: Grouped, ts: TablaDeSimbolos) -> str or list or Number or Boolean:
    
    if isinstance(instruccion, Grouped) & (instruccion.type == "Par"):
        return funcionEval(data, instruccion.expression, ts)

    elif isinstance(instruccion, Grouped) & (instruccion.type == "Brace"):
        return funcionEval(data, instruccion.expression, ts)

    elif isinstance(instruccion, Grouped) & (instruccion.type == "SingleQuote"):
        return instruccion.expression

    elif isinstance(instruccion, Grouped) & (instruccion.type == "Bracket"):
        instruccion = instruccion.expression
        arregloTemp = []

        # Casos en el que el arreglo tiene un solo elemento
        if isinstance(instruccion, Number) or isinstance(instruccion, Boolean) or isinstance(instruccion, Identifier) or isinstance(instruccion, UnaOp) or isinstance(instruccion, ArrayExpression) or isinstance(instruccion, Grouped) or (isinstance(instruccion, BinOp) & (instruccion.op in "^*/%+-<<=>=>=<>&&||")):


            respuesta = funcionEval(data, instruccion, ts)

            # Si el unico elemento es un ERROR, se retorna el error.
            if f"{respuesta}".startswith("ERROR"):
                return respuesta
            else:
                arregloTemp.append(respuesta)

        
        # Caso de que el arreglo tiene mas de un elemento
        elif isinstance(instruccion, BinOp) & (instruccion.op == ","):
            arregloTemp = procesarArgsOrElemArray(data, instruccion, ts, arregloTemp)

            # Si procesarArgsOrElemArray retorna un ERROR, se retorna el error.
            if f"{arregloTemp}".startswith("ERROR"):
                return respuesta

            
        return arregloTemp

    else:
        return funcionEval(data, instruccion, ts)

def procesarArgsOrElemArray(data, instruccion, ts, arregloTemp) -> list or str:

    # Se obtiene el primer elemento del arreglo
    izquierda = instruccion.left
    respuesta = funcionEval(data, izquierda, ts)
    
    # Si el primer elemento es un ERROR, se retorna el error, si no se continua con el procesamiento
    if f"{respuesta}".startswith("ERROR"):
        return respuesta
    else:
        arregloTemp.append(respuesta)
    
    # Se obtienen los elementos del medio del arreglo, si los hay
    derecha = instruccion.right
    while isinstance(derecha, BinOp):
        if (derecha.op == ","):
            # # print(arregloTemp)
            izquierda = derecha.left
            respuesta = funcionEval(data, izquierda, ts)

            # Si el elemento es un ERROR, se retorna el error, si no se continua con el procesamiento
            if f"{respuesta}".startswith("ERROR"):
                return respuesta
            else:
                arregloTemp.append(respuesta)

            derecha = derecha.right

        else:
            break

    respuesta = funcionEval(data, derecha, ts)

    # Si el ultimo elemento es un ERROR, se retorna el error.
    if f"{respuesta}".startswith("ERROR"):
        return respuesta
    else:
        arregloTemp.append(respuesta)

    return arregloTemp

def procesarArregloInstruccion(data: str, instruccion: ArrayExpression, ts: TablaDeSimbolos) -> Number or Boolean or list or str:
    # Verifiquemos que el identificador exista en la tabla de simbolos
    if ts.existe_simbolo_en_ts(instruccion.id):
        definicionArreglo = ts.obtener_simbolo(instruccion.id)
        arreglo = definicionArreglo.expression

        if isinstance(arreglo, list):
            indice = funcionEval(data, instruccion.index, ts)
            if isinstance(indice, Number):
                try:
                    # # print(type(arreglo[indice.value]))
                    respuesta = arreglo[indice.value]
                    return funcionEval(data, respuesta, ts)

                except IndexError:
                    return f"ERROR: indice fuera de rango"
            else:
                return f"ERROR: {indice} no es un numero"
        else:
            return f"ERROR: {arreglo} no es un arreglo"
    else:
        return f"ERROR: variable {instruccion.id} no definida"

def procesarBoolean(data: str, instruccion: Boolean, ts: TablaDeSimbolos) -> Boolean:
    return instruccion

def procesarLista(data: str, instruccion: list, ts: TablaDeSimbolos) -> list:
    arrTemp = []
    for elem in instruccion:
        resultadoTemp = funcionEval(data, elem, ts)
        if f"{resultadoTemp}".startswith("ERROR"):
            return resultadoTemp
        else:
            arrTemp.append(resultadoTemp)
    
    return arrTemp

def procesarFuncion(data: str, instruccion: Function, ts: TablaDeSimbolos) -> str:
    nombreFuncion = instruccion.id.value
    funcionesConArgs = ["if","type","ltype","floor","length","sum","avg","ln","exp","sin","cos","tan"]
    funcionesSinArgs = ["reset","uniform","pi","now"]

    if nombreFuncion in funcionesConArgs:
        argumentos = instruccion.args

        if nombreFuncion == "if":
            return procesarIf(data, argumentos, ts)
        elif nombreFuncion == "type":
            return procesarType(data, argumentos, ts)
        elif nombreFuncion == "ltype":
            return procesarLtype(data, argumentos, ts)
        elif nombreFuncion == "floor":
            return procesarFloor(data, argumentos, ts)
        elif nombreFuncion == "length":
            return procesarLength(data, argumentos, ts)
        elif nombreFuncion == "sum":
            return procesarSum(data, argumentos, ts)
        elif nombreFuncion == "avg":
            return procesarAvg(data, argumentos, ts)
        elif nombreFuncion == "ln":
            return procesarLn(data, argumentos, ts)
        elif nombreFuncion == "exp":
            return procesarExp(data, argumentos, ts)
        elif nombreFuncion == "sin":
            return procesarSin(data, argumentos, ts)
        elif nombreFuncion == "cos":
            return procesarCos(data, argumentos, ts)
        elif nombreFuncion == "tan":
            return procesarTan(data, argumentos, ts)
        else:
            return f"ERROR: {nombreFuncion} no definida"

    elif nombreFuncion in funcionesSinArgs:
        if nombreFuncion == "reset":
            return procesarReset(ts)
        elif nombreFuncion == "uniform":
            return procesarUniform()
        elif nombreFuncion == "pi":
            return procesarPi()
        elif nombreFuncion == "now":
            return procesarNow()
        else:
            return f"ERROR: {nombreFuncion} no definida"

    else:
        return f"ERROR: funcion {nombreFuncion} no definida"

# Funcion que se encarga de procesar la instruccion if    
def procesarIf(data: str, argumentos: BinOp, ts: TablaDeSimbolos):
    arregloTemp = procesarArgsOrElemArray(data, argumentos, ts, [])

    if isinstance(arregloTemp, str) and arregloTemp.startswith("ERROR"):
        return arregloTemp

    else:
        condicion = arregloTemp[0]
        expT = arregloTemp[1]
        expF = arregloTemp[2]

        if isinstance(condicion, Boolean) and condicion.value:
            return expT
        elif isinstance(condicion, Boolean) and (not condicion.value):
            return expF
        else:
            return f"ERROR: condicion no valida"
    
# Funcion procesarType retorna el tipo de una expresión, sin evaluar dicha expresión
def procesarType(data: str, argumento, ts: TablaDeSimbolos) -> BasicType or str:

    # # print(argumento)
    # # print(type(argumento))

    if isinstance(argumento, Identifier):

        if ts.existe_simbolo_en_ts(argumento):
            simbolo = ts.obtener_simbolo(argumento)
            return simbolo.type
        else:
            return f"ERROR: identificador {argumento} no definido"

    elif isinstance(argumento, Number):

        return BasicType(argumento.type)

    elif isinstance(argumento, ArrayExpression):

        if ts.existe_simbolo_en_ts(argumento.id):
            simbolo = ts.obtener_simbolo(argumento.id)
            tipo = simbolo.type.expression
            return tipo
        else:
            return f"ERROR: identificador {argumento.id} no definido"

    elif isinstance(argumento, Boolean):
        return BasicType(argumento.type)

    elif isinstance(argumento, Grouped) and (argumento.type == "Par"):
        return procesarType(data, argumento.expression, ts)

    elif isinstance(argumento, list):
        tipoElemArray = procesarType(data, argumento[0], ts)
        return Grouped("Bracket", "[", tipoElemArray, "]")

    elif isinstance(argumento, UnaOp):
        if argumento.op == "!" and isinstance(argumento.right, Boolean):
            return BasicType(argumento.right.type)
        elif argumento.op in "-+" and isinstance(argumento.right, Number):
            return BasicType(argumento.right.type)
        else:
            return f"ERROR: operacion binaria no definida o inconsistencia de tipos"

    elif isinstance(argumento, BinOp):

        if argumento.op in "^*/%+-":
            return BasicType("num")
        elif argumento.op in "<<=>=>=<>":
            return BasicType("bool")
        elif argumento.op in "=<>&&||":
            return BasicType("bool")
        else:
            return f"ERROR: operacion binaria no definida o inconsistencia de tipos"

    elif isinstance(argumento, Function):
        if argumento.id.value in ["uniform", "floor", "length", "sum", "avg", "pi", "now", "ln", "exp", "sin", "cos", "tan"]:
            return BasicType("num")
        else:
            return f"ERROR: funcion {argumento} no posse un tipo o no se puede obtener sin evaluar la funcion."
    
    else:
        return f"ERROR: {argumento} no es de un tipo conocido"

# Funcion procesarLtype retorna el tipo de una expresión asignable, o un error si la expresión no es asignable
def procesarLtype(data: str, argumento, ts: TablaDeSimbolos) -> str:
    if isinstance(argumento, Identifier):

        if ts.existe_simbolo_en_ts(argumento):
            simbolo = ts.obtener_simbolo(argumento)
            tipo = simbolo.type
            return tipo
        else:
            return f"ERROR: identificador {argumento} no definido"

    elif isinstance(argumento, Number):

        return f"ERROR: la expresion ‘{argumento}' no tiene LVALUE"

    elif isinstance(argumento, ArrayExpression):

        if ts.existe_simbolo_en_ts(argumento.id):
            simbolo = ts.obtener_simbolo(argumento.id)
            tipo = simbolo.type.expression
            return tipo
        else:
            return f"ERROR: identificador {argumento.id} no definido"

    elif isinstance(argumento, Boolean):
        return f"ERROR: la expresion ‘{argumento}' no tiene LVALUE"

    elif isinstance(argumento, Grouped):
        return f"ERROR: la expresion ‘{argumento}' no tiene LVALUE"

    elif isinstance(argumento, UnaOp):
        return f"ERROR: la expresion ‘{argumento}' no tiene LVALUE"

    elif isinstance(argumento, BinOp):
        return f"ERROR: la expresion ‘{argumento}' no tiene LVALUE"

# Funcion procesarReset, elimina todas las variables definidas por el usuario en la VM
def procesarReset(ts: TablaDeSimbolos) -> str:
    try:
        resultado = ts.limpiar_ts()
        return f"{resultado}".lower()
    except:
        return f"{False}".lower()

# Funcion procesarUniform, retorna un número entero “aleatorio” entre 0 y 1.
def procesarUniform() -> str:
    return Number(random.uniform(0, 1))

# Funcion procesarFloor retorna el mayor número entero n tal que n <= argumento.
def procesarFloor(data: str, argumento, ts: TablaDeSimbolos) -> str:
    # # print(argumento)
    # # print(type(argumento))
    tipo = procesarType(data, argumento, ts)
    # # print(tipo)
    # # print(type(tipo))
    # Comprobamos si tipo es de tipo "num"
    if isinstance(tipo, BasicType) and tipo.type == "num":
        respuesta = funcionEval(data, argumento, ts)
        return Number(math.floor(respuesta.value))
    else:
        return f"ERROR: la expresion ‘{argumento}' no es de tipo num"
        
# Funcion procesarLength retorna la longitud de un arreglo de cualquier tipo.
def procesarLength(data: str, argumento: Identifier, ts: TablaDeSimbolos) -> str:
    # 1ra Manera
    if ts.existe_simbolo_en_ts(argumento):
        simbolo = ts.obtener_simbolo(argumento)
        arrTemp = simbolo.expression
        if isinstance(arrTemp, list):
            # #print(Number(len(arrTemp)))
            return Number(len(arrTemp))
        else:
            return f"ERROR: identificador {argumento} no es un arreglo"
    else:
        return f"ERROR: identificador {argumento} no esta definido"

# Funcion procesarSum retorna la suma de un arreglo de números
def procesarSum(data: str, argumento: Identifier, ts: TablaDeSimbolos) -> int or str:
    if ts.existe_simbolo_en_ts(argumento):
        simbolo = ts.obtener_simbolo(argumento)
        arrTemp = simbolo.expression

        tipo = procesarType(data, arrTemp[0], ts)

        # # print(type(arrTemp))
        # # print(type(tipo))
        # # print(tipo.type)

        # Comprobamos si tipo es de tipo "num"
        if isinstance(arrTemp, list) and isinstance(tipo, BasicType) and tipo.type == "num":

            suma = 0
            
            for i in range(0, len(arrTemp)):
                varTemp = funcionEval(data, arrTemp[i], ts).value
                # print(varTemp)
                suma = suma + varTemp
            
            # # print("qlq")
            return Number(suma)    

        else:
            return f"ERROR: el arreglo ‘{argumento}' no es de tipo [num]"
    else:
        return f"ERROR: identificador {argumento} no esta definido"

def procesarAvg(data: str, argumento: Identifier, ts: TablaDeSimbolos) -> str:
    suma = procesarSum(data, argumento, ts)
    length = procesarLength(data, argumento, ts) 

    tipoSuma = procesarType(data, suma, ts)
    tipoLength = procesarType(data, length, ts)

    # Comprobamos si tipoSuma y tipoLength son de tipo "num"
    if (isinstance(tipoSuma, BasicType) and tipoSuma.type == "num") and (isinstance(tipoLength, BasicType) and tipoLength.type == "num"):
        return Number(suma.value / length.value)

    else:
        return f"ERROR: la expresion ‘{argumento}' no es de tipo [num]"

# Funcion procesarPi, retorna una aproximación al numero pi
def procesarPi() -> str:
    return Number(math.pi)

# Funcion procesarNow, retorna un número entero correspondiente al número de milisegundos transcurridos desde un punto de referencia en el tiempo
def procesarNow():
    return Number(int(round(time.time() * 1000)))

# La función procesarLn retorna el logaritmo natural del argumento. Si el logaritmo no existe arroja un error.
def procesarLn(data, argumento, ts):
    tipo = procesarType(data, argumento, ts)
    
    # Comprobamos si tipo es de tipo "num"
    if isinstance(tipo, BasicType) and tipo.type == "num":
        respuesta = funcionEval(data, argumento, ts)

        if respuesta.value <= 0:
            return f"ERROR: {respuesta.value} no pertenece al dominio de la funcion ln."

        else:
            return Number(math.log(respuesta.value))
    else:
        return f"ERROR: la expresion ‘{argumento}' no es de tipo num"

# La función procesarExp retorna el exponencial del argumento x, es decir e^x .
def procesarExp(data, argumento, ts):
    tipo = procesarType(data, argumento, ts)
    
    # Comprobamos si tipo es de tipo "num"
    if isinstance(tipo, BasicType) and tipo.type == "num":
        respuesta = funcionEval(data, argumento, ts)
        return Number(math.exp(respuesta.value))
    else:
        return f"ERROR: la expresion ‘{argumento}' no es de tipo num"

# La función procesarSin retorna el seno del argumento, es decir sin x .
def procesarSin(data, argumento, ts):
    tipo = procesarType(data, argumento, ts)
    
    # Comprobamos si tipo es de tipo "num"
    if isinstance(tipo, BasicType) and tipo.type == "num":
        respuesta = funcionEval(data, argumento, ts)

        return Number(math.sin(respuesta.value))
    else:
        return f"ERROR: la expresion ‘{argumento}' no es de tipo num"

# La función procesarCos retorna el coseno del argumento, es decir cos x .
def procesarCos(data, argumento, ts):
    tipo = procesarType(data, argumento, ts)
    
    # Comprobamos si tipo es de tipo "num"
    if isinstance(tipo, BasicType) and tipo.type == "num":
        respuesta = funcionEval(data, argumento, ts)
        return Number(math.cos(respuesta.value))
    else:
        return f"ERROR: la expresion ‘{argumento}' no es de tipo num"

# La función procesarTan retorna el coseno del argumento, es decir tan x .
def procesarTan(data, argumento, ts):
    tipo = procesarType(data, argumento, ts)
    
    # Comprobamos si tipo es de tipo "num"
    if isinstance(tipo, BasicType) and tipo.type == "num":
        respuesta = funcionEval(data, argumento, ts)
        return Number(math.tan(respuesta.value))
    else:
        return f"ERROR: la expresion ‘{argumento}' no es de tipo num"

####################################################

# funcionExecute recibe una definicion o asignacion y la procesa
def funcionExecute(input: str, instruccion: Definition or Assignment, ts: TablaDeSimbolos) -> str:

    # Si la instruccion es una declaracion de variable
    if isinstance(instruccion, Definition): 
        return procesarDefinicion(input, instruccion, ts)

    elif isinstance(instruccion, Assignment): 
        return procesarAsignacion(input, instruccion, ts)

# funcionEval recibe una expresion y la evalua
def funcionEval(input: str, instruccion, ts: TablaDeSimbolos) -> str or Number or Boolean:
    # print(instruccion)
    # print(type(instruccion))

    if isinstance(instruccion, BinOp):
        return procesarOperacionBinaria(input, instruccion, ts)

    elif isinstance(instruccion, Number): 
        return procesarNumero(input, instruccion, ts)

    elif isinstance(instruccion, Identifier): 
        return procesarIdentificador(input, instruccion, ts)

    elif isinstance(instruccion, UnaOp): 
        return procesarOperacionUnaria(input, instruccion, ts)

    elif isinstance(instruccion, Grouped): 
        return procesarAgrupacion(input, instruccion, ts)

    elif isinstance(instruccion, ArrayExpression): 
        return procesarArregloInstruccion(input, instruccion, ts)

    elif isinstance(instruccion, Boolean): 
        return procesarBoolean(input, instruccion, ts)

    elif isinstance(instruccion, Function):
        return procesarFuncion(input, instruccion, ts)

    elif isinstance(instruccion, list):
        return procesarLista(input, instruccion, ts)

    else: 
        # print("Hola Dani")
        return f"ERROR: instrucción no válida."

# Process
def process(input: str) -> str:

    global arr
    # Colocamos el arreglo vacio
    arr = []

    # Llamamos a parser con el input ingresado por el usuario
    instruccion, arrayErrores = parse(input)
    # # print(input)
    # # print(type(instruccion))
    # # print(instruccion)
    # # print(type(instruccion.id))
    # # print(type(instruccion.index))

    # Si el arreglo no esta vacio, entonces hubo un error
    if len(arrayErrores) > 0:
        return f"ERROR: caracter inválido ({arrayErrores[0]}) en la entrada"
    elif len(arr) > 0:
        return f"ERROR: syntax error {arr[0]}"
    else:   
        if isinstance(instruccion, Definition) or isinstance(instruccion, Assignment):
            return funcionExecute(input, instruccion, ts_global)
        elif isinstance(instruccion, str) and input.startswith("#"):
            return ""
        else:
            respuesta = funcionEval(input, instruccion, ts_global)

            if isinstance(respuesta, str) and respuesta.startswith("ERROR"):
                return respuesta

            else:
                # # print(type(respuesta))
                # # print(type(respuesta.left))
                # # print(type(respuesta.left.left))
                # # print(type(respuesta.left.right))
                # # print(type(respuesta.right))

                return f"OK: {input} ==> {respuesta}"