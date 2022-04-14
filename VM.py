'''
Grupo Dacary: 
                Gregory Muñoz   16-11313
                Daniela Ramirez 16-10940
                Giancarlo Dente 15-10395
'''

#import ply.lex as lex
from ast import Expression
from ply.lex import lex
from ply.yacc import yacc
from Objetos import *
import random
import math
import time

ts_global = TablaDeSimbolos()

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
        expresionNormal : expresionNumerica
                        | expresionLogica
                        | expresionArreglo
                        | expresionFunciones
        '''
        p[0] = p[1]
    
    def p_expresionNumerica(p):
        '''
        expresionNumerica : numero 
                          | identificador
                          | TkOpenPar expresionNumerica TkClosePar
                          | TkOpenBrace expresionNumerica TkCloseBrace
                          | expresionNumerica TkPower expresionNumerica
                          | TkPlus expresionNumerica %prec TkUPlus
                          | TkMinus expresionNumerica %prec TkUMinus
                          | expresionNumerica TkMult expresionNumerica
                          | expresionNumerica TkDiv expresionNumerica
                          | expresionNumerica TkMod expresionNumerica
                          | expresionNumerica TkPlus expresionNumerica
                          | expresionNumerica TkMinus expresionNumerica
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
    
    def p_expresionLogica(p):
        '''
        expresionLogica : booleano
                        | identificador
                        | TkOpenPar expresionLogica TkClosePar
                        | TkOpenBrace expresionLogica TkCloseBrace
                        | TkNot expresionLogica
                        | expresionNumerica TkLT expresionNumerica
                        | expresionNumerica TkLE expresionNumerica
                        | expresionNumerica TkGE expresionNumerica
                        | expresionNumerica TkGT expresionNumerica
                        | expresionNumerica TkEQ expresionNumerica
                        | expresionNumerica TkNE expresionNumerica
                        | expresionLogica TkEQ expresionLogica
                        | expresionLogica TkNE expresionLogica
                        | expresionLogica TkAnd expresionLogica
                        | expresionLogica TkOr expresionLogica   
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
    
    def p_booleano(p):
        '''
        booleano : TkTrue
                 | TkFalse
        '''
        p[0] = Boolean(p[1])
    
    def p_expresionArreglo(p):
        '''
        expresionArreglo : TkOpenBracket expresionArgs TkCloseBracket
                         | identificador TkOpenBracket expresionNumerica TkCloseBracket
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
        # print(f'Syntax error at {p.value!r}')
        # p[0] = f'Syntax error at {p}'
        if p == None:
            token = 'EOF'
        else:
            token = f"{p.type}({p.value}) at line {p.lineno}"
            
        print(f"Syntax error at {token}")

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

    # Eliminamos los espacios antes y despues de la expresión
    input = input[4:].strip()

    # Llamamos a parser con el input ingresado por el usuario
    ast = parse(input)

    astString = ast2str(input, ast)

    return astString

#########################################################

def procesarDefinicion(instruccion: Definition, ts: TablaDeSimbolos) -> str:
    if isinstance(instruccion.expression, BinOp):
        resultado = procesarOperacionBinaria(instruccion.expression, ts)
        
        # Se actualiza el simbolo en la tabla de simbolos
        ts.agregar_simbolo(Definition(instruccion.type, instruccion.id, resultado))

        return f"ACK: {instruccion.type} {instruccion.id} := {resultado};"

    elif isinstance(instruccion.expression, UnaOp):
        pass
    elif isinstance(instruccion.expression, Grouped):
        pass
    elif isinstance(instruccion.expression, Identifier):
        pass
    elif isinstance(instruccion.expression, Number):     
        # Se agrega el simbolo a la tabla de simbolos
        ts.agregar_simbolo(instruccion)

        return f"ACK: {instruccion.type} {instruccion.id} := {instruccion.expression};"

