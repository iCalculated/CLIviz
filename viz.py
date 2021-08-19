import ast
from loguru import logger
logger.add("out.log", backtrace=True, diagnose=True)  #

source_code = """
def bubble_sort(collection):
    length = len(collection)
    for i in range(length - 1):
        pass
    print(length)
    return collection
"""
tree = ast.dump(ast.parse(source_code, mode="exec"), indent=2)
print(tree)