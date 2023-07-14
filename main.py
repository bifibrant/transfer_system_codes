import multiprocessing
import time
from aux import *

# DEFINE CONSTANTS
NUM_THREADS_FACTOR = 5
NUM_THREADS = pow(2, NUM_THREADS_FACTOR)
RESULT_LIST = []
THREAD_STORE = []
QUEUE = multiprocessing.Queue()

# The order of the cyclic group that we are interested in
########
N = 36
########

if __name__ == "__main__":
    start_time = time.time()

    poss_edges = all_edges(N)
    ORDER = len(poss_edges)
    sub = list(divisor_generator(N))
    gcdDict = gcd_dictionary(N)
    INCREMENT = pow(2, ORDER - NUM_THREADS_FACTOR)

    for i in range(0, NUM_THREADS):
        thread = multiprocessing.Process(target=thread_process, args=(sub, gcdDict, i * INCREMENT, (i + 1) * INCREMENT, poss_edges, QUEUE))
        THREAD_STORE.append(thread)
        thread.start()

    print("Thunderthreads are go")

    for thread in THREAD_STORE:
        ret = QUEUE.get()
        RESULT_LIST.append(ret)

    for thread in THREAD_STORE:
        thread.join()

    print(sum(RESULT_LIST))

    print("Time elapsed = ", time.time() - start_time, "s")
