'''
Grupo Dacary: 
                Gregory Muñoz   16-11313
                Daniela Ramirez 16-10940
                Giancarlo Dente 15-10395
'''

from VM import * 

class REPL ():

    def __init__(self, data) -> None:
        self.data = data

    def read_terminal(self, data):
        while True:
            # arrayTokens = []
            # arrayErrores = []
            # tripleta = []

            if data == '.':
                break

            elif data.startswith('.lex'):        
                lectura_lex = lextest(data)

            elif data.startswith('.load'):
                load(data)

            elif data.startswith('.failed'):
                pass

            elif data.startswith('.reset'):
                pass

            else:
                process(data)


######################
if __name__ == "__main__":
    # Leer los parametros
    data = input("<Dacary> ")

    lectura_REPL = REPL.read_terminal(data)
