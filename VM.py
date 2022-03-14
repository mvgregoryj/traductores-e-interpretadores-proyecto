'''
Grupo Dacary: 
                Gregory Muñoz   16-11313
                Daniela Ramirez 16-10940
                Giancarlo Dente 15-10395
'''

import ply.lex as lex
from ply.yacc import yacc

# Process
def process (input: str, arrayTuplas: list) -> str:

    if input.startswith('.lex'):        
        return lextest(input)

    elif input.startswith('.load'):
        return load(input, arrayTuplas)

    elif input.startswith('.failed'):
        return failed(arrayTuplas)

    # elif input.startswith('.reset'):
    #     arrayTuplas = reset()

    elif input == "":
        pass

    else:
        print("ERROR: interpretación no implementada")


# Crea
def ejecutarLexer ():
    # Arreglos a usar
    arrayTokens = []
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
    lexer = lex.lex()

    return lexer, arrayTokens, arrayErrores

# Funcion lextest
def lextest (data: str) -> str:

    if data == '.lex':
        data = ""
    elif (data[4] == " "):
        data = data[5:]
    elif (data[4] != " "):
        data = data[4:]

    lexer, arrayTokens, arrayErrores = ejecutarLexer()

    # Entrada para el lexer
    lexer.input(data)

    for tok in lexer:

        if (tok.type == 'TkNumber' or tok.type == 'TkId'):
            arrayTokens.append(f"{tok.type}({tok.value})")
            # arrayTokens.append(tok.type + "(" + tok.value + ")" if type(tok.value)==str else tok.type + "(" + str(tok.value) +")")

        else:
            arrayTokens.append(f"{tok.type}")
           
    return mensajeLexer(data,arrayTokens,arrayErrores)
    
# Funcion mensajeLexer
def mensajeLexer(data: str, arrayTokens: list, arrayErrores: list) -> str:
    
    if (len(arrayErrores) > 0):
        # print(f"ERROR: caracter inválido ({arrayErrores[0]}) en la entrada")
        return f"ERROR: caracter inválido ({arrayErrores[0]}) en la entrada"
    
    else:
        # print(f'OK: lex("{data}") ==> {arrayTokens}') 
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
                mensaje = lextest(data)        
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