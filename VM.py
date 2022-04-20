'''
Grupo Dacary: 
                Gregory Muñoz   16-11313
                Daniela Ramirez 16-10940
                Giancarlo Dente 15-10395
'''

#import ply.lex as lex
from array import array
from ast import Expression
from cmath import exp
from ply.lex import lex
from ply.yacc import yacc
from Objetos import *
import random
import math
import time

ts_global = TablaDeSimbolos()
arr = []

# Process
def process (input: str) -> str:

    return procesar_instruccion(input, ts_global)

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
def lexTest (data: str):

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

# Funcion uniform, retorna un número entero “aleatorio” entre 0 y 1.
def uniform():
    return random.uniform(0,1)

# Funcion floor, retorna el mayor número entero n tal que n <= x
def floor(expr):
    return math.floor(expr)

# Funcion length, devuelve el tamaño de un arreglo    
def length(expr):
    return len(expr)

# Funcion sum, retorna la suma de un arreglo de numeros
def sum(expr):
    suma = 0
    
    for i in range(0, len(expr)):
        suma = suma + expr[i]
        
    return suma

# Funcion avg, retorna el promedio de un arreglo de números
def avg(expr):
    avg = sum(expr)/length(expr)
    return avg

# Funcion pi, retorna una aproximación al numero pi
def pi():
    return math.pi

# Funcion reset, elimina todas las variables definidas por el usuario en la VM
def reset2():
    identificadores.clear()    
    if len(identificadores) == 0:
        print(True)

# Funcion now, retorna un número entero correspondiente al número de milisegundos transcurridos desde un
# punto de referencia en el tiempo
def now():
    return int(round(time.time() * 1000))

#########################################################

# class Expr: pass

# class Uniform():
#     def __init__(self):
#         self = None
        
#     def __repr__(self):
#         return f"{uniform()}"

# class Floor(Expr):
#     def __init__(self,expression):
#         self.expression = expression
        
#     def __repr__(self):
#         return f"{floor(self.expression)}"

# class Length(Expr):
#     def __init__(self,expression):
#         self.expression = expression
        
#     def __repr__(self):
#         return f"{length(self.expression)}"
    
# class Sum(Expr):
#     def __init__(self,expression):
#         self.expression = expression
        
#     def __repr__(self):
#         return f"{sum(self.expression)}"
    
# class Avg(Expr):
#     def __init__(self,expression):
#         self.expression = expression
        
#     def __repr__(self):
#         return f"{avg(self.expression)}"
    
# class Pi():
#     def __init__(self):
#         self = None
        
#     def __repr__(self):
#         return f"{pi()}"

# class Reset():
#     def __init__(self):
#         self = None
        
#     def __repr__(self):
#         return f"{reset2()}"

# class Now():
#     def __init__(self):
#         self = None
        
#     def __repr__(self):
#         return str(now())
    
# class Conditional(Expr):
#     def __init__(self, condicion, expT, expF):
#         self.condicion = condicion
#         self.expT = expT
#         self.expF = expF
        
# class Type(Expr):
#     def __init__(self,expression):
#         self.expression = expression
        
