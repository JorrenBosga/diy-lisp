# -*- coding: utf-8 -*-

from types import Environment, LispError, Closure
from ast import is_boolean, is_atom, is_symbol, is_list, is_integer, is_closure
from asserts import assert_exp_length, assert_valid_definition, assert_boolean
from parser import unparse

"""
This is the Evaluator module. The `evaluate` function below is the heart
of your language, and the focus for most of parts 2 through 6.

A score of useful functions is provided for you, as per the above imports, 
making your work a bit easier. (We're supposed to get through this thing 
in a day, after all.)
"""

def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""

    # Simple types
    if is_boolean(ast):
        return ast
    if is_symbol(ast):
        return ast
    if is_integer(ast):
        return ast

    # Atoms, quotes and equal
    if ast[0] == "atom":
        return is_atom(evaluate(ast[1], env))
    if ast[0] == 'quote':
        return evaluate(ast[1], env)
    if ast[0] == 'eq':
        if is_atom(evaluate(ast[1], env)) and is_atom(evaluate(ast[2], env)):
            if evaluate(ast[1], env) == evaluate(ast[2], env):
                return True
            else:
                return False
        else:
            return False

    # Basic arithmetic

    if ast[0] == '+':
        if is_integer(evaluate(ast[1], env)) and is_integer(evaluate(ast[2], env)):
            return evaluate(ast[1], env) + evaluate(ast[2], env)
    if ast[0] == '-':
        if is_integer(evaluate(ast[1], env)) and is_integer(evaluate(ast[2], env)):
            return evaluate(ast[1], env) - evaluate(ast[2], env)
    if ast[0] == '/':
        if is_integer(evaluate(ast[1], env)) and is_integer(evaluate(ast[2], env)):
            return evaluate(ast[1], env) / evaluate(ast[2], env)
    if ast[0] == '*':
        if is_integer(evaluate(ast[1], env)) and is_integer(evaluate(ast[2], env)):
            return evaluate(ast[1], env) * evaluate(ast[2], env)
    if ast[0] == 'mod':
        if is_integer(evaluate(ast[1], env)) and is_integer(evaluate(ast[2], env)):
            return evaluate(ast[1], env) % evaluate(ast[2], env)
    if ast[0] == '>':
        if is_integer(evaluate(ast[1], env)) and is_integer(evaluate(ast[2], env)):
            return evaluate(ast[1], env) > evaluate(ast[2], env)
    if ast[0] == '<':
        if is_integer(evaluate(ast[1], env)) and is_integer(evaluate(ast[2], env)):
            return evaluate(ast[1], env) < evaluate(ast[2], env)


    # If statement
    if ast[0] == 'if':
        if evaluate(ast[1], env) == True:
            return evaluate(ast[2], env)
        if evaluate(ast[1], env) == False:
            return evaluate(ast[3], env)

    else:
        raise LispError