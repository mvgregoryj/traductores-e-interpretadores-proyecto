from ply.lex import lex
import re
import codecs
import os
import sys

# Tokens
tokens  = [
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
]

reservadas = {
    'num':'num',
    'bool':'bool',
    'false':'false',
    'true':'true'
}

tokens = tokens + list(reservadas.values())

# Caracteres ignorados
t_ignore = '\t'

# Tokens con regex
# Tokens palabras reservadas
# t_TkNum             = r'num'
# t_TkBool            = r'bool'
# t_TkFalse           = r'false'
# t_TkTrue            = r'true'

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
t_TkDiv             = r'/'
t_TkMod             = r'\%'
t_TkPlus            = r'\+'
t_TkMinus           = r'-'
t_TkLT              = r'\<'
t_TkLE              = r'\<='
t_TkGE              = r'\>='
t_TkGT              = r'\>'
t_TkEQ              = r'='
t_TkNE              = r'\<>'
t_TkAnd             = r'\&&'
t_TkOr              = r'\|\|'
t_TkQuote           = r'.'
t_TkComma           = r','
t_TkAssign          = r':='
t_TkSemicolon       = r';'
t_TkColon           = r':'

# Tokens Identificadores
def t_TkId(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.upper() in reservadas:
        t.value = t.value.upper()
        t.type = t.value
    return t

# Tokens Constantes numéricas
def t_TkNumber(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Token error
# def t_TkError(t):
#     print (f"caracter inválido (“{t.value[0]}”) en la entrada")
#     t.lexer.skip(1)

def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)


# Ignorar salto de linea
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

def buscarFicheros(directorio):
    ficheros = []
    numArchivo = ''
    respuesta = False
    cont = 1

    for base, dirs, files in os.walk(directorio):
        ficheros.append(files)

    for file in files:
        print(f" {cont} . {file}")
        cont = cont + 1

    while respuesta == False:
        numArchivo = input('\nNumero del test: ')
        for file in files:
            if file == files[int(numArchivo)-1]:
                respuesta = True
                break
    
    print(f"Has escogido \{files[int(numArchivo)-1]} \n")

    return files[int(numArchivo)-1]


# directorio = '/home/mvgregoryj/Desktop/traductores-e-interpretadores-proyecto/'
# archivo = buscarFicheros(directorio)
# test = directorio+archivo
# fp = codecs.open(test, "r", "utf-8")
# cadena = fp.read()
# fp.close()

cadena = '/home/mvgregoryj/Desktop/traductores-e-interpretadores-proyecto/prueba1.pl0'

analizador = lex()

# analizador.input(cadena)

# while True:
#     tok = analizador.token()
#     if not tok : break
#     print (tok)

while True:
    regex = input("< Stókhos >")
    print(regex)
    analizador.input(regex)

    tok = analizador.token()

    if not tok : break

    for tok in iter(tok, None):
        print( tok.type , tok.value)