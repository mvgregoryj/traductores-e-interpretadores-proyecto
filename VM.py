'''
Grupo Dacary: 
                Gregory Muñoz   16-11313
                Daniela Ramirez 16-10940
                Giancarlo Dente 15-10395
'''

#import ply.lex as lex
from ply.lex import lex
from ply.yacc import yacc

# Process
def process (input: str, arrayTuplas: list) -> str:

    if input.startswith('.lex'):        
        data, arrayTokens, arrayErrores = lexTest(input)
        return mensajeLexer(data, arrayTokens, arrayErrores)


    elif input.startswith('.load'):
        return load(input, arrayTuplas)

    elif input.startswith('.failed'):
        return failed(arrayTuplas)

    # elif input.startswith('.reset'):
    #     arrayTuplas = reset()

    elif input == "":
        return ""

    else:
        return f"ERROR: interpretación no implementada"

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
        'TkColon'
    )

    # Tokens con regex
    # Tokens palabras reservadas
    reservados = {
        'num' : 'TkNum',
        'bool' : 'TkBool',
        'false' : 'TkFalse',
        'true' : 'TkTrue'
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

            # Si no se ingresa alguno de los comandos especificados se devuelve ERROR
            elif not data.startswith('.lex') or not data.startswith('.load') or data.startswith('.failed') or not data.startswith('.reset') :
                arrayTuplas.append((nombreArchivo, numline, f"ERROR: interpretación no implementada"))
                mensajeLoad = mensajeLoad + f"ERROR: interpretación no implementada\n"

    file1.close()

    return mensajeLoad[:len(mensajeLoad)-1]
    #return mensajeLoad

# Funcion failed
def failed (arrayTuplas: list) -> str:
    msjFailed = ""
    msjFailed = msjFailed + f"[\n"

    if len(arrayTuplas) > 0:
        for i in range(0, len(arrayTuplas)-1):
            msjFailed = msjFailed + f"\t{arrayTuplas[i]},\n"

        msjFailed = msjFailed + f"\t{arrayTuplas[len(arrayTuplas)-1]}\n"
        
    msjFailed = msjFailed + f"]"

    return msjFailed

# Funcion reset
def reset():
    return []

class Expr: pass
 
class Definition(Expr):
    def __init__(self, type, id, expression):
        self.type = type
        self.id = id
        self.expression = expression
    
    def __repr__(self):
        return f"Def({self.type}, {self.id}, {self.expression})"
        #return "Def(%r, %r, %r)" % (self.type, self.id, self.expression)

class Assignment(Expr):
    def __init__(self, id, expression):
        self.id = id
        self.expression = expression

    def __repr__(self):
        return f"Assign({self.id}, {self.expression})"
        #return "Assign(%r, %r)" % (self.id, self.expression)

class BasicType(Expr):
    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return f"{self.type}"
        #return "%r" % (self.type)

class BinOp(Expr):
    def __init__(self,left,op,right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        #return "(%r %r %r)" % (self.left, self.op, self.right)
        if self.op == ',':
            return f"{self.left}{self.op} {self.right}"
        else:
            return f"({self.left} {self.op} {self.right})"

class Number(Expr):
    def __init__(self,value):
        self.type = "number"
        self.value = value

    def __repr__(self):
        return f"{self.value}"
        #return "%r" % (self.value)

class Identifier(Expr):
    def __init__(self,value):
        self.type = "id"
        self.value = value

    def __repr__(self):
        return f"{self.value}"
        #return "%r" % (self.value)

class UnaOp(Expr):
    def __init__(self,op,right):
        self.op = op
        self.right = right

    def __repr__(self):
        return f"{self.op}{self.right}"
        #return "%r%r" % (self.op, self.right)

class Grouped(Expr):
    def __init__(self,type,left,expression,right):
        self.type = type
        self.left = left
        self.expression = expression
        self.right = right

    def __repr__(self):
        #return "%r%r%r" % (self.left, self.expression, self.right)
        if self.type == "Par" and self.expression != BinOp:
            return f"{self.expression}"
        else:
            return f"{self.left}{self.expression}{self.right}"

class ArrayInstruction(Expr):
    def __init__(self,id,expression):
        self.id = id
        self.expression = expression

    def __repr__(self):
        return f"{self.id}[{self.expression}]"
        #return "%r[%r]" % (self.id, self.expression)
       

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
    # dictionary of names
    identificadores = { }

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
                          | expresionLogica TkAnd expresionLogica
                          | expresionLogica TkOr expresionLogica   
        '''
        if len(p) == 2:
            p[0] = p[1]

        elif len(p) == 3:
            p[0] = UnaOp(p[1], p[2])

        elif len(p) == 4:
            p[0] = BinOp(p[1], p[2], p[3])
    
    def p_booleano(p):
        '''
        booleano : TkTrue
                   | TkFalse
        '''
        p[0] = p[1]
    
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