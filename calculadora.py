# -----------------------------------
# |   INTERPRETE MATEMATICO BASICO  |
# -----------------------------------
# |   CALCULADORA BASICA  |
# -------------------------

tokens = (
    'NOMBRE',
    'NUMERO',
    'MAS',
    'MENOS',
    'POR',
    'ENTRE',
    'IGUAL',
    'LPAREN',
    'RPAREN',
    )

# Tokens
t_MAS     = r'\+'
t_MENOS   = r'-'
t_POR     = r'\*'
t_ENTRE   = r'/'
t_IGUAL   = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NOMBRE  = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Caracteres ignorados (Espacio y Tabulaciones)
t_ignore = " \t"

def t_nueva_linea(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Caracter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

# Construye el Analizador Lexico
import ply.lex as lex
lex.lex()

# Reglas de precedencia para los operadores aritméticos
precedence = (
    ('left','MAS','MENOS'),
    ('left','POR','ENTRE'),
    ('right','IGUAL'),
    )

# diccionario de nombres (para almacenar variables)
nombres = { }

def p_statement_asignar(p):
    'statement : NOMBRE IGUAL expression'
    nombres[p[1]] = p[3]

def p_statement_expresiones(p):
    'statement : expression'
    print(p[1])

def p_expression_binop(p):
    '''expression : expression MAS expression
                  | expression MENOS expression
                  | expression POR expression
                  | expression ENTRE expression'''
    if p[2] == '+'  : p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]

def p_expression_menos(p):
    'expression : MENOS expression %prec MENOS'
    p[0] = -p[2]

def p_expression_grupo(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_numero(p):
    'expression : NUMERO'
    p[0] = p[1]

def p_expression_nombre(p):
    'expression : NOMBRE'
    try:
        p[0] = nombres[p[1]]
    except LookupError:
        print("Nombre indefinido '%s'" % p[1])
        p[0] = 0

def p_error(p):
    print("Error de sintaxis en '%s'" % p.value)

import ply.yacc as yacc
yacc.yacc()

while True:
    try:
        s = input("Calculadora Básica 1.0 >>> ")
    except EOFError:
        break
    yacc.parse(s)
