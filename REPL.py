'''
Grupo Dacary: 
                Gregory Muñoz   16-11313
                Daniela Ramirez 16-10940
                Giancarlo Dente 15-10395
'''

import VM

while True:
    #data = input("< Stókhos >")
    data = input("<Dacary> ")

    # arrayTokens = []
    # arrayErrores = []
    # tripleta = []

    if data == '.':
        break

    else:
        VM.process(data)
    