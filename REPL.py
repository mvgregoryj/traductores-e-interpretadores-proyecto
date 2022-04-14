'''
Grupo Dacary: 
                Gregory Muñoz   16-11313
                Daniela Ramirez 16-10940
                Giancarlo Dente 15-10395
'''

import VM

# Funcion mensajeLexer
def mensajeLexer(data: str, arrayTokens: list, arrayErrores: list) -> str:
    
    if (len(arrayErrores) > 0):
        return f"ERROR: caracter inválido ({arrayErrores[0]}) en la entrada"
    
    else:
        return f'OK: lex("{data}") ==> {arrayTokens}'

# Funcion load
def load (data: str, arrayTuplas: list) -> str:

    mensajeLoad = ""
    
    try: 
        data = data[5:].strip()
        file1 = open(data, "r")
        
    except:
        return f"ERROR: archivo no encontrado." 
        
    Lines = file1.readlines()
    nombreArchivo = data
                
    numline = 0 
    
    for line in Lines:
        numline += 1

        # Ignoramos las lineas en blanco o espacios en blanco o tabulaciones
        if not line.isspace():
            data = line.strip()

            # Archivo contiene .lex en la linea numline
            if data.startswith('.lex'):
                data, arrayTokens, arrayErrores = VM.lexTest(data)
                mensaje = VM.mensajeLexer(data, arrayTokens, arrayErrores)
                mensajeLoad = mensajeLoad + f"{mensaje}\n"

                # Si la respuesta da ERROR se guarda el nombre del archivo, la linea y el mensaje en una lista de tuplas
                if mensaje.startswith('ERROR: ') or mensaje.startswith('Syntax error '):
                    arrayTuplas.append((nombreArchivo, numline, mensaje))

            # Archivo contiene otros nombres de archivos dentro
            elif data.startswith('.load'):
                mensaje = load(data, arrayTuplas)       
                mensajeLoad = mensajeLoad + f"{mensaje}\n"

            # Archivo contiene .failed en la linea numline
            elif data.startswith('.failed'):
                mensajeLoad = mensajeLoad + f"{failed(arrayTuplas)}\n"

            # Archivo contiene .reset en la linea numline
            elif data.startswith('.reset'):
                reset(arrayTuplas)

            # Archivo contiene .ast en la linea numline
            elif data.startswith('.ast'):
                mensaje = VM.testParser(data)
                mensajeLoad = mensajeLoad + f"{mensaje}\n"
            
            # Si no se ingresa alguno de los comandos especificados se devuelve ERROR
            elif not data.startswith('.lex') or not data.startswith('.load') or not data.startswith('.failed') or not data.startswith('.reset') or not data.startswith('.ast'):
                arrayTuplas.append((nombreArchivo, numline, f"ERROR: interpretación no implementada"))
                mensajeLoad = mensajeLoad + f"ERROR: interpretación no implementada\n"

    file1.close()

    return mensajeLoad[:len(mensajeLoad)-1]    # return mensajeLoad[:len(mensajeLoad)-1] para no incluir ultima linea en blanco

# Funcion failed
def failed (arrayTuplas: list) -> str:
    msjFailed = f"[\n"

    if len(arrayTuplas) > 0:
        for i in range(0, len(arrayTuplas)-1):
            msjFailed = msjFailed + f"\t{arrayTuplas[i]},\n"

        msjFailed = msjFailed + f"\t{arrayTuplas[len(arrayTuplas)-1]}\n"
        
    msjFailed = msjFailed + f"]"

    return msjFailed

# Funcion reset
def reset(arrayTuplas):
    for i in range(0, len(arrayTuplas)):
        arrayTuplas.pop()
        
# Variables Globales
arrayTuplas = []

if __name__ == '__main__':

    while True:
        data = input("<Dacary> ").strip()

        if data == '.':
            break

        elif data == "":
           mensajeVM = ""

        elif data.startswith('.lex'):        
            data, arrayTokens, arrayErrores = VM.lexTest(data)
            mensajeVM = mensajeLexer(data, arrayTokens, arrayErrores)

        elif data.startswith('.load'):
            mensajeVM = VM.load(data, arrayTuplas)

        elif data.startswith('.failed'):
            mensajeVM = failed(arrayTuplas)

        elif data.startswith('.reset'):
            reset(arrayTuplas)

        elif data.startswith('.ast'):
            mensajeVM = VM.testParser(data)

        else:
            mensajeVM = VM.process(data)
            
        print(mensajeVM)
