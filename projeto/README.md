# Compilador Pascal para EWVM

Compilador de um subconjunto da linguagem Pascal para a máquina virtual EWVM (Educational Web Virtual Machine).

Projeto desenvolvido no âmbito da unidade curricular de **Processamento de Linguagens e Compiladores** da Universidade do Minho.

## Funcionalidades

- Análise léxica e sintática de programas Pascal
- Análise semântica com verificação de tipos
- Geração de código para a EWVM
- Suporte a arrays multidimensionais
- Suporte a funções com parâmetros
- Estruturas de controlo: if/else, while, repeat, for
- Automação web para execução direta no simulador EWVM

## Estrutura do Projeto

```
code/
  lexer_pascal.py      # Analisador léxico
  parserPascal.py      # Analisador sintático
  analiseSemantica.py  # Análise semântica
  codigoMaquina.py     # Geração de código
  main.py              # Ponto de entrada
  erros.py             # Classes de exceções
  webAutomation/       # Automação do browser
```

## Utilização

```bash
cd code
python3 main.py
```

O compilador abre automaticamente o simulador EWVM no browser com o código gerado.

## Requisitos

- Python 3.x
- PLY (Python Lex-Yacc)
- Selenium
- ChromeDriver

## Autores (GRUPO 2)

- Gonçalo Monteiro (a108659)
- Gonçalo Soares (a108393)
- José Pedro (a108395)

---

Universidade do Minho, 2025