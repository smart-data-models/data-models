"""
originally from : https://gist.githubusercontent.com/dsuess/1a5919b598f54d24010eb0a7a79e71a0/raw/ea1643b8c320ac647f7dfd6c645f8502a2c60730/create_function.py
fork : https://gist.githubusercontent.com/whoopsjohnnie/5e0c7e7e263bf95a3145a003b6fc47e8/raw/37ebff8af4b276421e45a58b6389c31a237be378/create_function.py
"""
from __future__ import print_function

"""
Python is a dynamic language, and it is relatively easy to dynamically create
and modify things such as classes and objects. Functions, however, are quite
challenging to create dynamically.
One area where we might want to do this is in an RPC library, where a function
defined on a server needs to be available remotely on a client.
The naive solution is to simply pass arguments to a generic function that
accepts `*args` and `**kwargs`. A lot of information is lost with this approach,
however, in particular the number of arguments taken. Used in an RPC
implementation, this also delays any error feedback until after the arguments
have reached the server.
If you search online, most practical solutions involve `exec()`. This is
generally the approach chosen by many Python RPC libraries. This is, of course,
a very insecure solution, one that opens any program up to malicious code
execution.
This experiment creates a real function at the highest layer available: the AST.
There are several challenges to this approach. The most significant is that on
the AST layer, function arguments must be defined according to their type. This
greatly limits the flexibility allowed when defining a function with Python
syntax.
This experiment has a few requirements that introduce (and relieve) additional
 challenges:
- Must return a representative function signature to the Python interpreter
- Must support both Python 2 and 3
- Must allow serialization to JSON and/or MsgPack

Taken from https://gist.github.com/dhagrow/d3414e3c6ae25dfa606238355aea2ca5
"""


import ast
import types
import numbers
import collections
import sys
from typing import Callable
from inspect import signature


def get_function_signature(f: Callable) -> signature:
    """Gets the functions arguments signature

    Args:
        f (Callable): the function to inspect for argument signatures

    Returns:
        signature: signature of function
    """
    return signature(f)


