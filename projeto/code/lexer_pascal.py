import ply.lex as lex

#states = (('comment','exclusive'))


tokens = ["BOOL","INTEGER","REAL","VAR","FUN","STRING", 
          "PROGRAM","var","begin","end","for","to","do","mod","then","while","if",
          "else","or","and","array","downto","integer","boolean","of","function", "COMMENTCHAVETAS", 
          "COMMENTBARRA","COMMENTPARENTISES", "atri","menorigual","maiorigual",
          "xor","shl","shr","not","div", "repeat", "until","string","real","doispontos"]

literals = ["(",")",";",":","=",",","<",">","+","-","/","*","!","%","[","]", "."]

## nota: oq esta a maiusculo dos tokens são variaveis que tem um valor variavel e.g FLOAT pode ser 3.0 ou 8.69

def t_doispontos(t):
    r"\.\."
    return t

def t_COMMENTPARENTISES(t):
    r"\(\*[^\n]*?\*\)"
    pass

def t_COMMENTBARRA(t):
    r"//[^\n]*"
    pass

def t_COMMENTCHAVETAS(t):
    r'\{[^}]*\}'
    pass

def t_PROGRAM(t):  # inicio do programa 
    r"program [^;]+;"  
    return t

def t_xor(t):
    r"xor"
    return t

def t_shr(t):
    r"shr"
    return t

def t_shl(t):
    r"shl"
    return t

def t_not(t):
    r"not"
    return t

def t_div(t):
    r"div"
    return t

def t_var(t): 
    r"var"
    return t

def t_begin(t):
    r"begin"
    return t

def t_end(t):
    r"end"
    return t

def t_for(t):
    r"for"
    return t

def t_downto(t):
    r"downto"
    return t

def t_do(t):
    r"do"
    return t

def t_to(t):
    r"to"
    return t

def t_mod(t):
    r"mod"
    return t

def t_atri(t):
    r":="
    return t

def t_menorigual(t):
    r"<="
    return t

def t_maiorigual(t):
    r">="
    return t

def t_while(t):
    r"while"
    return t

def t_if(t):
    r"if"
    return t

def t_then(t):
    r"then"
    return t

def t_else(t):
    r"else"
    return t

def t_or(t):
    r"or"
    return t

def t_repeat(t):
    r"repeat"
    return t

def t_until(t):
    r"until"
    return t

def t_and(t):
    r"and"
    return t

def t_array(t):
    r"array"
    return t

def t_integer(t):
    r"integer"
    return t

def t_boolean(t):
    r"boolean"
    return t

def t_string(t):
    r"string"
    return t

def t_real(t):
    r"real"
    return t

def t_of(t):
    r"of"
    return t

def t_function(t):
    r"function"
    return t

####### VARIAVEIS QUE VARIAM 

def t_BOOL(t):
    r"true|false"
    return t

def t_REAL(t):
    r"\d+\.\d+"
    return t

def t_INTEGER(t):
    r"\d+"
    return t

def t_STRING(t):
    r"\'[^']+\'"
    return t

def t_FUN(t):
    r"[A-Za-z_-]+\s*\("
    return t 

def t_VAR(t):
    r"[A-Za-z][A-Za-z\_\d]*"
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = '\t '
def t_error(t):
    print('Carácter desconhecido: ', t.value[0], 'Linha: ',t.lexer.lineno)
    t.lexer.skip(1)


lexer = lex.lex()
