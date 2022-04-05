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
def process (input: str, arrayTuplas: list) -> str:

    if input.startswith('.lex'):        
        data, arrayTokens, arrayErrores = lexTest(input)
        return mensajeLexer(data, arrayTokens, arrayErrores)

    elif input.startswith('.load'):
        return load(input, arrayTuplas)

    elif input.startswith('.failed'):
        return failed(arrayTuplas)

    elif input == "":
        return ""

    else:
        return procesar_instruccion(input, ts_global)

        # # Eliminamos los espacios antes y despues de la expresión
        # input = input.strip().split()
        
        # if input[0] == 'int' or input[0] == 'bool' or input[0] == '[int]' or input[0] == '[bool]':

        #     # Almacenamos en el diccionario identificadores el nombre de la variable, su tipo y su valor
        #     identificadores[input[1]] = (input[0], input[3])

        #     print(identificadores)
        
        # return identificadores


        #return f"ERROR: interpretación no implementada"


# Crea
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
        'TkColon',

        # Funciones predefinidas
        'TkIf',
        'TkType',
        'TkLtype',
        'TkReset',
        'TkUniform',
        'TkFloor',
        'TkLength',
        'TkSum',
        'TkAvg',
        'TkPi',
        'TkNow'
    )

    # Tokens con regex
    # Tokens palabras reservadas
    reservados = {
        'num' : 'TkNum',
        'bool' : 'TkBool',
        'false' : 'TkFalse',
        'true' : 'TkTrue',
        'if' : 'TkIf',
        'type' : 'TkType',
        'ltype' : 'TkLtype',
        'reset' : 'TkReset',
        'uniform' : 'TkUniform',
        'floor' : 'TkFloor',
        'length' : 'TkLength',
        'sum' : 'TkSum',
        'avg' : 'TkAvg',
        'pi' : 'TkPi',
        'now' : 'TkNow'
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
    
# Funcion mensajeLexer
def mensajeLexer(data: str, arrayTokens: list, arrayErrores: list) -> str:
    
    if (len(arrayErrores) > 0):
        return f"ERROR: caracter inválido ({arrayErrores[0]}) en la entrada"
    
    else:
        return f'OK: lex("{data}") ==> {arrayTokens}'

# Funcion load
def load (data: str, arrayTuplas: list) -> str:

    mensajeLoad = ""
    
    try: 
        data = data[5:].strip()
        file1 = open(data, "r")
        
    except:
        return f"ERROR: archivo no encontrado." 
        
    Lines = file1.readlines()
    nombreArchivo = data
                
    numline = 0 
    
    for line in Lines:
        numline += 1

        # Ignoramos las lineas en blanco o espacios en blanco o tabulaciones
        if not line.isspace():
            data = line.strip()

            # Archivo contiene .lex en la linea numline
            if data.startswith('.lex'):
                data, arrayTokens, arrayErrores = lexTest(data)
                mensaje = mensajeLexer(data, arrayTokens, arrayErrores)
                mensajeLoad = mensajeLoad + f"{mensaje}\n"

                # Si la respuesta da ERROR se guarda el nombre del archivo, la linea y el mensaje en una lista de tuplas
                if mensaje.startswith('ERROR: '):
                    arrayTuplas.append((nombreArchivo, numline, mensaje))

            # Archivo contiene otros nombres de archivos dentro
            elif data.startswith('.load'):
                mensaje = load(data, arrayTuplas)       
                mensajeLoad = mensajeLoad + f"{mensaje}\n"

            # Archivo contiene .failed en la linea numline
            elif data.startswith('.failed'):
                mensajeLoad = mensajeLoad + f"{failed(arrayTuplas)}\n"

            # Archivo contiene .reset en la linea numline
            elif data.startswith('.reset'):
                reset(arrayTuplas)

            # Archivo contiene .ast en la linea numline
            elif data.startswith('.ast'):
                mensaje = testParser(data)
                mensajeLoad = mensajeLoad + f"{mensaje}\n"
            
            # Si no se ingresa alguno de los comandos especificados se devuelve ERROR
            elif not data.startswith('.lex') or not data.startswith('.load') or not data.startswith('.failed') or not data.startswith('.reset') or not data.startswith('.ast'):
                arrayTuplas.append((nombreArchivo, numline, f"ERROR: interpretación no implementada"))
                mensajeLoad = mensajeLoad + f"ERROR: interpretación no implementada\n"

    file1.close()

    return mensajeLoad[:len(mensajeLoad)-1]    # return mensajeLoad[:len(mensajeLoad)-1] para no incluir ultima linea en blanco
 
# Funcion failed
def failed (arrayTuplas: list) -> str:
    msjFailed = f"[\n"

    if len(arrayTuplas) > 0:
        for i in range(0, len(arrayTuplas)-1):
            msjFailed = msjFailed + f"\t{arrayTuplas[i]},\n"

        msjFailed = msjFailed + f"\t{arrayTuplas[len(arrayTuplas)-1]}\n"
        
    msjFailed = msjFailed + f"]"

    return msjFailed

# Funcion reset
def reset(arrayTuplas):
    for i in range(0, len(arrayTuplas)):
        arrayTuplas.pop()
        
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
def reset():
    identificadores.clear()    
    if len(identificadores) == 0:
        print(True)

# Funcion now, retorna un número entero correspondiente al número de milisegundos transcurridos desde un
# punto de referencia en el tiempo
def now():
    return int(round(time.time() * 1000))

#########################################################

class Expr: pass

class Uniform():
    def __init__(self):
        self = None
        
    def __repr__(self):
        return f"{uniform()}"

class Floor(Expr):
    def __init__(self,expression):
        self.expression = expression
        
    def __repr__(self):
        return f"{floor(self.expression)}"

class Length(Expr):
    def __init__(self,expression):
        self.expression = expression
        
    def __repr__(self):
        return f"{length(self.expression)}"
    
class Sum(Expr):
    def __init__(self,expression):
        self.expression = expression
        
    def __repr__(self):
        return f"{sum(self.expression)}"
    
class Avg(Expr):
    def __init__(self,expression):
        self.expression = expression
        
    def __repr__(self):
        return f"{avg(self.expression)}"
    
class Pi():
    def __init__(self):
        self = None
        
    def __repr__(self):
        return f"{pi()}"

class Reset():
    def __init__(self):
        self = None
        
    def __repr__(self):
        return f"{reset()}"

class Now():
    def __init__(self):
        self = None
        
    def __repr__(self):
        return str(now())
    
# class Conditional(Expr):
#     def __init__(self, condicion, expT, expF):
#         self.condicion = condicion
#         self.expT = expT
#         self.expF = expF
        
class Type(Expr):
    def __init__(self,expression):
        self.expression = expression
        
class Ltype(Expr):
    def __init__(self,expression):
        self.expression = expression    
    
#########################################################

# Funcion parse:
# Parse recibe la secuencia de caracteres correspondiente a la entrada 
# indicada por el usuario y retorna el AST correspondiente
def parse(input: str):

    # Construimos el objecto lexer y el arreglo de errores
    tokens, lexer, arrayErrores = ejecutarLexer()

    # Entrada para el lexer
    lexer.input(input)

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
        ('left', 'TkPower')
    )

    def p_entrada(p):
        '''
        entrada : 
                | instruccion 
                | expresion
                | funcion
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

        # Definition(p[1], p[2], p[4]).definir()

    def p_asignacion(p):
        '''
        asignacion : identificador TkAssign expresion TkSemicolon
        '''
        p[0] = Assignment(p[1], p[3])
        # Assignment(p[1], p[3]).asignar()

    def p_tipo(p):
        '''
        tipo : tipoBasico
               | tipoNoBasico
        '''
        p[0] = p[1]

    def p_tipoBasico(p):
        '''
        tipoBasico : TkNum
                     | TkBool
        '''
        p[0] = BasicType(p[1])

    def p_tipoNoBasico(p):
        '''
        tipoNoBasico : TkOpenBracket tipoBasico TkCloseBracket
        '''
        p[0] = Grouped("Bracket", p[1], p[2], p[3])

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
        expresionArreglo : TkOpenBracket expresionArregloLLamada TkCloseBracket
                           | expresionArregloInstruccion
        '''
        if len(p) == 2:
            p[0] = p[1]

        elif len(p) == 4:
            if (p[1]=='[' and p[3]==']'):
                p[0] = Grouped("Bracket", p[1], p[2], p[3])

    def p_expresionArregloLLamada(p):
        '''
        expresionArregloLLamada : expresion TkComma expresionArregloLLamada
                                | expresion  
        '''
        if len(p) == 2:
            p[0] = p[1]

        elif len(p) == 4:
            p[0] = BinOp(p[1], p[2], p[3])

    def p_expresionArregloInstruccion(p):
        '''
        expresionArregloInstruccion : identificador TkOpenBracket expresionNumerica TkCloseBracket
        '''
        p[0] = ArrayInstruction(p[1], p[3])

    def p_funcion(p):
        ''' 
        funcion : TkIf TkOpenPar condicion TkComma expT TkComma expF TkClosePar
                | TkType TkOpenPar expresionNormal TkClosePar
                | TkLtype TkOpenPar expresionNormal TkClosePar
                | TkReset TkOpenPar TkClosePar
                | TkUniform TkOpenPar TkClosePar
                | TkFloor TkOpenPar expresionNumerica TkClosePar
                | TkLength TkOpenPar expresionArreglo TkClosePar
                | TkSum TkOpenPar expresionNumerica TkClosePar
                | TkAvg TkOpenPar expresionNumerica TkClosePar
                | TkPi TkOpenPar TkClosePar
                | TkNow TkOpenPar TkClosePar
        '''
        if len(p) == 4:
            if (p[1] == 'reset'):
                p[0] = Reset()
                
            elif(p[1] == 'uniform'):
                p[0] = Uniform()
                
            elif(p[1] == 'pi'):
                p[0] = Pi()
                
            elif(p[1] == 'now'):
                p[0] = Now()
        
        elif len(p) == 5:
            if (p[1] == 'floor'):
                p[0] = Floor(p[3])
                
            elif (p[1] == 'length'):
                p[0] = Length(p[3])
            
            elif (p[1] == 'sum'):
                p[0] = Sum(p[3])
            
            elif (p[1] == 'avg'):
                p[0] = Avg(p[3])
                
            elif (p[1] == 'type'):
                p[0] = Type(p[3])
                
            elif (p[1] == 'ltype'):
                p[0] = Ltype(p[3])
        
        elif len(p) == 9:
            if (p[1] == 'if'):
                p[0] = Conditional(p[3], p[5], p[7])

    def p_condicion(p):
        '''
        condicion : expresionLogica
        '''
        p[0] = p[1]
        
    def p_expT(p):
        '''
        expT : expresion
        '''
        p[0] = p[1]
        
    def p_expF(p):
        '''
        expF : expresion
        '''
        p[0] = p[1]

    def p_error(p):
        print(f'Syntax error at {p.value!r}')

    # Construyendo el parser de yacc
    parseador = yacc()

    ast = parseador.parse(input)

    return ast