def create_function(name, signature, callback):
    """Dynamically creates a function that wraps a call to *callback*, based
    on the provided *signature*.
    """
    # utils to set default values when creating a ast objects
    Loc = lambda cls, **kw: cls(annotation=None, lineno=1, col_offset=0, **kw)
    Name = lambda id, ctx=None: Loc(ast.Name, id=id, ctx=ctx or ast.Load())

    # vars for the callback call
    call_args = []
    call_keywords = []

    # vars for the generated function signature
    func_args = []
    func_posonlyargs = []
    func_kwargs = []
    func_defaults = []
    func_kwdefaults = []
    vararg = None
    kwarg = None

    # vars for the args with default values
    defaults = []
    kwdefaults = dict()

    # assign args based on *signature*
    for param in viewvalues(signature.parameters):
        if param.default is not param.empty:
            if param.kind in {param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD}:
                add_to = func_defaults
                defaults.append(param.default)
            elif param.kind is param.KEYWORD_ONLY:
                add_to = func_kwdefaults
                kwdefaults[param.name] = param.default
            else:
                raise TypeError("Shouldnt have defaults for other types")

            if isinstance(param.default, type(None)):
                # `ast.NameConstant` is used in PY3, but both support `ast.Name`
                # add_to.append(Name("None"))
                add_to.append(Loc(ast.Constant, value=None))
            elif isinstance(param.default, bool):
                # `ast.NameConstant` is used in PY3, but both support `ast.Name`
                add_to.append(Name(str(param.default)))
            elif isinstance(param.default, numbers.Number):
                add_to.append(Loc(ast.Num, n=param.default))
            elif isinstance(param.default, str):
                add_to.append(Loc(ast.Str, s=param.default))
            elif isinstance(param.default, bytes):
                add_to.append(Loc(ast.Bytes, s=param.default))
            elif isinstance(param.default, list):
                add_to.append(Loc(ast.List, elts=param.default, ctx=ast.Load()))
            elif isinstance(param.default, tuple):
                add_to.append(Loc(ast.Tuple, elts=list(param.default), ctx=ast.Load()))
            elif isinstance(param.default, dict):
                add_to.append(
                    Loc(
                        ast.Dict,
                        keys=list(viewkeys(param.default)),
                        values=list(viewvalues(param.default)),
                    )
                )
            else:
                err = "unsupported default argument type: {}"
                raise TypeError(err.format(type(param.default)))
                # return ast.Constant(None)
                # add_to.append(Loc(ast.Constant(None), s=param.default))
        elif param.kind is param.KEYWORD_ONLY:
            # If it's a keyword-only arugment, we need to add a None-default
            # value
            func_kwdefaults.append(None)

        if param.kind in {param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD}:
            call_args.append(Name(param.name))
            func_args.append(Loc(ast.arg, arg=param.name))
        elif param.kind == param.VAR_POSITIONAL:
            call_args.append(Loc(ast.Starred, value=Name(param.name), ctx=ast.Load()))
            vararg = Loc(ast.arg, arg=param.name)
        elif param.kind == param.KEYWORD_ONLY:
            call_keywords.append(
                Loc(ast.keyword, arg=param.name, value=Name(param.name))
            )
            func_kwargs.append(Loc(ast.arg, arg=param.name))
        elif param.kind == param.VAR_KEYWORD:
            call_keywords.append(Loc(ast.keyword, arg=None, value=Name(param.name)))
            kwarg = Loc(ast.arg, arg=param.name)

    # generate the ast for the *callback* call
    call_ast = Loc(
        ast.Call, func=Name(callback.__name__), args=call_args, keywords=call_keywords
    )

    # generate the function ast
    func_ast = Loc(
        ast.FunctionDef,
        name=to_func_name(name),
        args=ast.arguments(
            args=func_args,
            posonlyargs=func_posonlyargs,
            vararg=vararg,
            defaults=func_defaults,
            kwarg=kwarg,
            kwonlyargs=func_kwargs,
            kw_defaults=func_kwdefaults,
        ),
        body=[Loc(ast.Return, value=call_ast)],
        decorator_list=[],
        returns=None,
    )

    # compile the ast and get the function code
    mod_ast = ast.Module(body=[func_ast])
    if sys.version_info >= (3, 8):
        mod_ast = ast.Module([func_ast], [])
    else:
        mod_ast = ast.Module([func_ast])
    # Use ast.parse instead of ast.Module for better portability
    # python 3.8 changes the signature of ast.Module
    # mod_ast = ast.parse("")
    # mod_ast.body = [func_ast]
    # mod_ast = ast.fix_missing_locations(mod_ast)

    # ValueError: Name node can't be used with 'None' constant
    # TypeError: required field "type_ignores" missing from Module
    # TypeError: required field "posonlyargs" missing from arguments
    module_code = compile(mod_ast, "<generated-ast>", "exec")
    func_code = [c for c in module_code.co_consts if isinstance(c, types.CodeType)][0]
    # return the generated function
    func = types.FunctionType(
        func_code, {callback.__name__: callback}, argdefs=tuple(defaults)
    )
    func.__kwdefaults__ = kwdefaults
    return func


##
## support functions
##


def viewitems(obj):
    return getattr(obj, "viewitems", obj.items)()


def viewkeys(obj):
    return getattr(obj, "viewkeys", obj.keys)()


def viewvalues(obj):
    return getattr(obj, "viewvalues", obj.values)()


def to_func_name(name):
    # func.__name__ must be bytes in Python2
    return to_unicode(name)


def to_bytes(s, encoding="utf8"):
    if isinstance(s, bytes):
        pass
    elif isinstance(s, str):
        s = s.encode(encoding)
    return s


def to_unicode(s, encoding="utf8"):
    if isinstance(s, bytes):
        s = s.decode(encoding)
    elif isinstance(s, str):
        pass
    elif isinstance(s, dict):
        s = {to_unicode(k): to_unicode(v) for k, v in viewitems(s)}
    elif isinstance(s, collections.Iterable):
        s = [to_unicode(x, encoding) for x in s]
    return s


def main():
    from inspect import signature

    # original function
    def original(a, b, *args, c, d=10, **kwargs):
        return a, b, args, c, kwargs

    sig = signature(original)
    print("original:", original)
    print("original signature:", sig)
    print("original ret:", original(1, 2, 4, c=5, borp="torp"))

    # cloned function
    def callback(*args, **kwargs):
        return args, kwargs

    cloned = create_function("clone", sig, callback)

    sig = signature(cloned)
    print("cloned:", cloned)
    print("cloned signature:", sig)
    print("cloned ret:", cloned(1, 2, 4, c=5, borp="torp"))


if __name__ == "__main__":
    main()
