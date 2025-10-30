## TPC5: Analisador Sintático de Expressões Aritméticas

Implementação de um analisador sintático (parser) descendente recursivo para expressões aritméticas.

### Objetivo

Desenvolver um parser que:
- Reconheça expressões aritméticas válidas
- Valide a sintaxe segundo uma gramática formal
- Mostre o processo de derivação da expressão

### Gramática

O parser implementa a seguinte gramática livre de contexto:

```
E  → T E'
E' → + T E' | - T E' | ε
T  → F T'
T' → * F T' | / F T' | ε
F  → NUM | ( E )
```

**Onde:**
- `E` = Expressão
- `T` = Termo
- `F` = Fator
- `NUM` = Número inteiro
- `ε` = Produção vazia

### Estrutura do Projeto

#### 1. **tokenizer.py** - Analisador Léxico
Responsável por converter a entrada em tokens:

**Tokens reconhecidos:**
- `NUM`: Números inteiros (`\d+`)
- `PLUS`: Operador de adição (`+`)
- `MINUS`: Operador de subtração (`-`)
- `MUL`: Operador de multiplicação (`*`)
- `DIV`: Operador de divisão (`/`)
- `PA`: Parêntese de abertura (`(`)
- `PF`: Parêntese de fecho (`)`)

**Funcionalidades:**
- Ignora espaços e tabs
- Conta linhas para melhor diagnóstico de erros
- Reporta caracteres desconhecidos

#### 2. **parser.py** - Analisador Sintático
Implementa o parser descendente recursivo:

**Funções principais:**
- `rec_E()`: Reconhece expressões
- `rec_E2()`: Reconhece continuação de expressões (+ ou -)
- `rec_T()`: Reconhece termos
- `rec_T2()`: Reconhece continuação de termos (* ou /)
- `rec_F()`: Reconhece fatores (números ou expressões parentizadas)
- `rec_term(simb)`: Consome um token esperado
- `rec_Parser(data)`: Função principal que inicia a análise

**Características:**
- Mostra o processo de derivação passo a passo
- Reporta erros sintáticos com o token inválido
- Utiliza análise preditiva (LL(1))

#### 3. **main.py** - Programa Principal
Interface de entrada para o utilizador:
- Solicita uma expressão aritmética
- Invoca o parser
- Mostra o resultado da análise

### Exemplos de Utilização

#### Exemplo 1: Expressão Simples
```
$ python main.py
Introduza uma expressão aritmética: 2 + 3
Derivando por: E → T E2
Derivando por: T → F T2
Derivando por: F → NUM
Reconheci: F → NUM
Derivando por: T2 → ε (vazio)
Reconheci: T → F T2
Derivando por: E2 → + T E2
Derivando por: T → F T2
Derivando por: F → NUM
Reconheci: F → NUM
Derivando por: T2 → ε (vazio)
Reconheci: T → F T2
Derivando por: E2 → ε (vazio)
Reconheci: E2 → + T E2
Reconheci: E → T E2
Análise concluída!
```

#### Exemplo 2: Expressão com Parênteses
```
$ python main.py
Introduza uma expressão aritmética: (5 + 3) * 2
Derivando por: E → T E2
Derivando por: T → F T2
Derivando por: F → ( E )
Derivando por: E → T E2
...
Análise concluída!
```

#### Exemplo 3: Expressão Complexa
```
$ python main.py
Introduza uma expressão aritmética: 10 + 20 * 3 - 5 / 2
```

#### Exemplo 4: Erro Sintático
```
$ python main.py
Introduza uma expressão aritmética: 2 + * 3
Derivando por: E → T E2
Derivando por: T → F T2
Derivando por: F → NUM
Reconheci: F → NUM
Derivando por: T2 → ε (vazio)
Reconheci: T → F T2
Derivando por: E2 → + T E2
Derivando por: T → F T2
Erro sintático, token invalido: LexToken(MUL,'*',1,4)
```

### Características da Implementação

**Vantagens:**
- Respeita a precedência de operadores (* e / antes de + e -)
- Suporta expressões parentizadas
- Análise da esquerda para a direita
- Gramática não ambígua

**Limitações:**
- Apenas números inteiros
- Não calcula o resultado (apenas valida sintaxe)
- Não suporta números negativos como literais

### Execução

```bash
python main.py
```

Ou diretamente com o parser:
```python
from parser import rec_Parser

rec_Parser("2 + 3 * 4")
```

### Extensões Possíveis

1. Adicionar cálculo do resultado da expressão
2. Suportar números decimais
3. Adicionar mais operadores (potência, módulo)
4. Implementar uma árvore sintática abstrata (AST)
5. Adicionar funções matemáticas (sin, cos, sqrt, etc.)