# Funcion ast2str:
# Técnicamente, ast2str implementa una traducción. Para simplificar la 
# traducción, y hacerla amigable, las expresiones deben ser regeneradas con 
# paréntesis redundantes usando notación infija:
def ast2str(ast) -> str:
    return(f'{ast}')

# Funcion testParser:
# Llama a parse y convierte el AST resultante en un string que puede ser 
# consumido por el REPL
def testParser(input: str) -> str:

    # Eliminamos los espacios antes y despues de la expresión
    input = input[4:].strip()

    # Llamamos a parser con el input ingresado por el usuario
    ast = parse(input)

    astString = ast2str(ast)

    return astString

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
    # Se actualiza el simbolo en la tabla de simbolos
    ts.actualizar_simbolo(instruccion)

    return f"ACK: {instruccion.id} := {instruccion.expression};"

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
        return ts.valor_simbolo(instruccion).value
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


            # elif instruccion.type == "Bracket": return f"{instruccion.left}{instruccion.expression}{instruccion.right}"
            # elif instruccion.type == "SingleQuote": return f"{instruccion.expression}"
            # elif instruccion.type == "Brace": return f"{instruccion.left}{instruccion.expression}{instruccion.right}"

def procesarArregloInstruccion(instruccion: ArrayInstruction, ts: TablaDeSimbolos) -> str:
    return instruccion

def procesarBoolean(instruccion: Boolean, ts: TablaDeSimbolos) -> str:
    return instruccion.value

def procesarConditional(instruccion: Conditional, ts):
    condicion = procesarOperacionBinaria(instruccion.condicion, ts)
    if condicion == "true":
        return procesarOperacionBinaria(instruccion.expT, ts)
    else:
        return procesarOperacionBinaria(instruccion.expF, ts)


# Funcion procesar_instruccion:
# Recibe una instruccion y la procesa
def procesar_instruccion(input: str, ts: TablaDeSimbolos) -> str:

    # Llamamos a parser con el input ingresado por el usuario
    instruccion = parse(input)
    print(type(instruccion))

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
    elif isinstance(instruccion, ArrayInstruction): return procesarArregloInstruccion(instruccion, ts)
    elif isinstance(instruccion, Boolean): return procesarBoolean(instruccion, ts)
    elif isinstance(instruccion, Conditional): return procesarConditional(instruccion, ts)
    else : print('ERROR: instrucción no válida')