# class Ltype(Expr):
#     def __init__(self,expression):
#         self.expression = expression    
    
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
        expresion : expresionAcotada
                  | expresionNormal
        '''
        p[0] = p[1]
    
    def p_expresionAcotada(p):
        '''
        expresionAcotada : TkSingleQuote expresionNormal TkSingleQuote 
        '''
        p[0] = Grouped("SingleQuote", p[1], p[2], p[3])
    
    def p_expresionNormal(p):
        '''
        expresionNormal : numero 
                        | identificador
                        | TkOpenPar expresionNormal TkClosePar
                        | TkOpenBrace expresionNormal TkCloseBrace
                        | expresionNormal TkPower expresionNormal
                        | TkPlus expresionNormal %prec TkUPlus
                        | TkMinus expresionNormal %prec TkUMinus
                        | expresionNormal TkMult expresionNormal
                        | expresionNormal TkDiv expresionNormal
                        | expresionNormal TkMod expresionNormal
                        | expresionNormal TkPlus expresionNormal
                        | expresionNormal TkMinus expresionNormal
                        | booleano
                        | TkNot expresionNormal
                        | expresionNormal TkLT expresionNormal
                        | expresionNormal TkLE expresionNormal
                        | expresionNormal TkGE expresionNormal
                        | expresionNormal TkGT expresionNormal
                        | expresionNormal TkEQ expresionNormal
                        | expresionNormal TkNE expresionNormal
                        | expresionNormal TkAnd expresionNormal
                        | expresionNormal TkOr expresionNormal   
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
        p[0] = Boolean(p[1])
    
    def p_expresionArreglo(p):
        '''
        expresionArreglo : TkOpenBracket expresionArgs TkCloseBracket
                         | identificador TkOpenBracket expresionNormal TkCloseBracket
        '''
        if len(p) == 4:
            if (p[1]=='[' and p[3]==']'):
                p[0] = Grouped("Bracket", p[1], p[2], p[3])
        else:
            p[0] = ArrayExpression(p[1], p[3])
                

    def p_expresionArgs(p):
        '''
        expresionArgs : 
                      | expresion TkComma expresionArgs
                      | expresion  
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
    return yacc()

parseador = ejecutamosParseador()

# Funcion parse:
# Parse recibe la secuencia de caracteres correspondiente a la entrada 
# indicada por el usuario y retorna el AST correspondiente
def parse(input: str):

    ast = parseador.parse(input)

    return ast

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
    ast = parse(input)

    if len(arr) == 0:
        astString = ast2str(input, ast)
        return astString
    else:
        return f"Syntax error: {arr[0]}"

#########################################################

def procesarDefinicion(data, instruccion: Definition, ts: TablaDeSimbolos) -> str:
    if ts.existe_simbolo_en_ts(instruccion.id):
        return f"ERROR: identificador {instruccion.id} ya está definido"
    else:
        if isinstance(instruccion.expression, BinOp):
            resultado = procesarOperacionBinaria(data, instruccion.expression, ts)
            
            # Si resultado es un ERROR no se agrega a la tabla de simbolos.
            if f"{resultado}".startswith("ERROR"):
                return resultado
            else:
                # Se actualiza el simbolo en la tabla de simbolos
                ts.agregar_simbolo(Definition(instruccion.type, instruccion.id, Number(resultado)))

                return f"ACK: {instruccion.type} {instruccion.id} := {resultado};"

        elif isinstance(instruccion.expression, UnaOp):
            resultado = procesarOperacionUnaria(data, instruccion.expression, ts)

            # Si resultado es un ERROR no se agrega a la tabla de simbolos.
            if f"{resultado}".startswith("ERROR"):
                return resultado
            else:
                # Se actualiza el simbolo en la tabla de simbolos
                ts.agregar_simbolo(Definition(instruccion.type, instruccion.id, Number(resultado)))

                return f"ACK: {instruccion.type} {instruccion.id} := {resultado};"

        elif isinstance(instruccion.expression, Grouped):
            expresion = procesarAgrupacion(data, instruccion.expression, ts)
            
            # Si expresion es un ERROR no se agrega a la tabla de simbolos.
            if f"{expresion}".startswith("ERROR"):
                return expresion
            else:
                # Se agrega el simbolo a la tabla de simbolos
                ts.agregar_simbolo(Definition(instruccion.type, instruccion.id, expresion))

                # Se verifican el tipo de elementos del arreglo expresion
                if isinstance(expresion[0], bool):
                    expresion_str = list(map(lambda ele: f"{ele == True}".lower(), expresion))
                    return f"ACK: {instruccion.type} {instruccion.id} := {expresion_str};"

                # elif isinstance(expresion[0], int):
                else:
                    return f"ACK: {instruccion.type} {instruccion.id} := {expresion};"
        elif isinstance(instruccion.expression, Identifier):
            if ts.existe_simbolo_en_ts(instruccion.expression):
                simbolo = ts.valor_simbolo(instruccion.expression)

                ts.agregar_simbolo(Definition(instruccion.type, instruccion.id, simbolo))
                return f"ACK: {instruccion.type} {instruccion.id} := {simbolo};"

            else:
                return f"ERROR: identificador {instruccion.expression} no está definido"
        elif isinstance(instruccion.expression, Number):     
            # Se agrega el simbolo a la tabla de simbolos
            ts.agregar_simbolo(instruccion)
            # Definition(instruccion.type, instruccion.id, instruccion.expression.value)

            return f"ACK: {instruccion.type} {instruccion.id} := {instruccion.expression};"
        elif isinstance(instruccion.expression, Boolean):
            valor = instruccion.expression

            # Se agrega el simbolo a la tabla de simbolos
            ts.agregar_simbolo(instruccion)

            return f"ACK: {instruccion.type} {instruccion.id} := {valor.str_value};"

def procesarAsignacion(data, instruccion: Assignment, ts: TablaDeSimbolos) -> str:
    if ts.existe_simbolo_en_ts(instruccion.id):
        # Se actualiza el simbolo en la tabla de simbolos
        ts.actualizar_simbolo(instruccion)
        return f"ACK: {instruccion.id} := {instruccion.expression};"
    else:
        return f"ERROR: identificador {instruccion.id} no definido"
    
def procesarOperacionBinaria(data, instruccion, ts):
    if isinstance(instruccion, BinOp) :
        expLeft = procesarOperacionBinaria(data, instruccion.left, ts)
        expRight = procesarOperacionBinaria(data, instruccion.right, ts)

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
        else:
            if instruccion.op == "^" : respuesta = expLeft ** expRight
            elif instruccion.op == "*" : respuesta = expLeft * expRight
            elif instruccion.op == "/" : respuesta = expLeft // expRight
            elif instruccion.op == "%" : respuesta = expLeft % expRight
            elif instruccion.op == "+" : respuesta = expLeft + expRight
            elif instruccion.op == "-" : respuesta = expLeft - expRight
            elif instruccion.op == "<" : respuesta = expLeft < expRight
            elif instruccion.op == "<=" : respuesta = expLeft <= expRight
            elif instruccion.op == ">=" : respuesta = expLeft >= expRight
            elif instruccion.op == ">" : respuesta = expLeft > expRight
            elif instruccion.op == "=" : respuesta = expLeft == expRight
            elif instruccion.op == "<>" : respuesta = expLeft != expRight
            elif instruccion.op == "&&" : respuesta = expLeft & expRight
            elif instruccion.op == "||" : respuesta = expLeft | expRight
    
            return respuesta

    elif isinstance(instruccion, Number):
        return procesarNumero(data, instruccion, ts)
    elif isinstance(instruccion, Boolean):
        return procesarBoolean(data, instruccion, ts)
    elif isinstance(instruccion, Identifier):
        return procesarIdentificador(data, instruccion, ts)
    elif isinstance(instruccion, UnaOp):
        return procesarOperacionUnaria(data, instruccion, ts)
    elif isinstance(instruccion, Grouped):
        return procesarAgrupacion(data, instruccion, ts)
    elif isinstance(instruccion, ArrayExpression):
        return procesarArregloInstruccion(data, instruccion, ts)
    else: 
        return f"ERROR: instrucción no válida."

def procesarNumero(data, instruccion: Number, ts: TablaDeSimbolos) -> str:
    return instruccion.value

def procesarIdentificador(data, instruccion: Identifier, ts: TablaDeSimbolos) -> int or bool:
    # Verifiquemos que el identificador exista en la tabla de simbolos
    if ts.existe_simbolo_en_ts(instruccion):
        valorEncontrado = ts.obtener_simbolo(instruccion)

        if isinstance(valorEncontrado.expression, Number) or isinstance(valorEncontrado.expression, Boolean):
            return valorEncontrado.expression.value
        elif isinstance(valorEncontrado.expression, list):
            return valorEncontrado.expression
    else:
        return f"ERROR: identificador {instruccion.value} no definido"

def procesarOperacionUnaria(data, instruccion, ts: TablaDeSimbolos) -> str:
    if isinstance(instruccion, UnaOp):
        exp = procesarOperacionUnaria(data, instruccion.right, ts)
        if instruccion.op == "+" : return exp
        if instruccion.op == "-" : return -exp
        if instruccion.op == "!" : return not exp

    elif isinstance(instruccion, Number):
        return procesarNumero(data, instruccion, ts)
    elif isinstance(instruccion, Boolean):
        return procesarBoolean(data, instruccion, ts)
    elif isinstance(instruccion, Identifier):
        return procesarIdentificador(data, instruccion, ts)
    elif isinstance(instruccion, Grouped):
        return procesarAgrupacion(data, instruccion, ts)

def procesarAgrupacion(data, instruccion, ts) -> str:
    
    if isinstance(instruccion, Grouped) & (instruccion.type == "Par"):
            exp = procesarAgrupacion(data, instruccion.expression, ts)
            return exp

    elif isinstance(instruccion, Grouped) & (instruccion.type == "Brace"):
            exp = procesarAgrupacion(data, instruccion.expression, ts)
            return exp

    elif isinstance(instruccion, Grouped) & (instruccion.type == "SingleQuote"):
            print("SingleQuote")
            #TODO
            pass

    elif isinstance(instruccion, Grouped) & (instruccion.type == "Bracket"):
            instruccion = instruccion.expression
            arregloTemp = []

            # Casos en el que el arreglo tiene un solo elemento
            if isinstance(instruccion, Number) | isinstance(instruccion, Identifier) | isinstance(instruccion, Boolean):
                respuesta = instruccion.value

                # Si el unico elemento es un ERROR, se retorna el error.
                if f"{respuesta}".startswith("ERROR"):
                    return respuesta
                else:
                    arregloTemp.append(respuesta)

            elif isinstance(instruccion, UnaOp):
                respuesta = procesarOperacionUnaria(data, instruccion, ts)
                
                # Si el unico elemento es un ERROR, se retorna el error.
                if f"{respuesta}".startswith("ERROR"):
                    return respuesta
                else:
                    arregloTemp.append(respuesta)

            elif isinstance(instruccion, ArrayExpression):
                respuesta = procesarArregloInstruccion(data, instruccion, ts)
                
                # Si el unico elemento es un ERROR, se retorna el error.
                if f"{respuesta}".startswith("ERROR"):
                    return respuesta
                else:
                    arregloTemp.append(respuesta)
                
            elif isinstance(instruccion, Grouped):
                respuesta = procesarAgrupacion(data, instruccion, ts)
                
                # Si el unico elemento es un ERROR, se retorna el error.
                if f"{respuesta}".startswith("ERROR"):
                    return respuesta
                else:
                    arregloTemp.append(respuesta)
                
            elif isinstance(instruccion, BinOp) & (instruccion.op in "^*/%+-<<=>=>=<>&&||"):
                respuesta = procesarOperacionBinaria(data, instruccion, ts)
                
                # Si el unico elemento es un ERROR, se retorna el error.
                if f"{respuesta}".startswith("ERROR"):
                    return respuesta
                else:
                    arregloTemp.append(respuesta)
            
            # Caso de que el arreglo tiene mas de un elemento
            elif isinstance(instruccion, BinOp) & (instruccion.op == ","):
                # print(arregloTemp)

                # Se obtiene el primer elemento del arreglo
                izquierda = instruccion.left
                if isinstance(izquierda, Number) | isinstance(izquierda, Identifier) | isinstance(izquierda, Boolean):
                    respuesta = izquierda.value
                elif isinstance(izquierda, UnaOp):
                    respuesta = procesarOperacionUnaria(data, izquierda, ts)
                elif isinstance(izquierda, ArrayExpression):
                    respuesta = procesarArregloInstruccion(data, izquierda, ts)
                elif isinstance(izquierda, Grouped):
                    respuesta = procesarAgrupacion(data, izquierda, ts)
                elif isinstance(izquierda, BinOp) & (izquierda.op in "^*/%+-<<=>=>=<>&&||"):
                    respuesta = procesarOperacionBinaria(data, izquierda, ts)
                
                # Si el primer elemento es un ERROR, se retorna el error, si no se continua con el procesamiento
                if f"{respuesta}".startswith("ERROR"):
                    return respuesta
                else:
                    arregloTemp.append(respuesta)
                
                # Se obtienen los elementos del medio del arreglo, si los hay
                derecha = instruccion.right
                while isinstance(derecha, BinOp):
                    if (derecha.op == ","):
                        # print(arregloTemp)
                        izquierda = derecha.left
                        if isinstance(izquierda, Number) | isinstance(izquierda, Identifier) | isinstance(izquierda, Boolean):
                            respuesta = izquierda.value
                        elif isinstance(izquierda, UnaOp):
                            respuesta = procesarOperacionUnaria(data, izquierda, ts)
                        elif isinstance(izquierda, ArrayExpression):
                            respuesta = procesarArregloInstruccion(data, izquierda, ts)
                        elif isinstance(izquierda, Grouped):
                            respuesta = procesarAgrupacion(data, izquierda, ts)
                        elif isinstance(izquierda, BinOp) & (izquierda.op in "^*/%+-<<=>=>=<>&&||"):
                            respuesta = procesarOperacionBinaria(data, izquierda, ts)

                        # Si el elemento es un ERROR, se retorna el error, si no se continua con el procesamiento
                        if f"{respuesta}".startswith("ERROR"):
                            return respuesta
                        else:
                            arregloTemp.append(respuesta)

                        derecha = derecha.right

                    else:
                        break

                # Se obtiene el ultimo elemento del arreglo
                # print(arregloTemp)
                if isinstance(derecha, Number) | isinstance(derecha, Identifier) | isinstance(derecha, Boolean):
                    respuesta = derecha.value
                elif isinstance(derecha, UnaOp):
                    respuesta = procesarOperacionUnaria(data, derecha, ts)
                elif isinstance(derecha, ArrayExpression):
                    respuesta = procesarArregloInstruccion(data, derecha, ts)
                elif isinstance(derecha, Grouped):
                    respuesta = procesarAgrupacion(data, derecha, ts)
                elif isinstance(derecha, BinOp) & (derecha.op in "^*/%+-<<=>=>=<>&&||"):
                    respuesta = procesarOperacionBinaria(data, derecha, ts)
                    
                # Si el ultimo elemento es un ERROR, se retorna el error.
                if f"{respuesta}".startswith("ERROR"):
                    return respuesta
                else:
                    arregloTemp.append(respuesta)
                
            
            return arregloTemp

    elif isinstance(instruccion, Number):
        return procesarNumero(data, instruccion, ts)
    elif isinstance(instruccion, Boolean):
        return procesarBoolean(data, instruccion, ts)
    elif isinstance(instruccion, Identifier):
        return procesarIdentificador(data, instruccion, ts)
    elif isinstance(instruccion, UnaOp):
        return procesarOperacionUnaria(data, instruccion, ts)
    elif isinstance(instruccion, BinOp):
        return procesarOperacionBinaria(data, instruccion, ts)

def procesarArregloInstruccion(data, instruccion: ArrayExpression, ts: TablaDeSimbolos) -> str:
    # Verifiquemos que el identificador exista en la tabla de simbolos
    if ts.existe_simbolo_en_ts(instruccion.id):
        definicionArreglo = ts.obtener_simbolo(instruccion.id)
        arreglo = definicionArreglo.expression
        try:
            return arreglo[instruccion.index.value]

            # return f"OK: {instruccion.id.value}[{instruccion.index.value}] ==> {resultado};"
        except IndexError:
            return f"ERROR: indice fuera de rango"
    else:
        return f"ERROR: variable {instruccion.id.value} no definida"

def procesarBoolean(data, instruccion: Boolean, ts: TablaDeSimbolos) -> str:
    return instruccion.value

# def procesarConditional(data, instruccion: Conditional, ts):
#     condicion = procesarOperacionBinaria(data, instruccion.condicion, ts)
#     if condicion == "true":
#         return procesarOperacionBinaria(data, instruccion.expT, ts)
#     else:
#         return procesarOperacionBinaria(data, instruccion.expF, ts)

# def procesarReset(instruccion: Reset, ts: TablaDeSimbolos) -> str:
#     hola = ts.limpiar_ts()

#     if hola:
#         return "true"




# Funcion procesar_instruccion:
# Recibe una instruccion y la procesa
def procesar_instruccion(data: str, ts: TablaDeSimbolos) -> str:

    # Llamamos a parser con el data ingresado por el usuario
    instruccion = parse(data)
    # print(type(instruccion))
    # print(type(instruccion.id))
    # print(type(instruccion.index))

    # Si la instruccion es una declaracion de variable
    if isinstance(instruccion, Definition): 
        return procesarDefinicion(data, instruccion, ts)

    elif isinstance(instruccion, Assignment): 
        return procesarAsignacion(data, instruccion, ts)

    elif isinstance(instruccion, BinOp):
        respuesta = procesarOperacionBinaria(data, instruccion, ts)
        # Verificar si la respuesta es un ERROR
        if isinstance(respuesta, str):
            if respuesta.startswith("ERROR"):
                return respuesta
            else:
                return f"OK: {data} ==> {respuesta}"
        elif isinstance(respuesta, bool):
            respuesta = f"{respuesta}".lower()
            return f"OK: {data} ==> '{respuesta}'"

            # if respuesta:
            #     return f"OK: {data} ==> true"
            # else:
            #     return f"OK: {data} ==> false"
        else:
            return f"OK: {data} ==> {respuesta}"

    elif isinstance(instruccion, Number): 
        respuesta = procesarNumero(data, instruccion, ts)
        return f"OK: {data} ==> {respuesta}"

    elif isinstance(instruccion, Identifier): 
        respuesta =  procesarIdentificador(data, instruccion, ts)
        # Se verifican el tipo de elementos de respuesta o si la respuesta es un ERROR
        if isinstance(respuesta, str):
            if respuesta.startswith("ERROR"):
                return respuesta

        elif isinstance(respuesta, bool):
            if respuesta:
                return f"OK: {data} ==> true"
            else:
                return f"OK: {data} ==> false"

        elif isinstance(respuesta, int):
            return f"OK: {data} ==> {respuesta}"

        elif isinstance(respuesta, list):
            if isinstance(respuesta[0], bool):
                respuesta_str = list(map(lambda ele: f"{ele == True}".lower(), respuesta))
                return f"OK: {data} ==> {respuesta_str}"

            elif isinstance(respuesta[0], int):
                return f"OK: {data} ==> {respuesta}"


    elif isinstance(instruccion, UnaOp): 
        respuesta = procesarOperacionUnaria(data, instruccion, ts)
        # Verificar si la respuesta es un ERROR
        if isinstance(respuesta, str):
            if respuesta.startswith("ERROR"):
                return respuesta
        elif isinstance(respuesta, bool):
            if respuesta:
                return f"OK: {data} ==> true"
            else:
                return f"OK: {data} ==> false"
        return f"OK: {data} ==> {respuesta}"

    elif isinstance(instruccion, Grouped): 
        respuesta = procesarAgrupacion(data, instruccion, ts)
        # Verificar si la respuesta es un ERROR
        if isinstance(respuesta, str):
            if respuesta.startswith("ERROR"):
                return respuesta
            else:
                # respuesta = f"{respuesta}".lower()
                return f"OK: {data} ==> {respuesta}"
        elif isinstance(respuesta, bool):
            if respuesta:
                return f"OK: {data} ==> true"
            else:
                return f"OK: {data} ==> false"
        else:
            return f"OK: {data} ==> {respuesta}"

    elif isinstance(instruccion, ArrayExpression): 
        respuesta = procesarArregloInstruccion(data, instruccion, ts)
        # Verificar si la respuesta es un ERROR
        if isinstance(respuesta, str):
            if respuesta.startswith("ERROR"):
                return respuesta

        else:
            # Se verifican el tipo de elementos de respuesta
            if isinstance(respuesta, bool):
                return f"OK: {data} ==> {str(respuesta).lower()}"

            # elif isinstance(respuesta, int):
            else:
                return f"OK: {data} ==> {respuesta}"

    elif isinstance(instruccion, Boolean): 
        respuesta = procesarBoolean(data, instruccion, ts)
        # Verificar si la respuesta es un ERROR
        if isinstance(respuesta, str):
            if respuesta.startswith("ERROR"):
                return respuesta
        else:
            respuesta = f"{respuesta}".lower()
            return f"OK: {data} ==> {respuesta}"

    else: 
        return f"ERROR: instrucción no válida."

