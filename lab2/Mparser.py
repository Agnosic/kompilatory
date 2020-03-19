#!/usr/bin/python

import scanner
import ply.yacc as yacc


tokens = scanner.tokens

precedence = (
    # ("left", 'IF'),
    # ("left", 'ELSE'),
    ("right", '='),
    ("nonassoc", '<', '>', 'GREATEREQUAL', 'LESSEQUAL', 'EQUAL', 'NOTEQUAL'),
    ("left", '+', '-', 'DOTPLUS', 'DOTMINUS'),
    ("left", '*', '/', 'DOTTIMES', 'DOTDIVIDE'),
    ("right", 'UMINUS'),
    ("left", 'TRANSPOSE')
)


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(
            p.lineno, scanner.find_tok_column(p), p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions_opt"""


def p_instructions_opt_1(p):
    """instructions_opt : instructions """


def p_instructions_opt_2(p):
    """instructions_opt : """


def p_instructions_1(p):
    """instructions : instructions instruction """


def p_instructions_2(p):
    """instructions : instruction """


def p_instruction(p):
    """instruction : assign """


def p_assign(p):
    """ assign : ID maybe_array_range '=' assign
               | ID maybe_array_range '=' assignment ';'
               | ID maybe_array_range PLUSASSIGN assignment ';'
               | ID maybe_array_range MINUSASSIGN assignment ';'
               | ID maybe_array_range TIMESASSIGN assignment ';'
               | ID maybe_array_range DIVIDEASSIGN assignment ';' """


def p_maybe_array_range(p):
    """ maybe_array_range : empty
                    | '[' INTNUM ',' INTNUM ']' """


def p_assignment(p):
    """ assignment : STRING
                   | matrix_special_features
                   | relational_expression
                   | expression 
                   | array """


def p_array(p):
    """ array : '[' ']'
              | '[' dimensions ']' """


def p_dimensions(p):
    """ dimensions : values 
                   | values ';' dimensions """


def p_values(p):
    """ values : value
               | value ',' values """


def p_value(p):
    """ value : STRING
              | number """


def p_relational_expression(p):
    """ relational_expression : expression '<' expression
                              | expression '>' expression 
                              | expression LESSEQUAL expression
                              | expression GREATEREQUAL expression
                              | expression EQUAL expression
                              | expression NOTEQUAL expression """


def p_expression_binary_operation(p):
    """ expression : expression '+' expression
                   | expression '-' expression
                   | expression '*' expression
                   | expression '/' expression
                   | expression DOTPLUS expression
                   | expression DOTMINUS expression
                   | expression DOTTIMES expression
                   | expression DOTDIVIDE expression """


def p_expression(p):
    """ expression : number
                   | ID """


def p_expression_transpose(p):
    """ expression : ID TRANSPOSE """


def p_expression_uminus(p):
    """ expression : '-' expression %prec UMINUS"""


def p_matrix_special_features(p):
    """ matrix_special_features : EYE '(' INTNUM ')'
                                | ZEROS '(' INTNUM ')'
                                | ONES '(' INTNUM ')' """


def p_number(p):
    """ number : INTNUM
               | FLOATNUM """


def p_empty(p):
    'empty :'
    pass


parser = yacc.yacc()
