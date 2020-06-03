import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *
import sys
import numpy as np

sys.setrecursionlimit(10000)


class Interpreter(object):

    def __init__(self):
        self.memoryStack = MemoryStack()
        self.relOp = {
            "==": (lambda x, y: x == y),
            "!=": (lambda x, y: x != y),
            ">": (lambda x, y: x > y),
            ">=": (lambda x, y: x >= y),
            "<": (lambda x, y: x < y),
            "<=": (lambda x, y: x <= y)
        }
        self.binOp = {
            "+": (lambda x, y: x + y),
            "+=": (lambda x, y: x + y),
            "-": (lambda x, y: x - y),
            "-=": (lambda x, y: x - y),
            "*": (lambda x, y: x * y),
            "*=": (lambda x, y: x * y),
            "/": (lambda x, y: x / y),
            "/=": (lambda x, y: x / y),
        }
        self.arrayOp = {
            '+=': (lambda x, y: (np.array(x) + np.array(y)).tolist()),
            '.+': (lambda x, y: (np.array(x) + np.array(y)).tolist()),
            '-=': (lambda x, y: (np.array(x) - np.array(y)).tolist()),
            '.-': (lambda x, y: (np.array(x) - np.array(y)).tolist()),
            '*=': (lambda x, y: np.array(x).dot(np.array(y)).tolist()),
            '.*': (lambda x, y: np.array(x).dot(np.array(y)).tolist()),
            '/=': (lambda x, y: (np.divide(np.array(x), np.array(y))).tolist()),
            './': (lambda x, y: (np.divide(np.array(x), np.array(y))).tolist()),
        }

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
        if node.condition.accept(self):
            return node.instruction.accept(self)

    @when(AST.IfElse)
    def visit(self, node):
        if node.condition.accept(self):
            return node.instruction.accept(self)
        else:
            return node.else_instruction.accept(self)

    @when(AST.Print)
    def visit(self, node):
        print(*node.arguments.accept(self), sep=" ")

    @when(AST.Arguments)
    def visit(self, node):
        return [argument.accept(self) for argument in node.arguments]

    @when(AST.While)
    def visit(self, node):
        while node.condition.accept(self):
            try:
                node.instruction.accept(self)
            except ContinueException:
                pass
            except BreakException:
                break

    @when(AST.For)
    def visit(self, node):
        start, end = node.range.accept(self)

        if self.memoryStack.get(node.variable.name) is not None:
            self.memoryStack.set(node.variable.name, start)
        else:
            self.memoryStack.insert(node.variable.name, start)

        self.memoryStack.push(Memory("local"))

        while self.memoryStack.get(node.variable.name) <= end:
            try:
                node.instruction.accept(self)
            except ContinueException:
                self.memoryStack.set(node.variable.name, self.memoryStack.get(node.variable.name) + 1)
                pass
            except BreakException:
                break

            self.memoryStack.set(node.variable.name, self.memoryStack.get(node.variable.name) + 1)
        self.memoryStack.pop()


    @when(AST.Range)
    def visit(self, node):
        return node.start.accept(self), node.end.accept(self)

    @when(AST.Break)
    def visit(self, node):
        raise BreakException()

    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException()

    @when(AST.Return)
    def visit(self, node):
        raise ReturnValueException(node.assignment.accept(self))

    @when(AST.Assign)
    def visit(self, node):
        right = node.right.accept(self)
        op = node.op
        if op == '=':
            if self.memoryStack.get(node.left.name) is not None:
                self.memoryStack.set(node.left.name, right)
            else:
                self.memoryStack.insert(node.left.name, right)
        elif op in ['+=', '-=', '*=', '/=']:
            value = self.memoryStack.get(node.left.name)
            self.memoryStack.set(node.left.name, self.binOp[op](value, right))

    @when(AST.AssignInArray)
    def visit(self, node):
        right = node.right.accept(self)
        op = node.op
        if op == '=':
            array = self.memoryStack.get(node.left.variable.name)
            if node.left.columns is not None:
                array[node.left.rows.accept(self)][node.left.columns.accept(self)] = right
            else:
                array[node.left.rows.accept(self)] = right;
        elif op in ['+=', '-=', '*=', '/=']:
            if node.left.columns is not None:
                array[node.left.rows.accept(self)][node.left.columns.accept(self)] = self.binOp[op](array[node.left.rows.accept(self)][node.left.columns.accept(self)], right)
            else:
                array[node.left.rows] = self.binOp[op](array[node.left.rows.accept(self)], right)

    @when(AST.Ref)
    def visit(self, node):
        array = self.memoryStack.get(node.variable.name)
        if node.columns is not None:
            return array[node.rows.accept(self)][node.columns.accept(self)]
        else:
            return array[node.rows]


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
        left = node.left.accept(self)
        right = node.right.accept(self)
        return self.relOp[node.op](left, right)

    @when(AST.BinExpr)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if isinstance(left, list) and isinstance(right, list):
            return self.arrayOp[node.op](left, right)
        else:
            return self.binOp[node.op](left, right)

    @when(AST.Transpose)
    def visit(self, node):
        array = self.memoryStack.get(node.variable.name)
        return np.transpose(np.array(array))

    @when(AST.UMinus)
    def visit(self, node):
        assignment = node.assignment.accept(self)
        if isinstance(assignment, list):
            return (np.array(assignment) * -1).tolist()
        else:
            return -assignment


    @when(AST.MatrixSpecial)
    def visit(self, node):
        value = node.value.accept(self)

        if node.name == "zeros":
            return [[0 for col in range(value)] for row in range(value)]
        elif node.name == "ones":
            return [[1 for col in range(value)] for row in range(value)]
        elif node.name == "eye":
            matrix = [[0 for col in range(value)] for row in range(value)]
            for i in range(0, value):
                matrix[i][i] = 1
            return matrix

    @when(AST.IntNum)
    def visit(self, node):
        return int(node.value)

    @when(AST.FloatNum)
    def visit(self, node):
        return float(node.value)

    @when(AST.String)
    def visit(self, node):
        return str(node.value)

    @when(AST.Variable)
    def visit(self, node):
        return self.memoryStack.get(node.name)

