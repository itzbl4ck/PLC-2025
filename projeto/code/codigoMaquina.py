from parserPascal import *
from lexer_pascal import *
from analiseSemantica import *
from random import *

def computaFuncao(parsed, dic_args, dic_global):
    res = ""

    dic_locais = criaDicMainVars(parsed, {})   
    dic = dic_locais | dic_args                
    res += criaCodigoMaquinaDic(dic_locais) + "\n"

    res += fazCodigo(getCorpoMain(parsed), dic, dic_global)
    return res

def calculaTamanhoArrayTotal(dimensoes):
    tamanho = 1
    for inicio, fim in dimensoes:
        tamanho *= (fim - inicio + 1)
    return tamanho


def geraCodigoOffsetMultidimensional(indices, dimensoes, dic, dic_global):
    res = ""
    n_dims = len(dimensoes)
    
    # Calcular os tamanhos de cada dimensão
    tamanhos = [(fim - inicio + 1) for inicio, fim in dimensoes]
    
    for i, idx in enumerate(indices):
        # Gerar código para (índice - base)
        res += criaExpressoes(idx, dic, dic_global) + "\n"
        res += f"PUSHI {dimensoes[i][0]}\n"  # base da dimensão i
        res += "SUB\n"
        
        # Multiplicar pelo produto dos tamanhos
        multiplicador = 1
        for j in range(i + 1, n_dims):
            multiplicador *= tamanhos[j]
        
        if multiplicador > 1:
            res += f"PUSHI {multiplicador}\n"
            res += "MUL\n"
        
        if i > 0:
            res += "ADD\n"
    
    return res


def criaCodigoMaquinaDic(dic):
    codigo = ""
    codigo += f"PUSHI {dic['program'][0]}"
    for var in dic.keys():
        if var == "program":
            continue
        match dic[var][0]:
            case 'integer' | 'boolean':
                codigo += f"\nPUSHI {randint(1,2**32-1)} // alocado espaço para a variavel: {var}"
            case 'string':
                codigo += f'\nPUSHS "" // alocado espaço para a variavel: {var}'
            case 'real':
                codigo += f"\nPUSHF {randint(1,2**32-1)} // alocado espaço para a variavel: {var}"
            case 'arr':
                tamanho = calculaTamanhoArrayTotal(dic[var][1])
                codigo += f"\nPUSHN {tamanho} // alocado espaço para o array: {var}"
    return codigo

#print(input)

#print(criaDicMainVars(input))
# dic = criaDicMainVars(input)

#def geraGlobal():


def geraFun(fun,dic_global):
    res = ""
    pos = -1
    dic_global[fun[0]] = ("fun",dict(),fun[-1][1]) # tag dicionario tipo do retorno
    dic_Local = dic_global[fun[0]][1]
    for args, tipo in fun[1][1]:
        for arg in args:
            dic_Local[arg] = (tipo,pos)
            pos += -1
    dic_Local[fun[0][:-1]] = (fun[-1][1],pos)
    
    res += f"{fun[0][:-1]}:" + "\n"
    res += computaFuncao(['START',[[],fun[2],fun[3]]],dic_global[fun[0]][1],dic_global)

    res += "PUSHL 0\n"

    res += "POPN\n"



    res += "RETURN\n"


    return res,dic_global


def geraFuns(funs,dic_global):
    res = ""
    for fun in funs:
        dic_global = geraFun(fun,dic_global)[1]
        res += geraFun(fun,dic_global)[0]
    return res,dic_global



#def fazArrays(linha,dic,dic_global):

# def functionCall(...):


def isCharAccess(expressao, dic, dic_global):
    if isinstance(expressao, tuple) and expressao[1] == "arr_var":
        var = expressao[0]
        if var in dic and dic[var][0] == "string":
            return True
        if var in dic_global and dic_global[var][0] == "string":
            return True
    return False

def isCharLiteral(expressao):
    if isinstance(expressao, tuple) and expressao[1] == "string":
        string = expressao[0].strip("'")
        return len(string) == 1
    return False


