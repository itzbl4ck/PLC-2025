import ply.yacc as yacc
from inputs import * 
from lexer_pascal import lexer,tokens,literals

# todo: Codigo singular, corpof
#### !! Umas regras pra fazer a gramatica:

### os tokens estaticos: é tudo minusculo;
### os tokens variaveis (por uma ER): é tudo maiusculo
### os elementos da gramatica: começam por uma maiuscula
### e claro os literals: é entre ''

## isso tudo é pra evitar colisões!

def p_ProgramaI(p):
    r"""
    ProgramaI : PROGRAM Corpo '.'
    """
    p[0] = ["START",p[2]] 
 
def p_Corpo(p): # falta por o CorpoF
    r"""
    Corpo : CorpoF CorpoV CorpoB
    """ 
    p[0] = [["FUNÇOES",p[1]],["VARIAVEIS",p[2]],["CorpoMain",p[3]]]
def p_CorpoF(p):
    r"""
    CorpoF : CorpoF function FUN Argumentos ')' ':' Tipo ';' CorpoV CorpoB ';'
          | CorpoF function FUN ')' ':' Tipo ';' CorpoV CorpoB ';'
          |
    """
    if len(p) == 12:
        p[0] = p[1] + [[p[3],["ARGUMENTOS",p[4]],["VARIAVEIS",p[9]],["CorpoB",p[10]],["TipoRetorno",p[7]]]]
    elif len(p) == 11:
        p[0] = p[1] + [[p[3],["ARGUMENTOS",[]],["VARIAVEIS",p[8]],["CorpoB",p[9]],["TipoRetorno",p[6]]]]
    else:
        p[0] = []

def p_Argumentos(p):
    r"""
    Argumentos : Argumentos ';' VarArg ':' Tipo 
        | VarArg ':' Tipo 
        
    """
    if len(p) == 6:
        p[0] = p[1] + [(p[3],p[5])]
    else:
        p[0] = [(p[1],p[3])]

def p_VarArg(p):
    r"""
    VarArg : VarArg ',' VAR
            | VAR 
    """
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_CorpoV(p):
    r"""
    CorpoV : ListaVar
           | 
    """
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]    

def p_ListaVar(p):
    r"""
    ListaVar : ListaVar Var
             | Var
    """

    if len(p) == 3:
        p[0] = p[1] + p[2]

    else: 
        p[0] = p[1]

def p_Var(p):
    r"""
    Var : var LinesV
    """
    p[0] = p[2]

def p_LinesV(p):
    r"""
     LinesV : LinesV LineV
            | LineV
    """
    
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]
    

def p_LineV(p):
    r"""
        LineV : Ids ':' Tipo ';' 
    """
    p[0] = [(p[1],p[3])]

def p_Ids(p):
    r"""
    Ids : Ids ',' VAR
        | VAR
    """
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_TipoV(p):
    r"""
    TipoV : boolean 
            | integer
            | string
            | real
    """
    p[0] = p[1]

def p_Tipo(p):
    r"""
    Tipo : array '[' ListaA ']' of TipoV
        | TipoV

    """
    if len(p) == 7:
        p[0] = (p[3],p[6],"arr")
    else:
        p[0] = p[1]
        

def p_ListaA(p): ## arrays multidimensionais 
    r"""
    ListaA : ListaA ',' INTEGER doispontos INTEGER
            | INTEGER doispontos INTEGER
    """
    if len(p) == 4:
        p[0] = [(int(p[1]),int(p[3]))]
    else:
        p[0] = p[1] + [(int(p[3]),int(p[5]))]


########## FIM DE VAR  ##########


def p_CorpoB(p):
    r"""
    CorpoB : begin Codigo end
            | begin end
            | begin Codigo ';' end
    """
    if len(p) == 4:
        p[0] = [["BEGIN",p[2]]]
    elif len(p) == 2:
        p[0] = [["BEGIN",[]]]
    else:
        p[0] = [["BEGIN",p[2]]]
    

def p_Codigo(p):
    r"""
    Codigo : Codigo ';' CodigoSingular
            | CodigoSingular
    """
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_CodigoSingular(p):
    r"""
    CodigoSingular : Atribuicao 
                   | CorpoB  
                   | Function_call 
                   | While      
                   | Repeat 
                   | For
                   | If
    """
    p[0] = p[1]
    

def p_Atribuicao(p): 
    r"""
    Atribuicao : VAR atri Expressao_logica
                | VAR '[' IndicesList ']' atri Expressao_logica
    """
    if len(p) == 4:
        p[0] = ["Atrib",p[1],p[3]]
    else:
        p[0] = ["Atrib",(p[1],"arr_var",p[3]),p[6]]

    

 

def p_Expressao(p): 
    r"""
    Expressao : Expressao_logica
    """
    p[0] = p[1]

def p_Expressao_logica(p):
    r"""
    Expressao_logica : Expressao_logica or TermoL
                    | TermoL
    """
    if len(p) == 4:
        p[0] = ["or",p[1],p[3]]
    else:
        p[0] = p[1]


def p_TermoL(p):
    r"""
    TermoL : TermoL and FatorL
            | FatorL
    """
    if len(p) == 4:
        p[0] = ["and",p[1],p[3]]
    else:
        p[0] = p[1]
    

def p_FatorL(p):
    r"""
    FatorL :  CompL
            | Expressao_aritmetica

    """
    p[0] = p[1]

