import sys
import ply.yacc as yacc
import Mparser
import scanner
from TypeChecker import TypeChecker
from Interpreter import Interpreter

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example1.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()

    ast = parser.parse(text, lexer=scanner.lexer)

    # Below code shows how to use visitor
    # typeChecker = TypeChecker()
    # typeChecker.visit(ast)   # or alternatively ast.accept(typeChecker)

    if not Mparser.error_occurred:
        # typeChecker = TypeChecker()
        # typeChecker.visit(ast)   # or alternatively ast.accept(typeChecker)
        ast.accept(Interpreter())
    else:
        print("Parsing failed!")


