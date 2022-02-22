from ply.lex import lex
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
t_TkNum             = r'num'
t_TkBool            = r'bool'
t_TkFalse           = r'false'
t_TkTrue            = r'true'

# Tokens Identificadores
t_TkId              = r'[a-zA-Z_][a-zA-Z0-9_]*'

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
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

# Build the lexer object
lexer = lex()

# --- Parser

# Write functions for each grammar rule which is
# specified in the docstring.
def p_expression(p):
    '''
    expression : term TkPlus term
               | term TkMinus term
    '''
    # p is a sequence that represents rule contents.
    #
    # expression : term TkPlus term
    #   p[0]     : p[1] p[2] p[3]
    # 

    if (p[2] == '+'):
        operator = 'TkPlus'
    elif (p[2] == '-'):
        operator = 'TkMinus'

    p[0] = p[1], operator, p[3]

    # p[0] = ('binop', p[2], p[1], p[3])

def p_expression_term(p):
    '''
    expression : term
    '''
    p[0] = p[1]

def p_term(p):
    '''
    term : factor TkMult factor
         | factor TkDiv factor
    '''
    if (p[2] == '*'):
        operator = 'TkMult'
    elif (p[2] == '/'):
        operator = 'TkDiv'
    elif (p[2] == '%'):
        operator = 'TkMod'
        
    p[0] = p[1], operator, p[3]

    # p[0] = ('binop', p[2], p[1], p[3])

def p_term_factor(p):
    '''
    term : factor
    '''
    p[0] = p[1]

def p_factor_number(p):
    '''
    factor : TkNumber
    '''
    p[0] = f'TkNumber({p[1]})'


    # p[0] = ('number', p[1])

def p_factor_name(p):
    '''
    factor : TkId
    '''
    p[0] = f'TkId("{p[1]}")'

# def p_factor_unary(p):
#     '''
#     factor : TkPlus factor
#            | TkMinus factor
#     '''
#     p[0] = ('unary', p[1], p[2])

def p_factor_grouped(p):
    '''
    factor : TkOpenPar expression TkClosePar
    '''
    p[0] = 'TkOpenPar', p[2], 'TkClosePar'

def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Build the parser
parser = yacc()


# Parse an expression
ast = parser.parse('2 * 3 + 4 * (5 - x)', lexer)
print(ast)