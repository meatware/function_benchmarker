"""Run benchmarks."""

import os
import sys
import time
import logging
import inspect
import importlib
import time
import random
import statistics
#
LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

def benchmark(func_dic, *arg_list):
    """Run benchmarks on functions stored in a dictionary."""

    func_names = [func_name for func_name, _ in func_dic.items()]
    timing_dict = {func_name: [] for func_name, _ in func_dic.items()}

    len_func = len(func_dic.items())
    N =  200000
    n_iter = len_func * N

    # get roughly n_iter iterations
    for _ in range(n_iter):
        chosen_func = random.choice(func_names)

        ####################
        t0 = time.time()
        func_dic[chosen_func](*arg_list)
        t1 = time.time()
        ####################

        timing_dict[chosen_func].append((t1 - t0) * 1000)
    print("\nFine-tuning\n")

    # TODO: Implement fine tuning so all functions have same no of N iterations
    fine_tune_funcs = {}
    for func_name, numbers in timing_dict.items():
        coarse_len = len(numbers)
        #print(func_name, coarse_len)
        if coarse_len < N:
            fine_tune_funcs[func_name] = N - coarse_len

        norm_list_over = numbers[:N]
        # print("norm_list_over", len(norm_list_over))
        timing_dict[func_name] = norm_list_over

    #for func_name, remainder in fine_tune_funcs.items():

    stats_dic = {}
    for name, numbers in timing_dict.items():

        stats_dic[name] = [{}]
        fn_iter = len(numbers)
        print('Benchmarking function:', name, 'Used', fn_iter, 'times')
        stats_dic[name][0]["iter"] = fn_iter

        fn_median = statistics.median(numbers)
        print('\tMEDIAN', fn_median)
        stats_dic[name][0]["fn_median"] = fn_median

        fn_mean = statistics.mean(numbers)
        print('\tMEAN  ', fn_mean)
        stats_dic[name][0]["fn_mean"] = fn_mean

        fn_stdev = statistics.stdev(numbers)
        print('\tSTDEV ', fn_stdev)
        stats_dic[name][0]["fn_stdev"] = fn_stdev

    return stats_dic