def criaExpressoes(expressao, dic, dic_global):    
    if isinstance(expressao,tuple): ## CASO BASE DE UM SO NUMERO E O TIPO

        if expressao[1] == "var":
            if expressao[0] not in dic:
                return f"PUSHG{ dic_global[expressao[0]][1]}" ## VERIFICANDO OS DOIS DICIONARIOS
            else:
                return f"PUSHL {dic[expressao[0]][1]}"


        elif expressao[1] == "arr_var": ## 1. PREPARAR A STACK E O OFFSET PARA DAR LOAD
            res = ""
            var_name = expressao[0]
            # expressao[2] pode ser uma lista de índices (multidimensional) ou uma expressão única
            indices = expressao[2] if isinstance(expressao[2], list) else [expressao[2]]
            
            if var_name in dic:
                if dic[var_name][0] == "string":
                    res += f'PUSHL {dic[var_name][1]}' + "\n"
                    res += criaExpressoes(indices[0], dic, dic_global) + "\n"
                    res += "PUSHI 1\nSUB\n"
                    res += "CHARAT"
                    return res
            else:
                if dic_global[var_name][0] == "string":
                    res += f'PUSHG {dic_global[var_name][1]}' + "\n"
                    res += criaExpressoes(indices[0], dic, dic_global) + "\n"
                    res += "PUSHI 1\nSUB\n"
                    res += "CHARAT"
                    return res

            if var_name in dic:
                var_info = dic[var_name]
                res += "PUSHFP\n"
                res += f"PUSHI {var_info[3]}" + "\n"  # posição base do array
                res += "PADD\n"
                # var_info[1] contém as dimensões [(i1,f1), (i2,f2), ...]
                res += geraCodigoOffsetMultidimensional(indices, var_info[1], dic, dic_global)
            else:
                var_info = dic_global[var_name]
                res += "PUSHGP\n"
                res += f"PUSHI {var_info[3]}" + "\n"  # posição base do array
                res += "PADD\n"
                res += geraCodigoOffsetMultidimensional(indices, var_info[1], dic, dic_global)

            res += "LOADN"
            return res
        

        elif expressao[1] == "boolean":

            if expressao[0] == "true":
                return f"PUSHI 1"
            
            elif expressao[0] == "false":
                return f"PUSHI 0"
            
        elif expressao[1] == "string":
            string = expressao[0].strip("'")  
            return f'PUSHS "{string}"'
        
        elif expressao[1] == "real":
            return f"PUSHF {expressao[0]}"

        elif expressao[1] == "integer":
            return f"PUSHI {expressao[0]}"
        
        elif expressao[1] == "fun": # (['fun', 'Dobro(', [('5', 'integer')]], 'fun')
            return fazFuns(expressao[0],dic,dic_global)
    
    if isinstance(expressao, list):
        if len(expressao) == 1:
            return criaExpressoes(expressao[0], dic,dic_global)
        
        if len(expressao) >= 3:
            op = expressao[0]
            exp1 = expressao[1]
            exp2 = expressao[2]
            
            match op:
                case '+':
                    if verificaExpressoes(exp2, dic, dic_global) == "integer":
                        return f"{criaExpressoes(exp2, dic,dic_global)}\n{criaExpressoes(exp1, dic,dic_global)}\nADD"
                    else:
                        return f"{criaExpressoes(exp2, dic,dic_global)}\n{criaExpressoes(exp1, dic,dic_global)}\nCONCAT"
                case '-':
                    return f"{criaExpressoes(exp2, dic,dic_global)}\n{criaExpressoes(exp1, dic,dic_global)}\nSUB"
                case '*':
                    return f"{criaExpressoes(exp2, dic,dic_global)}\n{criaExpressoes(exp1, dic,dic_global)}\nMUL"
                case '/':
                    return f"{criaExpressoes(exp2, dic,dic_global)}\n{criaExpressoes(exp1, dic,dic_global)}\nDIV"
                
                case 'div':
                    return f"{criaExpressoes(exp1, dic,dic_global)}\n{criaExpressoes(exp2, dic,dic_global)}\nDIV"
                case 'mod':
                    return f"{criaExpressoes(exp1, dic,dic_global)}\n{criaExpressoes(exp2, dic,dic_global)}\nMOD"
                case 'shl':
                    return f"{criaExpressoes(exp2, dic,dic_global)}\n{criaExpressoes(exp1, dic,dic_global)}\nSHL"
                case 'shr':
                    return f"{criaExpressoes(exp2, dic,dic_global)}\n{criaExpressoes(exp1, dic,dic_global)}\nSHR"
                
                case 'and':
                    return f"{criaExpressoes(exp2, dic,dic_global)}\n{criaExpressoes(exp1, dic,dic_global)}\nAND"
                case 'or':
                    return f"{criaExpressoes(exp2, dic,dic_global)}\n{criaExpressoes(exp1, dic,dic_global)}\nOR"
                case 'xor':
                    return f"{criaExpressoes(exp2, dic,dic_global)}\n{criaExpressoes(exp1, dic,dic_global)}\nXOR"
                
                case '<':
                    return f"{criaExpressoes(exp2, dic,dic_global)}i\n{criaExpressoes(exp1, dic,dic_global)}\nSUP"
                case '>':
                    return f"{criaExpressoes(exp2, dic,dic_global)}\n{criaExpressoes(exp1, dic,dic_global)}\nINF"
                case '=':
                    exp1_is_char = isCharAccess(exp1, dic, dic_global) or isCharLiteral(exp1)
                    exp2_is_char = isCharAccess(exp2, dic, dic_global) or isCharLiteral(exp2)
                    
                    if exp1_is_char and exp2_is_char:
                        res = criaExpressoes(exp2, dic, dic_global) + "\n"
                        if isCharLiteral(exp2):
                            res += "CHRCODE\n"
                        res += criaExpressoes(exp1, dic, dic_global) + "\n"
                        if isCharLiteral(exp1):
                            res += "CHRCODE\n"
                        res += "EQUAL"
                        return res
                    else:
                        return f"{criaExpressoes(exp2, dic,dic_global)}\n{criaExpressoes(exp1, dic,dic_global)}\nEQUAL"

                case '<=':
                    return f"{criaExpressoes(exp2, dic,dic_global)}\n{criaExpressoes(exp1, dic,dic_global)}\nSUPEQ"
                case '>=':
                    return f"{criaExpressoes(exp2, dic,dic_global)}\n{criaExpressoes(exp1, dic,dic_global)}\nINFEQ" 
    
    # se entrar aqui é porque o parser falhou
    raise NaoSeiOQueAconteceu()   



