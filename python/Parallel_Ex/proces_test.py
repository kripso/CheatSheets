# SuperFastPython.com
# example of calling submit with a function call
from time import sleep
from random import random
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed

# custom task that will sleep for a variable amount of time
def task(path):
    # sleep for less than a second
    _sleep = random()
    sleep(_sleep)
    print(round(_sleep, 2), path)
    return "all done"


# entry point
def main():
    paths = ["path1", "path2", "path3", "path4"]
    # start the process pool
    with ProcessPoolExecutor(max_workers=4) as executor:
        # submit the task
        futures = {executor.submit(task, path): path for path in paths}
        # get the result
        results = [future.result() for future in as_completed(futures)]

    print(results)


if __name__ == "__main__":
    main()