def procesarAsignacion(instruccion: Assignment, ts: TablaDeSimbolos) -> str:
    if ts.existe_simbolo_en_ts(instruccion.id):
        # Se actualiza el simbolo en la tabla de simbolos
        ts.actualizar_simbolo(instruccion)
        return f"ACK: {instruccion.id} := {instruccion.expression};"
    else:
        return f"ERROR: identificador {instruccion.id} no definido"
    
def procesarOperacionBinaria(instruccion, ts):
    if isinstance(instruccion, BinOp) :
        expLeft = procesarOperacionBinaria(instruccion.left, ts)
        expRight = procesarOperacionBinaria(instruccion.right, ts)
        if instruccion.op == "^" : return expLeft ** expRight
        if instruccion.op == "*" : return expLeft * expRight
        if instruccion.op == "/" : return expLeft // expRight
        if instruccion.op == "+" : return expLeft + expRight
        if instruccion.op == "-" : return expLeft - expRight
        if instruccion.op == "<" : return f"{expLeft < expRight}".lower()
        if instruccion.op == "<=" : return f"{expLeft <= expRight}".lower()
        if instruccion.op == ">=" : return f"{expLeft >= expRight}".lower()
        if instruccion.op == ">" : return f"{expLeft > expRight}".lower()
        if instruccion.op == "=" : return f"{expLeft == expRight}".lower()
        if instruccion.op == "<>" : return f"{expLeft != expRight}".lower()
        if instruccion.op == "&&" : return f"{expLeft & expRight}".lower()
        if instruccion.op == "||" : return f"{expLeft | expRight}".lower()
    elif isinstance(instruccion, Number):
        return instruccion.value
    elif isinstance(instruccion, Boolean):
        return instruccion.value
    elif isinstance(instruccion, Identifier):
        if ts.existe_simbolo_en_ts(instruccion):
            return ts.valor_simbolo(instruccion).value
        else:
            return f"ERROR: identificador {instruccion} no definido"
    elif isinstance(instruccion, UnaOp):
        return procesarOperacionUnaria(instruccion, ts)
    elif isinstance(instruccion, Grouped):
        return procesarAgrupacion(instruccion.expression, ts)

def procesarNumero(instruccion: Number, ts: TablaDeSimbolos) -> str:
    return instruccion.value

def procesarIdentificador(instruccion: Identifier, ts: TablaDeSimbolos) -> str:
    if ts.existe_simbolo_en_ts(instruccion):
        valorEncontrado = ts.obtener_simbolo(instruccion)
        return f"OK: {instruccion.value} ==> {valorEncontrado.expression};"
    else:
        return f"ERROR: identificador {instruccion.value} no definido"

def procesarOperacionUnaria(instruccion, ts: TablaDeSimbolos) -> str:
    if isinstance(instruccion, UnaOp):
        exp = procesarOperacionUnaria(instruccion.right, ts)
        if instruccion.op == "+" : return exp
        if instruccion.op == "-" : return -exp
        if instruccion.op == "!" : return not exp

    elif isinstance(instruccion, Number):
        return  instruccion.value
            
    elif isinstance(instruccion, Identifier):
        return ts.valor_simbolo(instruccion)

    elif isinstance(instruccion, Boolean):
        return instruccion.value

