import json
import sys
import tp5 as alex

# Carregar inventário
with open("stock.json","r") as ficheiro:
    inventario = json.load(ficheiro)

credito = 0
maquina_ativa = True

def formatar_saldo(valor_centimos):
    """Converte centimos para formato euros e centimos"""
    euros = valor_centimos // 100
    centimos = valor_centimos % 100
    return f'{euros}e{centimos}c'

def calcular_troco(valor):
    """Calcula o troco em moedas"""
    moedas_disponiveis = [200, 100, 50, 20, 10, 5, 2, 1]
    troco = []

    for moeda in moedas_disponiveis:
        quantidade = valor // moeda
        if quantidade > 0:
            valor -= quantidade * moeda
            if moeda >= 100:
                troco.append(f"{quantidade}x {moeda//100}e")
            else:
                troco.append(f"{quantidade}x {moeda}c")

    return "Pode retirar o troco: " + ", ".join(troco) + "."

def mostrar_produtos():
    """Mostra a listagem de produtos disponíveis"""
    listagem = "maq:\n"
    listagem += "cod  | nome              | quantidade | preço\n"
    listagem += "---------------------------------------------------\n"

    for item in inventario["stock"]:
        listagem += f"{item['cod']}     {item['nome']:<15}   {item['quant']:<10}  {item['preco']}\n"

    listagem += f"\nSaldo = {formatar_saldo(credito)}\n" 
    return listagem

def processar_compra(codigo):
    """Processa a compra de um produto"""
    global credito
    
    for item in inventario["stock"]:
        if item['cod'] == codigo:
            if item['quant'] == 0:
                return "maq: Produto esgotado\n"
            
            preco_centimos = int(item['preco'] * 100)
            if preco_centimos > credito:
                return f"maq: Saldo insuficiente para satisfazer o seu pedido\nSaldo = {formatar_saldo(credito)}; Pedido = {formatar_saldo(preco_centimos)}\n"
            
            credito -= preco_centimos
            item['quant'] -= 1
            return f"maq: Pode retirar o produto dispensado {item['nome']}\nmaq: Saldo = {formatar_saldo(credito)}\n"
    
    return "maq: Produto inexistente\n"

for comando in sys.stdin:
    alex.lexer.input(comando)

    for token in alex.lexer:
        
        if token.type == 'LISTAR':
            print(mostrar_produtos())

        elif token.type == 'VALOR_EURO':
            credito += int(token.value[:-1]) * 100
        
        elif token.type == 'VALOR_CENT':
            credito += int(token.value[:-1])
        
        elif token.type == 'FIM_MOEDA':
            print(f"maq: Saldo = {formatar_saldo(credito)}")

        elif token.type == 'SELECIONAR':
            pass

        elif token.type == 'CODIGO':
            print(processar_compra(token.value))

        elif token.type == 'SAIR':
            print("maq: " + calcular_troco(credito))
            print("maq: Até à próxima!\n")
            maquina_ativa = False
            
    if not maquina_ativa:
        break