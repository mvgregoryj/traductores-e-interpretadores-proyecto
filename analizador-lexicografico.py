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

# Tokens Identificadores
t_TkId              = r'[a-zA-Z_][a-zA-Z0-9_]*'

# Tokens con regex
# Tokens palabras reservadas
t_TkNum             = r'num'
t_TkBool            = r'bool'
t_TkFalse           = r'false'
t_TkTrue            = r'true'


# Tokens Constantes numéricas
def t_TkNumber(t):
    # r'\d+.*\d*'

    # try:
    #     t.value = float(t.value)
    # except ValueError:
    #     print("Float value too large %d", t.value)
    #     t.value = 0
    r'\d+'
    t.value = int(t.value)    
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

# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Error handler for illegal characters
def t_error(t):
    print(f'ERROR: caracter inválido ({t.value[0]!r}) en la entrada')
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

    print(f'OK: lex("{data}") ==> {arrayTokens}')


while True:
    #data = input("< Stókhos >")
    data = input("<Dacary>")

    arrayTokens = []

    if data == '.':
        break

    elif data.startswith('.lex'):
        
        lextest(lexer, data[4:])

    elif data.startswith('.load'):
        pass

    elif data.startswith('.failed'):
        pass

    elif data.startswith('.reset'):
        pass

    else:
        print("ERROR: interpretación no implementada")