def procesarAgrupacion(instruccion, ts: TablaDeSimbolos) -> str:

    if isinstance(instruccion, Grouped):
        if instruccion.type == "Par":
            if isinstance(instruccion.expression, Grouped):          
                return procesarAgrupacion(instruccion.expression, ts)
            elif isinstance(instruccion.expression, BinOp):
                return procesarOperacionBinaria(instruccion.expression, ts)
            elif isinstance(instruccion.expression, Number):
                return instruccion.expression.value
            elif isinstance(instruccion.expression, Boolean):
                return f"{instruccion.expression.value}".lower()
            elif isinstance(instruccion.expression, Identifier):
                return ts.valor_simbolo(instruccion.expression)
            elif isinstance(instruccion.expression, UnaOp):
                return procesarOperacionUnaria(instruccion.expression, ts)
            
        elif instruccion.type == "SingleQuote":
            if isinstance(instruccion.expression, Grouped):
                return instruccion.expression
            elif isinstance(instruccion.expression, BinOp):
                return f"{instruccion.expression.left} {instruccion.expression.op} {instruccion.expression.right}"
            elif isinstance(instruccion.expression, Number):
                return instruccion.expression.value
            elif isinstance(instruccion.expression, Boolean):
                return f"{instruccion.expression.value}".lower()
            elif isinstance(instruccion.expression, Identifier):
                return instruccion.expression.value
            elif isinstance(instruccion.expression, UnaOp):
                return f"{instruccion.expression.op}{instruccion.expression.right}"

    elif isinstance(instruccion, Number):
        return instruccion.value

def procesarArregloInstruccion(instruccion: ArrayExpression, ts: TablaDeSimbolos) -> str:
    return instruccion

def procesarBoolean(instruccion: Boolean, ts: TablaDeSimbolos) -> str:
    return instruccion.value

def procesarConditional(instruccion: Conditional, ts):
    condicion = procesarOperacionBinaria(instruccion.condicion, ts)
    if condicion == "true":
        return procesarOperacionBinaria(instruccion.expT, ts)
    else:
        return procesarOperacionBinaria(instruccion.expF, ts)

# def procesarReset(instruccion: Reset, ts: TablaDeSimbolos) -> str:
#     hola = ts.limpiar_ts()

#     if hola:
#         return "true"




# Funcion procesar_instruccion:
# Recibe una instruccion y la procesa
def procesar_instruccion(input: str, ts: TablaDeSimbolos) -> str:

    # Llamamos a parser con el input ingresado por el usuario
    instruccion = parse(input)
    # print(type(instruccion))

    # print(type(instruccion))
    # print(type(instruccion.expression))

    # Si la instruccion es una declaracion de variable
    if isinstance(instruccion, Definition): return procesarDefinicion(instruccion, ts)
    elif isinstance(instruccion, Assignment): return procesarAsignacion(instruccion, ts)
    elif isinstance(instruccion, BinOp): return procesarOperacionBinaria(instruccion, ts)
    elif isinstance(instruccion, Number): return procesarNumero(instruccion, ts)
    elif isinstance(instruccion, Identifier): return procesarIdentificador(instruccion, ts)
    elif isinstance(instruccion, UnaOp): return procesarOperacionUnaria(instruccion, ts)
    elif isinstance(instruccion, Grouped): return procesarAgrupacion(instruccion, ts)
    elif isinstance(instruccion, ArrayExpression): return procesarArregloInstruccion(instruccion, ts)
    elif isinstance(instruccion, Boolean): return procesarBoolean(instruccion, ts)
    elif isinstance(instruccion, Conditional): return procesarConditional(instruccion, ts)
    # elif isinstance(instruccion, Type): return procesarType(instruccion, ts)
    # elif isinstance(instruccion, Ltype): return procesarLtype(instruccion, ts)
    # elif isinstance(instruccion, Reset): return procesarReset(instruccion, ts)
    # elif isinstance(instruccion, Uniform): return procesarUniform(instruccion, ts)
    # elif isinstance(instruccion,Floor): return procesarFloor(instruccion, ts)
    # elif isinstance(instruccion,Length): return procesarLength(instruccion, ts)
    # elif isinstance(instruccion, Sum): return procesarSum(instruccion, ts)
    # elif isinstance(instruccion, Avg): return procesarAvg(instruccion, ts)
    # elif isinstance(instruccion, Pi): return procesarPi(instruccion, ts)
    # elif isinstance(instruccion, Now): return procesarNow(instruccion, ts)
    else : print('ERROR: instrucción no válida')

