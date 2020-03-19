import ply.lex as lex
import sys

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT'
}

tokens = ['DOTPLUS',       # .+
          'DOTMINUS',      # .-
          'DOTTIMES',      # .*
          'DOTDIVIDE',     # ./
          'PLUSASSIGN',    # +=
          'MINUSASSIGN',   # -=
          'TIMESASSIGN',   # *=
          'DIVIDEASSIGN',  # /=
          'LESSEQUAL',     # <=
          'GREATEREQUAL',  # >=
          'NOTEQUAL',      # !=
          'EQUAL',         # ==
          'TRANSPOSE',
          'ID',
          'INTNUM',
          'FLOATNUM',
          'STRING',
          'COMMENT'
          ] + list(reserved.values())

literals = "+-*/=()[]{}:,;<>"

t_DOTPLUS = r'\.\+'
t_DOTMINUS = r'\.\-'
t_DOTTIMES = r'\.\*'
t_DOTDIVIDE = r'\.\/'
t_PLUSASSIGN = r'\+\='
t_MINUSASSIGN = r'\-\='
t_TIMESASSIGN = r'\*\='
t_DIVIDEASSIGN = r'\/\='
t_LESSEQUAL = r'\<\='
t_GREATEREQUAL = r'\>\='
t_NOTEQUAL = r'\!\='
t_EQUAL = r'\=\='
t_TRANSPOSE = r'\''
t_STRING = r'\"([^\\\n]|(\\.))*?\"'


def t_ID(t):
    r'[_a-zA-Z]\w*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_FLOATNUM(t):
    r'\d+\.\d*'
    t.value = float(t.value)
    return t


def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_COMMENT(t):
    r'\#.*'
    pass


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


t_ignore = '  \t'


def t_error(t):
    print("Illegal character at line %d: '%s'" % (t.lexer.lineno, t.value[0]))
    t.lexer.skip(1)


lexer = lex.lex()
