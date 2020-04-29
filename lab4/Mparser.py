#!/usr/bin/python
import scanner
import ply.yacc as yacc
import AST


tokens = scanner.tokens

error_occurred = False

precedence = (
    ("left", 'IFX'),
    ("left", 'ELSE'),
    ("right", '='),
    ("nonassoc", '<', '>', 'GREATEREQUAL', 'LESSEQUAL', 'EQUAL', 'NOTEQUAL'),
    ("left", '+', '-', 'DOTPLUS', 'DOTMINUS'),
    ("left", '*', '/', 'DOTTIMES', 'DOTDIVIDE'),
    ("right", 'UMINUS'),
    ("left", 'TRANSPOSE')
)

def p_program(p):
    """program : instructions_opt"""
    p[0] = p[1]

def p_instructions_opt_1(p):
    """instructions_opt : instructions """
    p[0] = AST.InstructionsOpt(p[1])

def p_instructions_opt_2(p):
    """instructions_opt : """
    p[0] = AST.InstructionsOpt()

def p_instructions_1(p):
    """instructions : instructions instruction """
    p[0] = p[1]
    p[0].append(p[2])

def p_instructions_2(p):
    """instructions : instruction """
    p[0] = AST.Instructions(p[1])

def p_instruction(p):
    """instruction : block 
                   | if 
                   | print
                   | while 
                   | for 
                   | break 
                   | continue
                   | return 
                   | assign
                   | assign_in_array """
    p[0] = p[1]

def p_block(p):
    """ block : '{' instructions '}' """
    p[0] = p[2]

def p_if_1(p):
    """ if : IF '(' assignment ')' instruction %prec IFX """
    p[0] = AST.If(p[3], p[5])

def p_if_2(p):
    """ if : IF '(' assignment ')' instruction ELSE instruction """
    p[0] = AST.IfElse(p[3], p[5], p[7])

def p_print(p):
    """ print : PRINT arguments ';' """
    p[0] = AST.Print(p[2])

def p_arguments_1(p):
    """ arguments : assignment """
    p[0] = AST.Arguments(p[1])

def p_arguments_2(p):
    """ arguments : arguments ',' assignment """
    p[0] = p[1]
    p[0].append(p[3])

def p_while(p):
    """ while : WHILE '(' assignment ')' instruction """
    p[0] = AST.While(p[3], p[5])

def p_for(p):
    """ for : FOR ID '=' range instruction """
    p[0] = AST.For(AST.Variable(p[2]), p[4], p[5])

def p_range(p):
    """ range : expression ':' expression """
    p[0] = AST.Range(p[1], p[3])

def p_break(p):
    """ break : BREAK ';' """
    p[0] = AST.Break()

def p_continue(p):
    """ continue : CONTINUE ';' """
    p[0] = AST.Continue()

def p_return_1(p):
    """ return : RETURN ';' """
    p[0] = AST.Return()

def p_return_2(p):
    """ return : RETURN assignment ';' """
    p[0] = AST.Return(p[2])

def p_assign(p):
    """ assign : ID '=' assignment ';'
               | ID PLUSASSIGN assignment ';'
               | ID MINUSASSIGN assignment ';'
               | ID TIMESASSIGN assignment ';'
               | ID DIVIDEASSIGN assignment ';' """
    p[0] = AST.Assign(p[2], AST.Variable(p[1]), p[3])

def p_assign_in_array(p):
    """ assign_in_array : ref '=' assignment ';'
                        | ref PLUSASSIGN assignment ';'
                        | ref MINUSASSIGN assignment ';'
                        | ref TIMESASSIGN assignment ';'
                        | ref DIVIDEASSIGN assignment ';' """
    p[0] = AST.AssignInArray(p[2], p[1], p[3])

def p_ref_1(p):
    """ ref : ID '[' INTNUM ',' INTNUM ']' """
    p[0] = AST.Ref(AST.Variable(p[1]), AST.IntNum(p[3]), AST.IntNum(p[5]))

def p_ref_2(p):
    """ ref : ID '[' INTNUM ']' """
    p[0] = AST.Ref(AST.Variable(p[1]), AST.IntNum(p[3]))

def p_assignment(p):
    """ assignment : string
                   | matrix_special_features
                   | relational_expression
                   | expression 
                   | array """
    p[0] = p[1]

def p_array_1(p):
    """ array : '[' ']' """
    p[0] = AST.Array()

def p_array_2(p):
    """ array : '[' dimensions ']' """
    p[0] = AST.Array(p[2])

def p_dimensions_1(p):
    """ dimensions : values """
    p[0] = AST.Dimensions(p[1])

def p_dimensions_2(p):
    """ dimensions : dimensions ';' values """
    p[0] = p[1]
    p[0].append(p[3])

def p_values_1(p):
    """ values : value """
    p[0] = AST.Values(p[1])

def p_values_2(p):
    """ values : values ',' value """
    p[0] = p[1]
    p[0].append(p[3])

def p_value(p):
    """ value : string
              | number 
              | array """
    p[0] = p[1]

def p_relational_expression(p):
    """ relational_expression : expression '<' expression
                              | expression '>' expression 
                              | expression LESSEQUAL expression
                              | expression GREATEREQUAL expression
                              | expression EQUAL expression
                              | expression NOTEQUAL expression """
    p[0] = AST.RelationalExpression(p[2], p[1], p[3])

def p_expression_binary_operation(p):
    """ expression : expression '+' expression
                   | expression '-' expression
                   | expression '*' expression
                   | expression '/' expression
                   | expression DOTPLUS expression
                   | expression DOTMINUS expression
                   | expression DOTTIMES expression
                   | expression DOTDIVIDE expression """
    p[0] = AST.BinExpr(p[2], p[1], p[3])

def p_expression(p):
    """ expression : number """
    p[0] = p[1]

def p_expression_id(p):
    """ expression : ID """
    p[0] = AST.Variable(p[1])

def p_expression_transpose(p):
    """ expression : ID TRANSPOSE """
    p[0] = AST.Transpose(AST.Variable(p[1]))

def p_expression_uminus(p):
    """ expression : '-' expression %prec UMINUS """
    p[0] = AST.UMinus(p[2])

def p_expression_ref(p):
    """ expression : ref """
    p[0] = p[1]

def p_matrix_special_features(p):
    """ matrix_special_features : EYE '(' INTNUM ')'
                                | ZEROS '(' INTNUM ')'
                                | ONES '(' INTNUM ')' """
    p[0] = AST.MatrixSpecial(p[1], AST.IntNum(p[3]))

def p_number_int(p):
    """ number : INTNUM """
    p[0] = AST.IntNum(p[1])

def p_number_float(p):
    """ number : FLOATNUM """
    p[0] = AST.FloatNum(p[1])

def p_string(p):
    """ string : STRING """
    p[0] = AST.String(p[1]) 
    

def p_error(p):
    global error_occurred
    error_occurred = True

    if p:
        print("Syntax error at '%s' on line %d" % (p.value, p.lineno))
    else:
        print("Syntax error at EOI")

parser = yacc.yacc()
