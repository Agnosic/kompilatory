import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *
import sys

sys.setrecursionlimit(10000)


class Interpreter(object):

    @on('node')
    def visit(self, node):
        pass

    @when(AST.InstructionsOpt)
    def visit(self, node):
        node.instructions.accept(self)

    @when(AST.Instructions)
    def visit(self, node):
        for instruction in node.instructions:
            instruction.accept(self)

    @when(AST.If)
    def visit(self, node):
        pass

    @when(AST.IfElse)
    def visit(self, node):
        pass

    @when(AST.Print)
    def visit(self, node):
        pass

    @when(AST.Arguments)
    def visit(self, node):
        pass

    @when(AST.While)
    def visit(self, node):
        pass

    @when(AST.For)
    def visit(self, node):
        pass

    @when(AST.Range)
    def visit(self, node):
        pass

    @when(AST.Break)
    def visit(self, node):
        pass

    @when(AST.Continue)
    def visit(self, node):
        pass

    @when(AST.Return)
    def visit(self, node):
        pass

    @when(AST.Assign)
    def visit(self):
        pass

    @when(AST.AssignInArray)
    def visit(self, node):
        pass

    @when(AST.Ref)
    def visit(self, node):
        pass

    @when(AST.Array)
    def visit(self, node):
        pass

    @when(AST.Dimensions)
    def visit(self, node):
        pass

    @when(AST.Values)
    def visit(self, node):
        pass

    @when(AST.RelationalExpression)
    def visit(self, node):
        pass

    @when(AST.BinExpr)
    def visit(self, node):
        pass

    @when(AST.Transpose)
    def visit(self, node):
        pass

    @when(AST.UMinus)
    def visit(self, node):
        pass

    @when(AST.MatrixSpecial)
    def visit(self, node):
        pass

    @when(AST.IntNum)
    def visit(self, node):
        pass

    @when(AST.FloatNum)
    def visit(self, node):
        pass

    @when(AST.String)
    def visit(self, node):
        pass

    @when(AST.Variable)
    def visit(self, node):
        pass

    # @when(AST.BinExpr)
    # def visit(self, node):
    #     r1 = node.left.accept(self)
    #     r2 = node.right.accept(self)
    #     # try sth smarter than:
    #     # if(node.op=='+') return r1+r2
    #     # elsif(node.op=='-') ...
    #     # but do not use python eval

    # # simplistic while loop interpretation
    # @when(AST.While)
    # def visit(self, node):
    #     r = None
    #     while node.condition.accept(self):
    #         r = node.instruction.accept(self)
    #     return r
