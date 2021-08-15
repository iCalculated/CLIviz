from sorts.bubble import bubble_sort
import importlib
import time
import time
import sys

def get_functions(module):
    return [f for f in dir(module) if not f.startswith("__")]

def find_sort(module):
    funcs = get_functions(module)
    if len(funcs) != 1:
        raise SortModuleError("Too many functions in sort file! (Should be 1)")
    return getattr(module, funcs[0])

if __name__ == "__main__":

    lib = input("File to get sort from: ")
    sort_module = importlib.import_module("sorts." + lib)
    sort = find_sort(sort_module)
    
    unsorted = list(range(100,0,-1))

    start = time.process_time()
    print(sort(unsorted), sep=",")
    print(f"Processing time: {time.process_time() - start}")