#print(criaExpressoes(['+', ('i', 'VAR'), ('1', 'INTEGER')], dic,dic_global))
#print(criaExpressoes((["or",("primo","var"),("primo","var")]),criaDicMainVars(input)))
#print(criaExpressoes(['<', ['*', ('1',"integer"), ['+',('i',"var"),('2',"integer")]], ('2',"integer")], criaDicMainVars(input)))

def fazAtribs(atrib,dic,dic_global): # isto vem neste formato: ['atrib','var','expressao']

    verificaAtribs(atrib,dic,dic_global)

    if isinstance(atrib[1], tuple) and atrib[1][1] == "arr_var":
        var_new = atrib[1][0]
        n = dic[var_new] if var_new in dic else dic_global[var_new]
        # atrib[1][2] pode ser lista de índices (multidimensional) ou expressão única
        indices = atrib[1][2] if isinstance(atrib[1][2], list) else [atrib[1][2]]
        res = ""
        
        if var_new in dic:
            res += "PUSHFP\n"
        else:
            res += "PUSHGP\n"
        
        res += f"PUSHI {n[3]}" + "\n"  # POSIÇÃO BASE DO ARRAY
        res += "PADD\n"
        # Gerar código para calcular o offset multidimensional
        res += geraCodigoOffsetMultidimensional(indices, n[1], dic, dic_global)
        res += criaExpressoes(atrib[2], dic, dic_global) + "\n"  # VALOR QUE VAI GUARDAR
        res += "STOREN\n"
    else:
        var_new = atrib[1]
        n = dic[var_new][1] if var_new in dic else dic_global[var_new][1]
        res = criaExpressoes(atrib[2],dic,dic_global)
        res += f"\nSTOREL {n}"


    
    
    return res


def fazIfs(comando,dic,dic_global):
    res = ""
    label = f"label{comando[1]}"
    
    # da raise
    verificaIfs(comando[2],dic,dic_global) 

    res += criaExpressoes(comando[2],dic,dic_global) + "\n"

    res += f"jz {label}\n"

    
    res += fazCodigo(comando[3],dic,dic_global)

    res += "\n"+ f"{label}: " + "\n"

    return res

