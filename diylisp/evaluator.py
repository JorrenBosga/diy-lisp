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
    if is_symbol(ast):
        splitast = ast.split(' ')
        if splitast[0] == 'define':
            return Environment.extend(env, dict(zip(splitast[1:2], splitast[2::])))
        else:
            return Environment.lookup(env, ast)

    if is_boolean(ast) or is_integer(ast):
        return ast

    if is_list(ast):
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

        # Atoms, quotes and equal
        if ast[0] == 'atom':
            return is_atom(evaluate(ast[1], env))
        if ast[0] == 'quote':
            return ast[1]
        if ast[0] == 'eq':
            return is_atom(evaluate(ast[1], env)) and is_atom(evaluate(ast[2], env)) and evaluate(ast[1], env) == evaluate(ast[2], env)

        # If statement
        if ast[0] == 'if':
            if evaluate(ast[1], env) == True:
                return evaluate(ast[2], env)
            if evaluate(ast[1], env) == False:
                return evaluate(ast[3], env)

        # Functions
        if ast[0] == 'define':
            assert_valid_definition(ast[1:])
            symbol = ast[1]
            value = evaluate(ast[2], env)
            env.set(symbol, value)
            return symbol

        if ast[0] == 'lambda':
            if len(ast) != 3:
                raise LispError("Wrong number of arguments")
            if not is_list(ast[1]):
                raise LispError("Parameters are not in list-form")
            else:
                return Closure(env, ast[1], ast[2])

        if is_closure(ast[0]):
            closure = ast[0]
            arguments = ast[1:]
            if len(arguments) != len(closure.params):
               errormessage = "wrong number of arguments, expected " + str(len(closure.params)) + " got " + str(len(arguments))
               raise LispError(errormessage)
            arguments = [evaluate(a, env) for a in arguments]
            bindings = dict(zip(closure.params, arguments))
            new_env = closure.env.extend(bindings)
            return evaluate(closure.body, new_env)

        if is_list(ast[0]) or is_symbol(ast[0]):
                closure = evaluate(ast[0], env)
                return evaluate([closure] + ast[1:], env)

        else:
            raise LispError("not a function")

    else:
        raise LispError