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
t_TkNum             = r'num'
t_TkBool            = r'bool'
t_TkFalse           = r'false'
t_TkTrue            = r'true'

# Tokens Identificadores
t_TkId              = r'[a-zA-Z_][a-zA-Z0-9_]*'

# Tokens Constantes numéricas
def t_TkNumber(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
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

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()


# Asociación de operadores y precedencia
precedence = (
    ('left','TkPlus','TkMinus'),
    ('left','TkMult','TkDiv'),
    ('right','TkNot'),
    )

# Definición de la gramática
# def p_instrucciones_lista(t):
#     '''instrucciones    : instruccion instrucciones
#                         | instruccion '''

# def p_instrucciones_evaluar(t):
#     'instruccion : REVALUAR CORIZQ expresion CORDER PTCOMA'
#     print('El valor de la expresión es: ' + str(t[3]))

def p_expresion_binaria(t):
    '''expresion : expresion TkPlus expresion
                  | expresion TkMinus expresion
                  | expresion TkMult expresion
                  | expresion TkDiv expresion'''
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]

# def p_expresion_unaria(t):
#     'expresion : TkNot expresion %prec UMENOS'
#     t[0] = -t[2]

def p_expresion_agrupacion(t):
    'expresion : TkOpenPar expresion TkClosePar'
    t[0] = t[2]

def p_expresion_number(t):
    '''expresion    : TkNumber'''
    t[0] = t[1]

def p_error(t):
    print("Error sintáctico en '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()


f = open("./entrada.txt", "r")
input = f.read()
print(input)
parser.parse(input)