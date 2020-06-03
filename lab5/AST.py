class Node(object):
    def accept(self, visitor):
        return visitor.visit(self)

class InstructionsOpt(Node):
    def __init__(self, instructions=None):
        self.instructions = instructions

    def accept(self, visitor):
        visitor.visit(self)

class Instructions(Node):
    def __init__(self, instruction):
      self.instructions = [instruction]

    def append(self, instruction):
      self.instructions.append(instruction)

    def accept(self, visitor):
        visitor.visit(self)

class If(Node):
    def __init__(self, condition, instruction):
      self.condition = condition
      self.instruction = instruction

class IfElse(Node):
    def __init__(self, condition, instruction, else_instruction):
      self.condition = condition
      self.instruction = instruction
      self.else_instruction = else_instruction

class Print(Node):
    def __init__(self, arguments):
      self.arguments = arguments

class Arguments(Node):
    def __init__(self, argument):
      self.arguments = [argument]

    def append(self, argument):
      self.arguments.append(argument)

class While(Node):
    def __init__(self, condition, instruction):
      self.condition = condition
      self.instruction = instruction

class For(Node):
    def __init__(self, variable, range, instruction):
      self.variable = variable
      self.range = range
      self.instruction = instruction

class Range(Node):
    def __init__(self, start, end):
      self.start = start
      self.end = end

class Break(Node):
    def __init__(self):
      pass

class Continue(Node):
    def __init__(self):
      pass

class Return(Node):
    def __init__(self, assignment=None):
      self.assignment = assignment

class Assign(Node):
  def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class AssignInArray(Node):
  def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class Ref(Node):
  def __init__(self, variable, rows, columns=None):
        self.variable = variable
        self.rows = rows
        self.columns = columns

class Array(Node):
  def __init__(self, dimensions=None):
        self.dimensions = dimensions

class Dimensions(Node):
    def __init__(self, dimension):
      self.dimensions = [dimension]

    def append(self, dimension):
      self.dimensions.append(dimension)

class Values(Node):
    def __init__(self, value):
      self.values = [value]

    def append(self, value):
      self.values.append(value)

class RelationalExpression(Node):
  def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class Transpose(Node):
    def __init__(self, variable):
        self.variable = variable

class UMinus(Node):
    def __init__(self, assignment):
        self.assignment = assignment

class MatrixSpecial(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        self.value = value

class String(Node):
    def __init__(self, value):
        self.value = value

class Variable(Node):
    def __init__(self, name):
        self.name = name


# ...
# fill out missing classes
# ...

class Error(Node):
    def __init__(self):
        pass
