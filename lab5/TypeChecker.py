#!/usr/bin/python
from SymbolTable import SymbolTable, VariableSymbol


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    #def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)



class TypeChecker(NodeVisitor):

    def __init__(self):
        self.symbol_table = SymbolTable(None, 'program')

    def visit_InstructionsOpt(self, node):
        self.visit(node.instructions)

    def visit_Instructions(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_If(self, node):
        self.symbol_table.pushScope('if')
        self.visit(node.condition)
        self.visit(node.instruction)
        self.symbol_table.popScope()


    def visit_IfElse(self, node):
        self.symbol_table.pushScope('if')
        self.visit(node.condition)
        self.visit(node.instruction)
        self.symbol_table.popScope()
        self.symbol_table.pushScope('else')
        self.visit(node.else_instruction)
        self.symbol_table.popScope()

    def visit_Print(self, node):
        self.visit(node.arguments)

    def visit_Arguments(self, node):
        for argument in node.arguments:
            self.visit(argument)

    def visit_While(self, node):
        self.symbol_table.pushNesting()
        self.symbol_table.pushScope('while')
        self.visit(node.condition)
        self.visit(node.instruction)
        self.symbol_table.popScope()
        self.symbol_table.popNesting()

    def visit_For(self, node):
        self.symbol_table.pushNesting()
        self.symbol_table.pushScope('for')
        type = self.visit(node.range)
        self.symbol_table.put(node.variable.name, VariableSymbol(node.variable.name, type))
        self.visit(node.instruction)
        self.symbol_table.popScope()
        self.symbol_table.popNesting()

    def visit_Range(self, node):
        type1 = self.visit(node.start)
        type2 = self.visit(node.end)

    def visit_Break(self, node):
        if self.symbol_table.nesting == 0:
            print("Break outside loop")

    def visit_Continue(self, node):
        if self.symbol_table.nesting == 0:
            print("Continue outside loop")

    def visit_Return(self, node):
        self.visit(node.assignment)

    def visit_Assign(self, node):
        type1 = self.visit(node.right)
        op = node.op
        if op == '=':
            self.symbol_table.put(node.left.name, VariableSymbol(node.left.name, type1))
        elif op in ['+=', '-=', '*=', '/=']:
            type2 = self.visit(node.left)
            if type1 != type2:
                print("Incompatible types")

    def visit_AssignInArray(self, node):
        type1 = self.visit(node.right)
        op = node.op
        if op == '=':
            self.symbol_table.put(node.left.name, VariableSymbol(node.left.name, type1))
        elif op in ['+=', '-=', '*=', '/=']:
            type2 = self.visit(node.left)
            if type1 != type2:
                print("Incompatibles types")

    def visit_Ref(self, node):
        pass

    def visit_Array(self, node):
        return self.visit(node.dimensions)

    def visit_Dimensions(self, node):
        sizes = []
        type = ''
        for dimension in node.dimensions:
            sizes.append(len(dimension.values))
            type = self.visit(dimension)
        if len(set(sizes)) != 1:
            print("Vectors in matrix has diffrent sizes")
        return [type , [len(sizes), sizes[0]]]

    def visit_Values(self, node):
        types = []
        for value in node.values:
            types.append(self.visit(value)[0])
        if len(set(types)) != 1:
            print("Vectors must have same types")
        return types[0]

    def visit_RelationalExpression(self, node):
        type1 = self.visit(node.left)     # type1 = node.left.accept(self)
        type2 = self.visit(node.right)    # type2 = node.right.accept(self)
        op    = node.op

    def visit_BinExpr(self, node):
                                          # alternative usage,
                                          # requires definition of accept method in class Node
        type1 = self.visit(node.left)     # type1 = node.left.accept(self)
        type2 = self.visit(node.right)    # type2 = node.right.accept(self)
        op    = node.op
        if isinstance(type1[1], list) != isinstance(type2[1], list):
            print('Cannot do binary expression with normal value and matrix')
        elif op in ['+', '-'] and len(type1) == 2 and type1[1] != type2[1]:
            print('Matrix have diffrent sizes')
        elif op in ['+', '-', '*', '/'] and len(type1) == 1 and type1[0] != type2[0]:
            print('Incompatible types in binary expression')
        # ...
        #

    def visit_Transpose(self, node):
        type = self.visit(node.variable)
        if isinstance(type[1], list):
            print('Cannot transponse seomthing thats not a vector or matrix')

    def visit_UMinus(self, node):
        type1 = self.visit(node.assignment)
        if type1 != 'string':
            return type1
        else:
            print("Bad type for uminus!")

    def visit_MatrixSpecial(self, node):
        type =  self.visit(node.value) ##nie ma potrzeby sprawdzac, poniewaz scanner juz sprawdza typ i ilosc argumentow
        type[1] = [type[1], type[1]]
        return type

    def visit_IntNum(self, node):
        return ['int', node.value]

    def visit_FloatNum(self, node):
        return ['float', node.value]

    def visit_String(self, node):
        return ['string', node.value]

    def visit_Variable(self, node):
        type = self.symbol_table.get(node.name)
        return type.type


