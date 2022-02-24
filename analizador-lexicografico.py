'''
Grupo Dacary: 
                Gregory Muñoz   16-11313
                Daniela Ramirez 16-10940
                Giancarlo Dente 15-10395
'''

import ply.lex as lex
from ply.yacc import yacc

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
    r'\d+.*\d*'
    t.value = float(t.value)
    # except ValueError:
    #     print("Float value too large %d", t.value)
    #     t.value = 0
    #r'\d+'
    #t.value = int(t.value)    
    return t

# Tokens operadores
t_TkOpenPar         = r'\('
t_TkClosePar        = r'\)'
t_TkOpenBracket     = r'\['
t_TkCloseBracket    = r'\]'
t_TkOpenBrace       = r'\{'
t_TkCloseBrace      = r'\}'
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
    #print(f'ERROR: caracter inválido ({t.value[0]!r}) en la entrada')
    arrayErrores.append(f'{t.value[0]!r}')
    t.lexer.skip(1)

# Build the lexer object
lexer = lex.lex()

def lextest (lexer, data):
    # Entrada para el lexer
    lexer.input(data)

    for tok in lexer:

        if (tok.type == 'TkNumber' or tok.type == 'TkId' or tok.type == 'TkBool'):
            arrayTokens.append(f"{tok.type}({tok.value})")

        else:
            arrayTokens.append(f"{tok.type}")

    #print(f'OK: lex("{data}") ==> {arrayTokens}')
    imprimir(data,arrayTokens,arrayErrores)
    
# Funcion para imprimir
def imprimir(data, arrayTokens, arrayErrores):
    
    numErrores = len(arrayErrores)
    if (numErrores > 0):
        #for i in range(0,numErrores):
        print("ERROR: caracter inválido '%s' en la entrada" % arrayErrores) 
    
    else:
        print(f'OK: lex("{data}") ==> {arrayTokens}\n')        
    

# Funcion load
def load (data):
    
    numlinea = 0 
    archivo = open(data, "r")
    cadena = archivo.read()
    archivo.close()
    lexer(cadena)
    numErrores = len(arrayErrores)
    
    for tok in lexer:
        
        if (tok.type == 'TkNumber' or tok.type == 'TkId' or tok.type == 'TkBool'):
            arrayTokens.append(f"{tok.type}({tok.value})")

        else:
            arrayTokens.append(f"{tok.type}")

    if (numErrores > 0):
        tripleta.append(f"")
        
    imprimir(data,arrayTokens,arrayErrores)
        

while True:
    #data = input("< Stókhos >")
    data = input("<Dacary>")

    arrayTokens = []
    arrayErrores = []
    tripleta = []

    if data == '.':
        break

    elif data.startswith('.lex'):
        
        lextest(lexer, data[5:])

    elif data.startswith('.load'):
        
        load(data[5:])

    elif data.startswith('.failed'):
        pass

    elif data.startswith('.reset'):
        pass

    else:
        print("ERROR: interpretación no implementada")