def p_CompL(p):
    r"""
    CompL : Expressao_aritmetica '<' Expressao_aritmetica
        | Expressao_aritmetica '>' Expressao_aritmetica
        | Expressao_aritmetica menorigual Expressao_aritmetica
        | Expressao_aritmetica maiorigual Expressao_aritmetica
        | Expressao_aritmetica '=' Expressao_aritmetica
    """
    p[0] = [p[2],p[1],p[3]]

def p_Expressao_aritmetica(p): 
    r"""
    Expressao_aritmetica : Expressao_aritmetica '+' TermoA 
                        | Expressao_aritmetica '-' TermoA 
                        | TermoA
    """
    if len(p) == 4:
        p[0] = [p[2],p[3],p[1]]
    else:
        p[0] = p[1]

def p_TermoA(p):
    r"""
    TermoA : TermoA shl FatorA
          | TermoA shr FatorA
          | TermoA mod FatorA
          | TermoA div FatorA
          | TermoA '/' FatorA
          | TermoA '*' FatorA
          | FatorA 
    """
    if len(p) == 4:
        p[0] = [p[2],p[1],p[3]]
    else:
        p[0] = p[1]
    

def p_FatorA(p):
    r"""
    FatorA : not ValorA
         | '+' ValorA
         | '-' ValorA
         | ValorA 
    """
    if len(p) == 3:
        p[0] = [p[1],("0","integer"),p[2]]
    
    else:
        p[0] = p[1]

def p_ValorA(p):
    r"""
    ValorA : ValorA_v
        | VAR '[' IndicesList ']'
        | ValorA_i
        | ValorA_b
        | ValorA_r 
        | ValorA_s
        | '(' Expressao_logica ')'
        | ValorA_f
    """
    if len(p) == 5:
        p[0] = (p[1],'arr_var',p[3])  

    elif len(p) == 4:
        p[0] = p[2]
    
    else: 
        p[0] = p[1]

def p_ValorA_v(p):
    r"""
    ValorA_v : VAR
    """
    p[0] = (p[1],"var")

def p_ValorA_i(p):
    r"""
    ValorA_i : INTEGER
    """
    p[0] = (p[1],"integer")

def p_ValorA_b(p):
    r"""
    ValorA_b : BOOL
    """
    p[0] = (p[1],"boolean")

def p_ValorA_s(p):
    r"""
    ValorA_s : STRING
    """
    p[0] = (p[1],"string")

def p_ValorA_f(p):
    r"""
    ValorA_f : Function_call
    """
    p[0] = (p[1],"fun")

def p_ValorA_r(p):
    r"""
    ValorA_r : REAL
    """
    p[0] = (p[1],"real")


    

def p_IndicesList(p): 
    r"""IndicesList : IndicesList ',' Expressao
                    | Expressao"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]
    


def p_Function_call(p): 
    r"""
    Function_call : FUN Args ')' 
                  | FUN ')'
    """
    if len(p) == 4:
        p[0] = ["fun",p[1],p[2]]
    else:
        p[0] = ["fun",p[1],[]] 

def p_Args(p):
    r"""    
    Args : Args ',' Expressao
            | Expressao
    """
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_While(p):
    r"""
    While : while Expressao_logica do CodigoSingular
    """
    p[0] = ["while",parser.jumps,parser.jumps+1,p[2],p[4]]
    parser.jumps += 2

def p_Repeat(p):
    r"""
    Repeat : CorpoRepeat Expressao_logica 
    """
    p[0] = ["repeat",parser.jumps,p[2],p[1]]
    parser.jumps += 1

def p_CorpoRepeat(p):
    r"""
    CorpoRepeat : repeat Codigo until
            | repeat Codigo ';' until
    """
    p[0] = [["BEGIN",p[2]]]
    

def p_For(p):
    r"""
    For : ForTo
          | ForDownto
    """
    p[0] = p[1]
    

def p_ForTo(p):
    r"""
    ForTo : for Atribuicao to Expressao_aritmetica do CodigoSingular
    """
    p[0] = ["forto",parser.jumps,parser.jumps+1, p[2],p[4],p[6]]
    parser.jumps += 2

def p_ForDownto(p):
    r"""
    ForDownto : for Atribuicao downto Expressao_aritmetica do CodigoSingular
    """
    p[0] = ["fordownto",parser.jumps,parser.jumps+1, p[2],p[4],p[6]]
    parser.jumps += 2

def p_If(p):
    r"""    
    If : if Expressao_logica then CodigoSingular
        | if Expressao_logica then CodigoSingular else CodigoSingular
    """
    if len(p) == 5:
        p[0] = ["if",parser.jumps,p[2],p[4]]
        parser.jumps += 1
    else:
        p[0] = ["ifelse",parser.jumps,parser.jumps + 1,p[2],p[4],p[6]]
        parser.jumps += 2


def p_error(p):
    print('Erro sintático: ', p)
    parser.success = False


    
parser = yacc.yacc(debug=True)

#parser.vars = dict()

parser.success = True
parser.vars = dict()
parser.jumps = 0






#parser.parse(input_1)
#parser.parse(input_2)
# parser.parse(input_3)
# parser.parse(input_4)
# parser.parse(input_5)
# print(parser.parse(input_5))
# print("---------")
# print("---------")
