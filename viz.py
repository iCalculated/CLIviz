from sorts.bubble import bubble_sort
import importlib
import time
import time
import sys

if __name__ == "__main__":
    import sys

    """
    unsorted = list(range(100,0,-1))

    start = time.process_time()
    print(*bubble_sort(unsorted), sep=",")
    print(f"Processing time: {time.process_time() - start}")
    """

    lib = input("File to get sort from: ")
    sort = importlib.import_module("sorts." + lib)

    modulenames = set(sys.modules) & set(globals())
    allmodules = [sys.modules[name] for name in modulenames]
    print(allmodules)