'''
Grupo Dacary: 
                Gregory Muñoz   16-11313
                Daniela Ramirez 16-10940
                Giancarlo Dente 15-10395
'''

import VM

arrayTuplas = []

while True:
    data = input("<Dacary> ")

    if data == '.':
        break

    elif data.startswith('.lex'):        
        mensaje = VM.lextest(data)

    elif data.startswith('.load'):
        cargo = VM.load(data, arrayTuplas)

    elif data.startswith('.failed'):
        VM.failed(arrayTuplas)

    elif data.startswith('.reset'):
        arrayTuplas = VM.reset()

    else:
        print("ERROR: interpretación no implementada")