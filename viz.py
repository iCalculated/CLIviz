from sorts.bubble import bubble_sort
import time
from heartrate import trace, files
import time

if __name__ == "__main__":
    trace(files=files.path_contains("sorts"), browser=False)
    unsorted = list(range(100,0,-1))
    start = time.process_time()
    print(*bubble_sort(unsorted), sep=",")
    print(f"Processing time: {time.process_time() - start}")