def fazIfElse(comando,dic,dic_global):
    res = ""
    labelelse = f"label{comando[1]}"
    labelout = f"label{comando[2]}"

    verificaIfs(comando[3],dic,dic_global)


    res += criaExpressoes(comando[3],dic,dic_global) + "\n"
    res += f"jz {labelelse}" + "\n"
    res += fazCodigo(comando[4],dic,dic_global)
    res += f"JUMP {labelout}" + "\n"
    res +=  "\n"+ f"{labelelse}:" + "\n"
    res += fazCodigo(comando[5],dic,dic_global)
    res += "\n"+ f"{labelout}:"

    
    return res

def fazWhiles(comando,dic,dic_global):
    res = ""

    labeloop = f"label{comando[1]}"
    labelout = f"label{comando[2]}"

    verificaIfs(comando[3],dic,dic_global)

    res += "\n" + f"{labeloop}:" + "\n"
    res += criaExpressoes(comando[3],dic,dic_global) + "\n"
    res += f"jz {labelout}" + "\n"
    
     
    res += fazCodigo(comando[4],dic,dic_global)
    res += f"JUMP {labeloop}" + "\n"
    res += "\n" + f"{labelout}:"
    return res
    
def fazRepeats(comando,dic,dic_global):
    res = ""

    labeloop = f"label{comando[1]}"

    verificaIfs(comando[2],dic,dic_global)

    res += "\n" + f"{labeloop}:" + "\n"
    res += fazCodigo(comando[3],dic,dic_global)
    res += criaExpressoes(comando[2],dic,dic_global) + "\n"
    res += f"jz {labeloop}"

    return res

def fazForsTo(comando,dic,dic_global):
    res = ""
    labeloop = f"label{comando[1]}"
    labelout = f"label{comando[2]}"
    initial_var = comando[3][1]
    res += fazAtribs(comando[3],dic,dic_global) + "\n"
    res += "\n" + f"{labeloop}:" + "\n"
    res += criaExpressoes(comando[4],dic,dic_global) + "\n"
    res += criaExpressoes((initial_var,"var"),dic,dic_global) + "\n"
    res += "SUPEQ\n"
    res += f"jz {labelout}" + "\n"
    res += fazCodigo(comando[5],dic,dic_global)
    
    res += fazAtribs(["atrib",initial_var,['+', (initial_var, 'var'), ('1', 'integer')]],dic,dic_global) + "\n"

    res += f"JUMP {labeloop}" + "\n"
    res += "\n" + f"{labelout}:"

    return res

def fazForsDownto(comando,dic,dic_global):
    res = ""
    
    labeloop = f"label{comando[1]}"
    labelout = f"label{comando[2]}"
    initial_var = comando[3][1]
    verificaIfs(['<',(initial_var,"var"),comando[4]],dic,dic_global)
    res += fazAtribs(comando[3],dic,dic_global) + "\n"
    res += "\n" + f"{labeloop}:" + "\n"
    res += criaExpressoes(comando[4],dic,dic_global) + "\n"
    res += criaExpressoes((initial_var,"var"),dic,dic_global) + "\n" ## Verificaçao da var de atribuiçao
    res += "INFEQ\n"
    res += f"jz {labelout}" + "\n"
    res += fazCodigo(comando[5],dic,dic_global)
    
    res += fazAtribs(["atrib",initial_var,['-', ('1', 'integer') , (initial_var, 'var')]],dic,dic_global) + "\n"

    res += f"JUMP {labeloop}" + "\n"
    res += "\n" + f"{labelout}:"

    return res

