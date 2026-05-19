from typing import Dict, Any
from Token import Token
from RuntimeError import JLXRuntimeError

class Environment:
    def __init__(self):
        self.values: Dict[str, Any] = {}

    def define(self, name: str, value):
        """Bind a variable name to a value. Note that redefinition is allowed in jerryLox global scope."""
        self.values[name] = value

    def get(self, name: Token):
        """Look up a varible value by its token"""
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        raise JLXRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
    
    def assign(self, name: Token, value: Any):
        """Update value of an existing variable. Assignment is not allowed to crate a *new* variable"""
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return 
        raise JLXRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

