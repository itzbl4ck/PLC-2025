class VariavelNaoDeclaradaError(Exception):
    def __init__(self, variavel, linha=None):
        self.variavel = variavel
        self.linha = linha
        if linha:
            self.message = f"Erro: Variável '{variavel}' não foi declarada (linha {linha})"
        else:
            self.message = f"Erro: Variável '{variavel}' não foi declarada"
        super().__init__(self.message)

class TipoIncompativelError(Exception):
    def __init__(self, esperado, recebido, variavel=None):
        self.esperado = esperado
        self.recebido = recebido
        self.variavel = variavel
        if variavel:
            self.message = f"Erro: Variável '{variavel}' esperava tipo '{esperado}', mas recebeu '{recebido}'"
        else:
            self.message = f"Erro: Tipo incompatível. Esperado '{esperado}', recebido '{recebido}'"
        super().__init__(self.message)

class FuncaoNaoDeclaradaError(Exception):
    def __init__(self, funcao):
        self.funcao = funcao
        self.message = f"Erro: Função '{funcao}' não foi declarada"
        super().__init__(self.message)


class ExpressaoImpossivel(Exception):
    def __init__(self, variavel, linha=None):
        self.variavel = variavel
        self.linha = linha
        if linha:
            self.message = f"Erro: expressao nao é computada (linha {linha})"
        else:
            self.message = f"Erro: expressao nao é computada"
        super().__init__(self.message)
class TamanhoArrayInvalidoError(Exception):
    def __init__(self, inicio, fim):
        self.inicio = inicio
        self.fim = fim
        self.message = f"Erro: Array inválido. Índice inicial '{inicio}' não pode ser maior que índice final '{fim}'"
        super().__init__(self.message)        


class TamanhoArrayNegativoError(Exception):
    def __init__(self, inicio, fim):
        self.inicio = inicio
        self.fim = fim
        self.message = f"Erro: Array inválido. Índice inicial '{inicio}' e final '{fim}' não podem ser negativos"
        super().__init__(self.message)


class IndexInvalidoError(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        self.message = f"Erro indice do array não é um integer"
        super().__init__(self.message)


class NaoSeiOQueAconteceu(Exception):
    def __init__(self):
        self.message = f"Não é suposto isto acontecer"
        super().__init__(self.message)