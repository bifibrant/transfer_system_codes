import math


# Find all divisors of n
def divisor_generator(n):
    large_divisors = []
    for i in range(1, int(math.sqrt(n) + 1)):
        if n % i == 0:
            yield i
            if i * i != n:
                large_divisors.append(n / i)
    for divisor in reversed(large_divisors):
        yield int(divisor)


# GCD dictionary computation
def gcd_dictionary(n):
    dictionary = {}
    sub = list(divisor_generator(n))
    for i in sub:
        for j in sub:
            dictionary[(i, j)] = math.gcd(i, j)
    return dictionary


# Integer to padded bitstring
def int_to_bin_padded(n, pad_length):
    return bin(n)[2:].zfill(pad_length)


# Generate all possible edges for the transfer system
def all_edges(n):
    edges = []
    sub = list(divisor_generator(n))
    for i in sub:
        for j in sub:
            if i < j and j % i == 0:
                edges.append((i, j))
    return edges


# Transfer system check
def transfer_check(candidate, sub, gcdDict) -> bool:
    rule1 = True

    for edge in candidate:
        j = 0
        while sub[j] < edge[1]:
            if edge[1] % sub[j] == 0:
                gcdRes = gcdDict[(edge[0], sub[j])]
                if gcdRes != sub[j]:
                    if not (gcdRes, sub[j]) in candidate:
                        return False
            j += 1

    if rule1:
        for i in range(len(candidate)):
            for j in range(i + 1, len(candidate)):
                if candidate[i][1] == candidate[j][0]:
                    if not (candidate[i][0], candidate[j][1]) in candidate:
                        return False

    return True


# This function will check a subcollection of transfer systems ready for multithreading
def thread_process(sub, gcdDict, start_value, end_value, poss_edges, Q):
    result = 0
    order = len(poss_edges)

    for i in range(start_value, end_value):
        # BUILD THE CANDIDATE
        candidate = []
        indicator = int_to_bin_padded(i, order)
        for k in range(order):
            if indicator[k] == "1":
                candidate.append(poss_edges[k])
        if transfer_check(candidate, sub, gcdDict):
            result += 1
    Q.put(result)


    #
    #
    #
    #
    #
    # #
    # #
    # #
    # #
    # # result = 0
    # #
    # # for i in range(0, pow(2, ORDER)):
    # #     # BUILD THE CANDIDATE
    # #     candidate = []
    # #     indicator = int_to_bin_padded(i, ORDER)
    # #     for k in range(ORDER):
    # #         if indicator[k] == "1":
    # #             candidate.append(poss_edges[k])
    # #     if transfer_check(candidate, sub, gcdDict):
    # #         result += 1
    # #
    # # print(result)
    #
    # exit(0)
    #
    # # 2^order is the number of things that we want to check
    # ORDER = len(all_edges(N))
    #
    # # eventually n will be the number of possible edges! which is ALSO the pad value
    #
    # big_k = pow(2, ORDER)
    #
    # # this is the increase we need
    # INCREMENT = pow(2, ORDER - NUM_THREADS_FACTOR)
    #
    # for i in range(0, NUM_THREADS):
    #     thread = multiprocessing.Process(target=do_loop, args=(i * INCREMENT, (i + 1) * INCREMENT, QUEUE))
    #     THREAD_STORE.append(thread)
    #     thread.start()
    #
    # for thread in THREAD_STORE:
    #     ret = QUEUE.get()
    #     RESULT_LIST.append(ret)
    #
    # for thread in THREAD_STORE:
    #     thread.join()
    #
    # print(RESULT_LIST)
    #
    # print("Time elapsed for multiprocessing = ", time.time() - start_time, "s")