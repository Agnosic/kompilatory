from __future__ import print_function
import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.InstructionsOpt)
    def printTree(self, indent=0):
        if self.instructions:
            self.instructions.printTree()

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        for instruction in self.instructions:
            instruction.printTree(indent)

    @addToClass(AST.If)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end = '')
        print("IF")
        self.condition.printTree(indent+1)
        for i in range(indent):
            print("|  ", end = '')
        print("THEN")
        self.instruction.printTree(indent+1)

    @addToClass(AST.IfElse)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end = '')
        print("IF")
        self.condition.printTree(indent+1)
        for i in range(indent):
            print("|  ", end = '')
        print("THEN")
        self.instruction.printTree(indent+1)
        for i in range(indent):
            print("|  ", end = '')
        print("ELSE")
        self.else_instruction.printTree(indent+1)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end = '')
        print("PRINT")
        self.arguments.printTree(indent + 1)

    @addToClass(AST.Arguments)
    def printTree(self, indent=0):
        for argument in self.arguments:
            argument.printTree(indent)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end = '')
        print("WHILE")
        self.condition.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end = '')
        print("FOR")
        self.variable.printTree(indent + 1)
        self.range.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end = '')
        print("RANGE")
        self.start.printTree(indent + 1)
        self.end.printTree(indent + 1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end = '')
        print("BREAK")

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end = '')
        print("CONTINUE")

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end = '')
        print("RETURN")
        if self.assignment:
            self.assignment.printTree(indent + 1)

    @addToClass(AST.Assign)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end = '')
        print(self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.AssignInArray)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end = '')
        print(self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Ref)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end = '')
        print("REF")
        self.variable.printTree(indent + 1)
        self.rows.printTree(indent + 1)
        if self.columns:
            self.columns.printTree(indent + 1)

    @addToClass(AST.Array)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end = '')
        print("VECTOR")
        if self.dimensions:
            self.dimensions.printTree(indent + 1)

    @addToClass(AST.Dimensions)
    def printTree(self, indent=0):
        for dimension in self.dimensions:
            dimension.printTree(indent)

    @addToClass(AST.Values)
    def printTree(self, indent=0):
        for value in self.values:
            value.printTree(indent)

    @addToClass(AST.RelationalExpression)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end= '')
        print(self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end = '')
        print(self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Transpose)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end = '')
        print("TRANSPOSE")
        self.variable.printTree(indent + 1)

    @addToClass(AST.UMinus)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end = '')
        print("-")
        self.assignment.printTree(indent + 1)

    @addToClass(AST.MatrixSpecial)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end = '')
        print(self.name)
        self.value.printTree(indent+1)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end = '')
        print(self.value)

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end = '')
        print(self.value)

    @addToClass(AST.String)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end = '')
        print(self.value)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|  ", end = '')
        print(self.name)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        raise Exception("UNEXPECTED ERROR")


    # define printTree for other classes
    # ...

