## TPC4: Simulador de Máquina de Vending

Implementação de um programa que simula uma máquina de vending (máquina automática de vendas).

### Objetivo

Desenvolver um sistema interativo que permita:
- Listar produtos disponíveis
- Inserir moedas
- Selecionar e comprar produtos
- Devolver troco

### Funcionalidades

#### 1. Gestão de Stock
A máquina mantém um inventário de produtos armazenado em JSON (`stock.json`):
```json
{
    "stock": [
        { "cod": "A1", "nome": "Cafe", "preco": 0.60, "quant": 15 },
        { "cod": "A2", "nome": "Cha", "preco": 0.50, "quant": 12 },
        ...
    ]
}
```

#### 2. Comandos Disponíveis

**LISTAR** - Mostra todos os produtos disponíveis
```
>> LISTAR
maq:
cod  | nome              | quantidade | preço
---------------------------------------------------
A1     Cafe               15          0.6
A2     Cha                12          0.5
...
Saldo = 0e0c
```

**MOEDA** - Insere moedas na máquina
```
>> MOEDA 1e, 20c, 5c, 5c .
maq: Saldo = 1e30c
```
- Formato: `MOEDA <valor1>, <valor2>, ... .`
- Valores aceites: `Ne` (euros) e `Nc` (cêntimos)
- Termina com ponto `.`

**SELECIONAR** - Compra um produto pelo código
```
>> SELECIONAR A1
maq: Pode retirar o produto dispensado Cafe
maq: Saldo = 70c
```

**SAIR** - Termina a sessão e devolve o troco
```
>> SAIR
maq: Pode retirar o troco: 1x 50c, 1x 20c.
maq: Até à próxima!
```

### Estrutura do Projeto

- **tp5.py**: Analisador léxico (tokenizador) usando PLY
  - Define os tokens: LISTAR, MOEDA, SELECIONAR, CODIGO, SAIR, etc.
  - Utiliza estados exclusivos para processar moedas e códigos
  
- **app.py**: Lógica principal da máquina
  - Processa os tokens do analisador léxico
  - Gere o saldo e o inventário
  - Calcula trocos
  
- **stock.json**: Base de dados de produtos
  - Persistência do inventário
  - Atualizado após cada operação

### Exemplo de Interação

```
>> LISTAR
maq:
cod  | nome              | quantidade | preço
---------------------------------------------------
A1     Cafe               15          0.6
...

>> MOEDA 1e, 50c .
maq: Saldo = 1e50c

>> SELECIONAR A1
maq: Pode retirar o produto dispensado Cafe
maq: Saldo = 90c

>> SELECIONAR B1
maq: Saldo insuficiente para satisfazer o seu pedido
Saldo = 90c; Pedido = 1e50c

>> MOEDA 1e .
maq: Saldo = 1e90c

>> SELECIONAR B1
maq: Pode retirar o produto dispensado Sumo
maq: Saldo = 40c

>> SAIR
maq: Pode retirar o troco: 1x 20c, 1x 20c.
maq: Até à próxima!
```

### Tratamento de Erros

- **Produto inexistente**: Avisa quando o código não existe
- **Produto esgotado**: Informa quando a quantidade é 0
- **Saldo insuficiente**: Mostra saldo atual e valor necessário
- **Caracteres inválidos**: Reporta erros de sintaxe

### Execução

```bash
python app.py
```

O programa lê comandos da entrada padrão (stdin) e processa-os sequencialmente até receber o comando `SAIR`.
