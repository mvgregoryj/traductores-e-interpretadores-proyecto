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