def fazFuns(comando,dic_local,dic_global): # (fun,'nome',[args]) # (['fun', 'Dobro(', [('5', 'integer')]], 'fun')
    
    
    if comando[1] == "writeln(" or comando[1] == "Writeln(":
        res = ""
        for arg in comando[2]:
            res += criaExpressoes(arg,dic_local,dic_global) + "\n"
            if verificaExpressoes(arg,dic_local,dic_global) == "string":
                res += "WRITES\n"
            else:
                res += "WRITEI\n"
        return res
    
    elif comando[1] == "readln(":
        res = ""
        if isinstance(comando[2][0], tuple) and comando[2][0][1] == "arr_var":
            var_new = comando[2][0][0]
            n = dic_local[var_new] if var_new in dic_local else dic_global[var_new]
            # comando[2][0][2] pode ser lista de índices (multidimensional) ou expressão única
            indices = comando[2][0][2] if isinstance(comando[2][0][2], list) else [comando[2][0][2]]
            res = ""
            
            if var_new in dic_local:
                res += "PUSHFP\n"
            else:
                res += "PUSHGP\n"
            
            res += f"PUSHI {n[3]}" + "\n"  # POSIÇÃO BASE DO ARRAY
            res += "PADD\n"
            # Gerar código para calcular o offset multidimensional
            res += geraCodigoOffsetMultidimensional(indices, n[1], dic_local, dic_global)
            res += "READ\n"
            var_stored = comando[2][0]
            if not verificaExpressoes(comando[2][0],dic_local,dic_global) == "string":
                res += "ATOI\n"
            res += "STOREN\n"
    


        else:
            var_new = comando[2][0][0]
            n = dic_local[var_new][1] if var_new in dic_local else dic_global[var_new][1]
            res += "READ\n"
            var_stored = comando[2][0]
            if not verificaExpressoes(comando[2][0],dic_local,dic_global) == "string":
                res += "ATOI\n"
            res += f"\nSTOREL {n}\n"

        return res

    elif comando[1] == "length(":
        res = ""
        res += criaExpressoes(comando[2],dic_local,dic_global) + "\n"
        res += "STRLEN"
        return res
    

    n = dic_global[comando[1]]

    res = ""

    res += f"PUSHI 0" + "\n" 

    for arg in comando[2][::-1]:
        # print(arg)
        res += criaExpressoes(arg,dic_local,dic_global) + "\n"

    res += f"pusha {comando[1][:-1]}" + "\n"
    res += "call" + "\n"
    pop_n = len(comando[2])  

    # print(dic_local, "------------", dic_global, "iSSO DA: ", pop_n)
    res += f"pop {pop_n}" # numero de argumentos, e numero de variaveis locais com o program, o -1 é porque é todos menos o retorno


    return res

def getFuncoes(dic_global):
    ret = 0
    for var in dic_global.values():
        if var[0] == "fun":
            ret = ret + 1
    # print(dic_global,ret)
    return ret


def fazCodigo(linhas,dic,dic_global): # esta funçao deveria ir linha por linha gerando codigo resultando num output
    res = ""

    if len(linhas) > 0 and not isinstance(linhas[0],list): ### Caso so tenha so um comando 
        linhas = [linhas]

    for comando in linhas:
        

        # print(comando,  "RESULTADO " ,res) ## print debug util pra ver linha a linha
        
        if comando[0] == "BEGIN" :
            res += fazCodigo(comando[1],dic,dic_global)
        elif comando[0] == "Atrib":
            res += fazAtribs(comando,dic,dic_global) + "\n"
        elif comando[0] == "if":
            res += fazIfs(comando,dic,dic_global) + "\n"
        elif comando[0] == "ifelse":
            res += fazIfElse(comando,dic,dic_global) + "\n"
        elif comando[0] == "while":
            res += fazWhiles(comando,dic,dic_global) + "\n"

        elif comando[0] == "repeat":
            res += fazRepeats(comando,dic,dic_global) + "\n"

        elif comando[0] == "forto":
            res += fazForsTo(comando,dic,dic_global) + "\n"

        elif comando[0] == "fordownto":
            res += fazForsDownto(comando,dic,dic_global) + "\n"
        
        elif comando[0] == "fun":
            res += fazFuns(comando,dic,dic_global) 
            pass
        else:
            res += fazCodigo(comando[0],dic,dic_global)  + "\n"
            
    return res

# print(input_1)
        

# parsed = parser.parse(input_1)


# dic_global = dict()
# dic_global = criaDicMainVars(parsed, dic_global)

# # gerar codigo para as funcoes
# codigo_funs, dic_global = geraFuns(getFuns(parsed), dic_global)  
# dic_local = dict()

# print("---------------")

# print(parsed)

# print("----------------")

# result = "\nSTART:\n" + computaFuncao(parsed, dic_local, dic_global) + "STOP\n\n" + codigo_funs 

# print(result)


