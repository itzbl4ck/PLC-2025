import re 
import ply.lex as lex

states = (
    ('inserir_moeda', 'exclusive'),
    ('escolher', 'exclusive')
)

tokens = (
    'LISTAR',
    'MOEDA',
    'SELECIONAR',
    'CODIGO',
    'SAIR',
    'VALOR_EURO',
    'VALOR_CENT',
    'FIM_MOEDA'
)

t_ANY_ignore = ' \t\n'

def t_LISTAR(t):
    r'LISTAR'
    return t

def t_MOEDA(t):
    r'MOEDA'
    t.lexer.begin('inserir_moeda')
    return t

def t_inserir_moeda_VALOR_EURO(t):
    r'\d+e'
    return t

def t_inserir_moeda_VALOR_CENT(t):
    r'\d+c'
    return t

def t_inserir_moeda_FIM_MOEDA(t):
    r'\.'
    t.lexer.begin('INITIAL')
    return t

t_inserir_moeda_ignore = ' \t\n,'

def t_SELECIONAR(t):
    r'SELECIONAR'
    t.lexer.begin('escolher')
    return t

def t_escolher_CODIGO(t):
    r'[A-Z]\d+'
    t.lexer.begin('INITIAL')
    return t

t_escolher_ignore = ' \t\n'

def t_SAIR(t):
    r'SAIR'
    return t

def t_ANY_error(t):
    print(f"Erro: caractere inválido '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()