from unittest import TestCase
from VM import *

class VMTest(TestCase):
    def test_lex(self):
        self.assertEqual(lexTest(".lex(2+2)"), ("(2+2)", ["TkOpenPar", "TkNumber(2)", "TkPlus", "TkNumber(2)", "TkClosePar"], []))
    
        self.assertEqual(lexTest(".lex(2*7+1)"), ("(2*7+1)", ["TkOpenPar", "TkNumber(2)", "TkMult", "TkNumber(7)", "TkPlus", "TkNumber(1)", "TkClosePar"], []))       
    
        self.assertEqual(lexTest(".lex num x := 42;"), ("num x := 42;", ["TkNum", "TkId(x)", "TkAssign", "TkNumber(42)", "TkSemicolon"], []))
        
        self.assertEqual(lexTest(".lex"), ("", [], []))
        
        self.assertEqual(lexTest(".lex ! && || * / + - ;"), ("! && || * / + - ;", ['TkNot', 'TkAnd', 'TkOr', 'TkMult', 'TkDiv', 'TkPlus', 'TkMinus', 'TkSemicolon'], []))
        
        #self.assertEqual(lexTest(".lex double malo := @9;"), ("ERROR: caracter inválido ('@') en la entrada", [], []))
    
        self.assertEqual(lexTest(".lex 42 67 * &&|| fibo (20) num"), ("42 67 * &&|| fibo (20) num", ['TkNumber(42)', 'TkNumber(67)', 'TkMult', 'TkAnd', 'TkOr', 'TkId(fibo)', 'TkOpenPar', 'TkNumber(20)', 'TkClosePar', 'TkNum'], []))
    
        self.assertEqual(lexTest(".lex bool verdadero := true"), ("bool verdadero := true", ['TkBool', 'TkId(verdadero)', 'TkAssign', 'TkTrue'], []))
        
        self.assertEqual(lexTest(".lex num pi := 3.141592654"), ("num pi := 3.141592654", ['TkNum', 'TkId(pi)', 'TkAssign', 'TkNumber(3.141592654)'], []))
    
        self.assertEqual(lexTest(".lex verdadero || falso"), ("verdadero || falso", ['TkId(verdadero)', 'TkOr', 'TkId(falso)'], []))
            
        self.assertEqual(lexTest(".lex fact(n) = 1 if n=0 || n=1 else n*fact(n-1);"), ("fact(n) = 1 if n=0 || n=1 else n*fact(n-1);", ['TkId(fact)', 'TkOpenPar', 'TkId(n)', 'TkClosePar', 'TkEQ', 'TkNumber(1)', 'TkId(if)', 'TkId(n)', 'TkEQ', 'TkNumber(0)', 'TkOr', 'TkId(n)', 'TkEQ', 'TkNumber(1)', 'TkId(else)', 'TkId(n)', 'TkMult', 'TkId(fact)', 'TkOpenPar', 'TkId(n)', 'TkMinus', 'TkNumber(1)', 'TkClosePar', 'TkSemicolon'], []))

        self.assertEqual(lexTest(".lex (4<56<=60)"), ("(4<56<=60)", ['TkOpenPar', 'TkNumber(4)', 'TkLT', 'TkNumber(56)', 'TkLE', 'TkNumber(60)', 'TkClosePar'], []))
            
        self.assertEqual(lexTest(".lex (100>=89.5 && 100<559)"), ("(100>=89.5 && 100<559)", ['TkOpenPar', 'TkNumber(100)', 'TkGE', 'TkNumber(89.5)', 'TkAnd', 'TkNumber(100)', 'TkLT', 'TkNumber(559)', 'TkClosePar'], []))
         
        self.assertEqual(lexTest(".lex (100>=89.5 || 10>6)"), ("(100>=89.5 || 10>6)", ['TkOpenPar', 'TkNumber(100)', 'TkGE', 'TkNumber(89.5)', 'TkOr', 'TkNumber(10)', 'TkGT', 'TkNumber(6)', 'TkClosePar'], []))     

        #self.assertEqual(lexTest(".lex double dolares := $$$;"), ("ERROR: caracter inválido ('$') en la entrada", [], []))
         
    def test_ast(self):
        self.assertEqual(testParser(".ast(2+2)"), 'OK: ast("(2+2)") ==> ((2 + 2))')
    
        self.assertEqual(testParser(".ast 5*5"), 'OK: ast("5*5") ==> (5 * 5)')

        self.assertEqual(testParser(".ast num x := 5;"), 'OK: ast("num x := 5;") ==> Def(num, x, 5)')
    
        self.assertEqual(testParser(".ast y := 6;"), 'OK: ast("y := 6;") ==> Assign(y, 6)')
        
        self.assertEqual(testParser(".ast 5*5/(5-(1+1))"), 'OK: ast("5*5/(5-(1+1))") ==> ((5 * 5) / ((5 - ((1 + 1)))))')
        
        self.assertEqual(testParser(".ast x+y*z"), 'OK: ast("x+y*z") ==> (x + (y * z))')
        
        self.assertEqual(testParser(".ast x^y^z"), 'OK: ast("x^y^z") ==> (x ^ (y ^ z))')
        
        self.assertEqual(testParser(".ast (x+y"), 'Syntax error: Unexpected end of input')

        self.assertEqual(testParser(".ast (x*y*("), 'Syntax error: Unexpected end of input')

        self.assertEqual(testParser(".ast arreglo = [1, 2, 3, 4, 5, 9, 4, 0]"), 'OK: ast("arreglo = [1, 2, 3, 4, 5, 9, 4, 0]") ==> (arreglo = [1, 2, 3, 4, 5, 9, 4, 0])')

        self.assertEqual(testParser(".ast [1, 2] = [1, 2]"), 'OK: ast("[1, 2] = [1, 2]") ==> ([1, 2] = [1, 2])')
        
        self.assertEqual(testParser(".ast valor = [ x < y, x < z ]"), 'OK: ast("valor = [ x < y, x < z ]") ==> (valor = [(x < y), (x < z)])')
        
        self.assertEqual(testParser(".ast [num] arreglo := [1, 2, 3, 4, 5, 9, 4, 0]"), 'Syntax error: Unexpected end of input')
  
        self.assertEqual(testParser(".ast ([num] arreglo := [1, 2, 3, 4, 5, 9, 4, 0]);"), 'Syntax error: TkNum(num) at line 1')    

        self.assertEqual(testParser(".ast (arreglo = [1, 2, 3, 4, 5, 9, 4, 0]);"), 'Syntax error: TkSemicolon(;) at line 1') 
        
    def test_comments(self):
        self.assertEqual(process("5*5 #lefsefs"), 'OK: 5*5 #lefsefs ==> 25')
        
    #def test_saltoLinea(self):
    #    self.assertEqual(testParser("\n"), '')   
           
    def test_process(self):
        #self.assertEqual(process("num 'x+y' := 4"), ("OK: num 'x+y' := 4 ==> 4"))
        
        self.assertEqual(process("num (x)"), ("ERROR: instrucción no válida."))
        
        self.assertEqual(process("num valor := 4*12;"), 'ACK: num valor := 48;')
        
        self.assertEqual(process("num var := 5@5;"), 'ERROR: instrucción no válida.')
        
        #self.assertEqual(process("bool it := !g;"), 'ERROR: expresion g no es valida para operaciones unarias.')
        
        self.assertEqual(process("num what:= (5*4)$2;"), 'ERROR: instrucción no válida.')
        
        self.assertEqual(process("num i := 3;"), 'ACK: num i := 3;')
        
        self.assertEqual(process("num g := i;"), 'ACK: num g := 3;')
        
        self.assertEqual(process("g := (3+5);"), 'ACK: g := 8;')
        
        self.assertEqual(process("g := [5*5];"), 'ERROR: tipo de dato de la expresión [(5 * 5)] no coincide con el tipo de dato de g')
        
        self.assertEqual(process("bool cualquier := 5=5;"), 'ACK: bool cualquier := true;')
        
        self.assertEqual(process("bool dani := 52<>43;"), 'ACK: bool dani := true;')
        
        #self.assertEqual(process("num aaaa:= true = 5;"), 'ERROR: no hay coincidencia de tipo entre true y 5')
        
        self.assertEqual(process("num bianchi := +56;"), 'ACK: num bianchi := 56;')
        
        self.assertEqual(process("num sussy := -56;"), 'ACK: num sussy := -56;')
   
        self.assertEqual(process("num t"), 'ERROR: instrucción no válida.')
        
        self.assertEqual(process("i+t"), 'ERROR: identificador t no definido')
        
        self.assertEqual(process("num i := 7;"), 'ERROR: identificador i ya está definido')
        
        self.assertEqual(process("num {x} := 4545345"), 'OK: num {x} := 4545345 ==> 4545345')
        
        self.assertEqual(process("[num] arreglo := [1, 2, 3, 4, 5, 9, 4, 0];"), 'ACK: [num] arreglo := [1, 2, 3, 4, 5, 9, 4, 0];')
            
        self.assertEqual(process("bool value := true;"), ("ACK: bool value := true;"))
        
        self.assertEqual(process("bool poo := !true;"), ("ACK: bool poo := false;"))
        
        self.assertEqual(process("2000 - 802"), ("OK: 2000 - 802 ==> 1198"))
        
        self.assertEqual(process("[num] lista := [3,4,7,1,8];"), 'ACK: [num] lista := [3, 4, 7, 1, 8];')
   
        self.assertEqual(process("bool h := false;"), 'ACK: bool h := false;')
   
        self.assertEqual(process("!h"), 'OK: !h ==> true')
        
        self.assertEqual(process("!!h"), 'OK: !!h ==> false')
        
        self.assertEqual(process("num x := 8;"), 'ACK: num x := 8;')
    
        #self.assertEqual(process("num z := ‘x + y’;"), 'ACK: num z := x + y;') 
        
        #self.assertEqual(process("z"), 'OK: z ==> 15')    
        
        self.assertEqual(process("w := asals;"), 'ERROR: identificador w no definido')
        
        self.assertEqual(process("b := aswewe;"), 'ERROR: identificador b no definido')
        
        self.assertEqual(process("w+b"), 'ERROR: identificador w no definido\nERROR: identificador b no definido')

        self.assertEqual(process("c := 23;"), 'ERROR: identificador c no definido')
        
        self.assertEqual(process("num v := 45;"), 'ACK: num v := 45;')
        
        self.assertEqual(process("c+v"), 'ERROR: identificador c no definido')
        
        self.assertEqual(process("u := 23;"), 'ERROR: identificador u no definido')
        
        self.assertEqual(process("num s := 45;"), 'ACK: num s := 45;')
        
        self.assertEqual(process("s*u"), 'ERROR: identificador u no definido')

        self.assertEqual(process("[bool] booleanos := [true,false,true];"), 'ACK: [bool] booleanos := [true, false, true];') 

        self.assertEqual(process("booleanos"), 'OK: booleanos ==> [true, false, true]')

        self.assertEqual(process("[bool] booleanos2 := [false,true,false];"), 'ACK: [bool] booleanos2 := [false, true, false];') 

        self.assertEqual(process("booleanos2"), 'OK: booleanos2 ==> [false, true, false]')

        self.assertEqual(process("booleanos[0] && booleanos2[0]"), 'OK: booleanos[0] && booleanos2[0] ==> false')

        self.assertEqual(process("booleanos[0] || booleanos2[0]"), 'OK: booleanos[0] || booleanos2[0] ==> true')

        self.assertEqual(process("booleanos[0] && booleanos2[2]"), 'OK: booleanos[0] && booleanos2[2] ==> false')

        self.assertEqual(process("booleanos[0] && booleanos2[1]"), 'OK: booleanos[0] && booleanos2[1] ==> true')    
    
        self.assertEqual(process("booleanos[1] || booleanos2[0]"), 'OK: booleanos[1] || booleanos2[0] ==> false')

        self.assertEqual(process("[num] array:= [1,2,5,10];"), 'ACK: [num] array := [1, 2, 5, 10];')   

        self.assertEqual(process("array"), 'OK: array ==> [1, 2, 5, 10]')    

        self.assertEqual(process("[num] array2:= [5,2,8,1];"), 'ACK: [num] array2 := [5, 2, 8, 1];')   
        
        self.assertEqual(process("array2"), 'OK: array2 ==> [5, 2, 8, 1]')

        self.assertEqual(process("array[0] + array2[0]"), 'OK: array[0] + array2[0] ==> 6')

        self.assertEqual(process("array[0] + array2[3]"), 'OK: array[0] + array2[3] ==> 2')   

        self.assertEqual(process("array[3] * array2[3]"), 'OK: array[3] * array2[3] ==> 10') 
        
        self.assertEqual(process("array[5]"), 'ERROR: indice fuera de rango') 
        
        #self.assertEqual(process("array[o]"), 'ERROR: o no es un numero')
        
        self.assertEqual(process("array[0] + array1[1]"), 'ERROR: variable array1 no definida') 
        
        self.assertEqual(process("array[0] + v[1]"), 'ERROR: 45 no es un arreglo')  

        self.assertEqual(process("q := array[2] * array2[1];"), 'ERROR: identificador q no definido')

        self.assertEqual(process("array[3] - array2[1]"), 'OK: array[3] - array2[1] ==> 8')

        self.assertEqual(process("m:= 956;"), 'ERROR: identificador m no definido')
        
        self.assertEqual(process("num m:= 956;"), 'ACK: num m := 956;')
    
        self.assertEqual(process("num l := 35;"), 'ACK: num l := 35;')
        
        self.assertEqual(process("m"), 'OK: m ==> 956')
       
        self.assertEqual(process("l"), 'OK: l ==> 35')
        
        self.assertEqual(process("m-l"), 'OK: m-l ==> 921')
        
        self.assertEqual(process("m*l"), 'OK: m*l ==> 33460')
        
        self.assertEqual(process("m+l"), 'OK: m+l ==> 991')    
       
        self.assertEqual(process("m^l"), 'OK: m^l ==> 207026638089023476630104801994701520682553810061823759561503427825211695844847616952310042806390332850176')
        
        self.assertEqual(process("m/l"), 'OK: m/l ==> 27')
        
        self.assertEqual(process("m\l"), 'ERROR: instrucción no válida.')
       
        self.assertEqual(process("m<l"), 'OK: m<l ==> false')
        
        self.assertEqual(process("m>l"), 'OK: m>l ==> true')
        
        self.assertEqual(process("m<=l"), 'OK: m<=l ==> false')

        self.assertEqual(process("m>=l"), 'OK: m>=l ==> true')

        self.assertEqual(process("m:= 70;"), 'ACK: m := 70;')

        self.assertEqual(process("m/l"), 'OK: m/l ==> 2')    
    
        self.assertEqual(process("for i in range"), 'ERROR: instrucción no válida.')
        
        self.assertEqual(process("[num] lou := [10];"), 'ACK: [num] lou := [10];')
        
        self.assertEqual(process("[num] tom := [3$3];"), 'ERROR: instrucción no válida.')
        
        self.assertEqual(process("[num] lilo := [lou];"), 'ACK: [num] lilo := [[10]];')
        
        self.assertEqual(process("[bool] zayn := [true];"), 'ACK: [bool] zayn := [true];')
        
        self.assertEqual(process("[bool] ziam := [zayn];"), 'ACK: [bool] ziam := [[true]];')
        
        #self.assertEqual(process("[num] error := [justin];"), 'ERROR: identificador justin no definido')
        
        self.assertEqual(process("[num] arrayError := [?,3,4,5];"), 'ERROR: instrucción no válida.')
        
        self.assertEqual(process("num timmy := 2+4*7*67;"), 'ACK: num timmy := 1878;')
        
        self.assertEqual(process("[num] arregloError := [3**4,5,6];"), 'ERROR: instrucción no válida.')
        
        self.assertEqual(process("[num] arregloError2 := [3,5,6**2];"), 'ERROR: instrucción no válida.')
        
        self.assertEqual(process("[num] arregloError3 := [3,5,45;6];"), 'ERROR: instrucción no válida.')
        
        self.assertEqual(process("floor(453453.2423)"), 'OK: floor(453453.2423) ==> 453453')
        
        self.assertEqual(process("if(2<6,true,false)"), 'OK: if(2<6,true,false) ==> true')
        
        self.assertEqual(process("if(10>4000,true,false)"), 'OK: if(10>4000,true,false) ==> false')
        
        self.assertEqual(process("if(10>4000,5=5,!true)"), 'OK: if(10>4000,5=5,!true) ==> false')
        
        self.assertEqual(process("if(10<4000,5=5,!true)"), 'OK: if(10<4000,5=5,!true) ==> true')
        
        self.assertEqual(process("type(timmy)"), 'OK: type(timmy) ==> num')
        
        self.assertEqual(process("[num] darry := [2,3,4];"), 'ACK: [num] darry := [2, 3, 4];')
        
        self.assertEqual(process("type(darry)"), 'OK: type(darry) ==> [num]')
        
        self.assertEqual(process("type(true)"), 'OK: type(true) ==> bool')
        
        #self.assertEqual(process("type(ziam[0])"), 'OK: type(ziam[0]) ==> [bool]')
        
        self.assertEqual(process("num hola := 8<8;"), 'ERROR: tipo de dato de la expresión (8 < 8) no coincide con el tipo de dato de num')
        
        self.assertEqual(process("ltype(darry)"), 'OK: ltype(darry) ==> [num]')
        
        #self.assertEqual(process("ltype(true)"), 'ERROR: la expresion 'true' no tiene LVALUE')
                         
        self.assertEqual(process("num numero := 4;"), 'ACK: num numero := 4;')                 
        
        #self.assertEqual(process("ltype(numero-3)"), 'ERROR: la expresion '(numero - 3)' no tiene LVALUE')
        
        self.assertEqual(process("length(darry)"), 'OK: length(darry) ==> 3')
        
        self.assertEqual(process("sum(darry)"), 'OK: sum(darry) ==> 9')
        
        self.assertEqual(process("pi()"), 'OK: pi() ==> 3.141592653589793')
        
        self.assertEqual(process("avg(darry)"), 'OK: avg(darry) ==> 3.0')
        
        self.assertEqual(process("reset()"), 'OK: reset() ==> true')
        
        self.assertEqual(process("for()"), 'ERROR: funcion for no definida')
        
        self.assertEqual(process("ln(23323)"), 'OK: ln(23323) ==> 10.057195277130344')
        
        self.assertEqual(process("exp(45)"), 'OK: exp(45) ==> 3.4934271057485095e+19')
        
        self.assertEqual(process("sin(3.14)"), 'OK: sin(3.14) ==> 0.0015926529164868282')
        
        self.assertEqual(process("cos(0.5)"), 'OK: cos(0.5) ==> 0.8775825618903728')
        
        self.assertEqual(process("tan(45)"), 'OK: tan(45) ==> 1.6197751905438615')
        
        self.assertEqual(process("num guacala := (pi()*6)+ln(34)-(sin(3)*4);"), 'ACK: num guacala := 21.81143641391545;')
        
        self.assertEqual(process("[bool] bulian := [true,false,false];"), 'ACK: [bool] bulian := [true, false, false];')
        
        self.assertEqual(process("type(bulian[0])"), 'OK: type(bulian[0]) ==> bool')
        
        self.assertEqual(process("type(bulian)"), 'OK: type(bulian) ==> [bool]')