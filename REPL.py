'''
Grupo Dacary: 
                Gregory Muñoz   16-11313
                Daniela Ramirez 16-10940
                Giancarlo Dente 15-10395
'''

import VM

# Variables Globales
arrayTuplas = []


while True:
    data = input("<Dacary> ").strip()

    if data == '.':
        break

    elif data.startswith('.reset'):
        VM.reset(arrayTuplas)

    elif data.startswith('.ast'):
        mensajeParser = VM.testParser(data)

        print(mensajeParser)

    else:
        mensajeVM = VM.process(data, arrayTuplas)
        
        if len(mensajeVM) > 1:
            print(mensajeVM)
