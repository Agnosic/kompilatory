#!/usr/bin/python
class Symbol:
    pass


class VariableSymbol(Symbol):

    def __init__(self, name, type):
        self.name = name
        self.type = type

class SymbolTable(object):

    def __init__(self, parent, name): # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.scope = 0
        self.nesting = 0
        self.symbols = {}
    #

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol
    #

    def get(self, name): # get variable symbol or fundef from <name> entry
        return self.symbols[name]
    #

    def getParentScope(self):
        return self.parent
    #

    def pushScope(self, name):
        self.scope += 1
    #

    def popScope(self):
        self.scope -= 1

    def pushNesting(self):
        self.nesting += 1
    #

    def popNesting(self):
        self.nesting -= 1

