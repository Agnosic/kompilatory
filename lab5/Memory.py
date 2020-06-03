class Memory:

    def __init__(self, name):
      self.table = {}
      self.name = name

    def has_key(self, name):
      return name in self.table

    def get(self, name):
      return self.table[name]         # gets from memory current value of variable <name>

    def put(self, name, value):
      self.table[name] = value  # puts into memory current value of variable <name>


class MemoryStack:

    def __init__(self, memory=Memory("global")):
      self.stack = [] # initialize memory stack with memory <memory>
      self.stack.append(memory)

    def get(self, name):
      for memory in self.stack[::-1]:
        if memory.has_key(name):
          return memory.get(name)          # gets from memory stack current value of variable <name>
      return None

    def insert(self, name, value):
      self.stack[len(self.stack) - 1].put(name, value) # inserts into memory stack variable <name> with value <value>

    def set(self, name, value):
      for memory in self.stack[::-1]:
        if memory.has_key(name):
          return memory.put(name, value)  # sets variable <name> to value <value>

    def push(self, memory):
      self.stack.append(memory) # pushes memory <memory> onto the stack

    def pop(self):
      self.stack.pop()        # pops the top memory from the stack
