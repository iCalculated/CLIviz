import ast
from loguru import logger
logger.add("out.log", backtrace=True, diagnose=True)  #

source_code = """
def bubble_sort(collection):
    length = len(collection)
    for i in range(length - 1):
        swapped = False
        for j in range(length - 1 - i):
            if collection[j] > collection[j + 1]:
                swapped = True
                collection[j], collection[j + 1] = collection[j + 1], collection[j]
        if not swapped:
            break  
    return collection
"""
ast.parse(source, mode="exec")

explorer = ASTExplorer(source_code)
for result in explorer.getVariables():
    print(f"Found variable '{result.var}' with a value of '{result.expression}' (type: '{result.vType.__name__}')")