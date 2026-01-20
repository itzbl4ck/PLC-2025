from parserPascal import *
from lexer_pascal import *
from erros import *

input = parser.parse(input_fun)
# print(input)

TIPO = 0
TIPO_ARRAY = 2


def calculaTamanhoArray(dimensoes):
    tamanho_total = 1
    for inicio, fim in dimensoes:
        if inicio < 0 or fim < 0:
            raise TamanhoArrayNegativoError(inicio, fim)
        if fim < inicio:
            raise TamanhoArrayInvalidoError(inicio, fim)
        tamanho_total *= (fim - inicio + 1)
    return tamanho_total


def criaDicMainVars(input,dic_global): ## isto pega o input do parser faz a biblioteca de vars

    ret =  input[1][1] 
    vars = ret[1]
    pos = 1
    for lista, tipo in vars:

        if len(tipo) == 3 and  not isinstance(tipo,str):
            for elem in lista:
                dimensoes = tipo[0]
                tamanho_total = calculaTamanhoArray(dimensoes)
                dic_global[elem] = (tipo[2], tipo[0], tipo[1], pos)
                pos += tamanho_total
        else:
            for elem in lista:
                dic_global[elem] = (tipo, pos)
                pos += 1
    # TOPO DA STACK
    dic_global["program"] = (pos, 0)

    return dic_global


def criaDicLocalVars(input):  
    dic_local = {}
    ret = input[1][1]
    vars = ret[1]
    pos = 1
    for lista, tipo in vars:
        if len(tipo) == 3 and not isinstance(tipo, str):
            for elem in lista:
                dimensoes = tipo[0]
                tamanho_total = calculaTamanhoArray(dimensoes)
                dic_local[elem] = (tipo[2], tipo[0], tipo[1], pos)
                pos += tamanho_total
        else:
            for elem in lista:
                dic_local[elem] = (tipo, pos)
                pos += 1
    return dic_local








def getCorpoMain(input):
    return input[1][2][1]

def getFuns(input):
    return input[1][0][1]




def verificaExpressoes(expressao, dic,dic_global):
    if isinstance(expressao, str):
        return expressao
    
    elif isinstance(expressao,tuple): ## CASO BASE DE UM SO NUMERO E O TIPO

        if expressao[1] == "var":
            if expressao[0] not in dic and expressao[0] not in dic_global:
                raise VariavelNaoDeclaradaError(expressao[0])
 
            return dic[expressao[0]][0] if expressao[0] in dic else dic_global[expressao[0]][0]
        
        elif expressao[1] == "arr_var":

            if expressao[0] not in dic and expressao[0] not in dic_global:
                raise VariavelNaoDeclaradaError(expressao[0])
            
            indices = expressao[2] if isinstance(expressao[2], list) else [expressao[2]]
            for idx in indices:
                if verificaExpressoes(idx, dic, dic_global) != "integer":
                    raise IndexInvalidoError(verificaExpressoes(idx, dic, dic_global))
            
            var_info = dic[expressao[0]] if expressao[0] in dic else dic_global[expressao[0]]
            
            if var_info[0] == "string":
                return var_info[0]

            return var_info[2]  # tipo base do array

        elif expressao[1] == "fun":
            if expressao[0][1] == "length(":
                return "integer"
            if expressao[0][1] not in dic and expressao[0][1] not in dic_global:
                raise VariavelNaoDeclaradaError(expressao[0][1])
            else:
                return dic[expressao[0][1]][-1] if expressao[0][1] in dic else dic_global[expressao[0][1]][-1]
                


        return verificaExpressoes(expressao[1], dic,dic_global)
    
    if isinstance(expressao, list):
        if len(expressao) == 1:
            return verificaExpressoes(expressao[0], dic,dic_global)
        
        if len(expressao) >= 3:
            op = expressao[0]
            exp1 = expressao[1]
            exp2 = expressao[2]
            if op == "+" or op == "-" or op == "*" or op == "div" or op == "mod":
                res1 = verificaExpressoes(exp1, dic,dic_global)
                res2 = verificaExpressoes(exp2, dic,dic_global)
                if op == "+" and res1 == "string" and res2 == "string":
                    return "string"
                
                elif res1 == "integer" and res2 == "integer":
                    return "integer" 
                
                elif (res1 == "real" and res2 == "integer") or (res1 == "integer" and res2 == "real") or (res1 == "real" and res2 == "real") :
                    return "real"

                raise ExpressaoImpossivel(res1,res2)
            
            if op == "and" or op == "or" or op == "xor":
                res1 = verificaExpressoes(exp1, dic,dic_global)
                res2 = verificaExpressoes(exp2, dic,dic_global)

                if res1 == "boolean" and res2 == "boolean":
                    return "boolean" 

                raise ExpressaoImpossivel(res1,res2)
            
            if op == "<" or op == ">" or op == "=" or op == "menorigual" or "maiorigual":
                res1 = verificaExpressoes(exp1, dic,dic_global)
                res2 = verificaExpressoes(exp2, dic,dic_global)

                 
                if res1 == "real" and res2 == "integer" or res1 == "integer" and res2 == "real":
                    return "boolean"
                
                elif res1 == res2:
                    return "boolean"

                raise ExpressaoImpossivel(res1,res2)
    # se entrar aqui é porque o parser falhou
    raise(NaoSeiOQueAconteceu)



#print(verificaExpressoes(['-', ['*', ('1',"integer"), ['+',('i',"var"),('2',"integer")]], ('2',"integer")], criaDicMainVars(input)))


def verificaAtribs(atrib,dic,dic_global): # isto verifica se a atrib faz sentido com o tipo da var e a expressao
    
    if isinstance(atrib[1], tuple) and atrib[1][1] == "arr_var":
        var_new = atrib[1][0]
        if var_new not in dic and var_new not in dic_global:
            raise VariavelNaoDeclaradaError(var_new)
        n = dic[var_new][TIPO_ARRAY] if var_new in dic else dic_global[var_new][TIPO_ARRAY]
        verificaExpressoes(atrib[1],dic,dic_global)
    else:
        var_new = atrib[1]
        if var_new not in dic and var_new not in dic_global:
            raise VariavelNaoDeclaradaError(var_new)
        n = dic[var_new][TIPO] if var_new in dic else dic_global[var_new][TIPO]

    
    res = verificaExpressoes(atrib[2],dic,dic_global)
    if res != n:
        raise TipoIncompativelError(n, res)
    return True
 
def verificaIfs(cond, dic,dic_global):
    # print("AQ A COND",cond)
    tipo = verificaExpressoes(cond,dic,dic_global) 
    if tipo != "boolean":
        raise TipoIncompativelError("boolean", tipo)
    return True
#print(dic,dic_global)
#print(verificaAtribs(['Atrib', 'primo', ('true', 'BOOL')],dic,dic_global))


