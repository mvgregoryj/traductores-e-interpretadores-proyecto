from enum import Enum

class Expr: pass
 
class BasicType(Expr):
    def __init__(self, type: str):
        self.type = type

    def __repr__(self):
        return f"{self.type}"

class BinOp(Expr):
    def __init__(self, left, op: str, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        if self.op == ',':
            return f"{self.left}{self.op} {self.right}"
        else:
            # return f'{self.left} {self.op} {self.right}'
            return f'({self.left} {self.op} {self.right})'
        # elif self.op == '*':
        #     return f"Mult({self.left},{self.right})"

class Number(Expr):
    def __init__(self, value: int):
        self.type = "num"
        self.value = value

    def __repr__(self):
        return f"{self.value}"
        #return f"Number({self.value})"

# class Boolean(Expr):
#     def __init__(self,str_value,value=None):
#         self.type = "bool"
#         self.str_value = str_value
#         if str_value == "true":
#             self.value = True
#         elif str_value == "false":
#             self.value = False

#     def __repr__(self):
#         return f"{self.str_value}"
#         # return f"{self.value}"
#         #return f"Booleano({self.value})"

class Boolean(Expr):
    def __init__(self, value: bool):
        self.type = "bool"
        self.value = value

    def __repr__(self):
        return f"{self.value}".lower()

class Identifier(Expr):
    def __init__(self, value: str):
        self.type = "id"
        self.value = value

    def __repr__(self):
        return f"{self.value}"
        #return f"Id({self.value})"

class UnaOp(Expr):
    def __init__(self, op: str, right):
        self.op = op
        self.right = right

    def __repr__(self):
        return f"{self.op}{self.right}"

class Grouped(Expr):
    def __init__(self, type: str, left: str, expression, right: str):
        self.type = type
        self.left = left
        self.expression = expression
        self.right = right

    def __repr__(self):
        if self.type == "Par" and (not isinstance(self.expression, BinOp)):
            return f"{self.expression}"
        else:
            return f"{self.left}{self.expression}{self.right}"

class ArrayExpression(Expr):
    def __init__(self, id: Identifier, index: Number):
        self.id = id
        self.index = index

    def __repr__(self):
        return f"{self.id}[{self.index}]"
    
class Function(Expr):
    def __init__(self, id: Identifier, args):
        self.id = id
        self.args = args

    def __repr__(self):
        return f"{self.id}({self.args})"

class Definition(Expr):
    def __init__(self, type: BasicType or Grouped, id: Identifier, expression):
        self.type = type
        self.id = id
        self.expression = expression
    
    def __repr__(self):
        return f"Def({self.type}, {self.id}, {self.expression})"

class Assignment(Expr):
    def __init__(self, id: Identifier, expression):
        self.id = id
        self.expression = expression

    # def asignar(self):
    #     global identificadores
        
    #     if f"{self.id}" in identificadores:
    #         identificadores[f"{self.id}"] = (identificadores[f"{self.id}"][0], self.expression)
    #     else:
    #         print("ERROR: identificador no definido")
    #         # identificadores[f"{self.id}"] = (f"{type(self.expression)}", self.expression)

    def __repr__(self):
        return f"Assign({self.id}, {self.expression})"

################################################

# class TIPO_DATO(Enum):
#     num = 1
#     bool = 2
#     [num] = 3
#     [bool] = 4

class TablaDeSimbolos():
    """
    Tabla de símbolos globales que incluye tanto funciones predefinidas como variables definidas por el usuario.
    """
    def __init__(self, simbolos = {}):
        self.simbolos = simbolos

    def agregar_simbolo(self, simbolo: Definition):
        """
        Agrega un nuevo simbolo a la tabla de simbolos.
        """
        self.simbolos[str(simbolo.id)] = simbolo

    def existe_simbolo_en_ts(self, identificador: Identifier) -> bool:
        id = str(identificador.value)

        if id in self.simbolos:
            return True
        else:
            return False
    
    def obtener_simbolo(self, identificador: Identifier) -> Definition:
        """
        Obtiene un simbolo de la tabla de simbolos.
        """
        id = str(identificador.value)

        if self.existe_simbolo_en_ts(identificador):
            return self.simbolos[id]

        else:
            print ("ERROR: identificador ", id, " no definido")

    def valor_simbolo(self, identificador: Identifier):
        """
        Obtiene el valor de un simbolo de la tabla de simbolos.
        """
        id = str(identificador.value)

        if self.existe_simbolo_en_ts(identificador):
            return (self.simbolos[id]).expression

        else:
            print ("ERROR: identificador ", id, " no definido")

    def actualizar_simbolo(self, simbolo: Assignment):
        """
        Actualiza un simbolo de la tabla de simbolos.
        """
        if not str(simbolo.id) in self.simbolos:
            print ("ERROR: identificador ", str(simbolo.id), " no definido")
        else: 
            self.simbolos[str(simbolo.id)] = Definition(self.simbolos[str(simbolo.id)].type, simbolo.id, simbolo.expression)

    def limpiar_ts(self):
        """
        Limpia la tabla de simbolos.
        """
        self.simbolos = {}
        
        return True

    def __str__(self) -> str:
        return f"{self.simbolos}"
