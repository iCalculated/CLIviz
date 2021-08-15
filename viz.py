import importlib
import time
import sys
import os
import cmd
from nubia import Nubia, Options, command, context, argument, PluginInterface
from nubia.internal.cmdbase import AutoCommand
from termcolor import cprint

def get_functions(module):
    return [f for f in dir(module) if not f.startswith("__")]

def find_sort(module):
    funcs = get_functions(module)
    if len(funcs) != 1:
        raise SortModuleError("Too many functions in sort file! (Should be 1)")
    return getattr(module, funcs[0])

if __name__ == "__main__":

    cli = cmd.Cmd()

    LIB_NAME = "bubble_sort"
    lib = LIB_NAME if LIB_NAME else input("File to get sort from: ")

    sort_module = importlib.import_module("sorts." + lib)
    sort = find_sort(sort_module)
    
    unsorted = list(range(100,0,-1))

    start = time.process_time()
    print(sort(unsorted), sep=",")
    print(f"Processing time: {time.process_time() - start}")