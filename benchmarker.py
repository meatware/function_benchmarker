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
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.dates as mdates
from matplotlib import rcParams
from pylab import figure

rcParams['axes.labelsize'] = 14
rcParams['xtick.labelsize'] = 14
rcParams['ytick.labelsize'] = 14
rcParams['legend.fontsize'] = 12

rcParams['font.family'] = "Dejavu Sans"
rcParams['font.serif'] = ["Computer Modern Roman"]

rcParams['xtick.major.pad'] = 12
rcParams['ytick.major.pad'] = 12

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

def _get_def_files(dirname):
    files = [fil.replace(".py", "") for fil in os.listdir(dirname) if fil.startswith("test_")]

    LOG.info("def files found: %s", files)

    return files

def _import_func_defs(graphdef_files):

    _modules = __import__('func_defs', globals(), locals(), graphdef_files, 0)

    _module_list = [(key, value) for key, value in inspect.getmembers(_modules) if inspect.ismodule(value)]

    LOG.info("_module_list %s", _module_list)

    func_dict = {}
    for module_name, _ in _module_list:
        #print("*", module_name, val)
        mymodule = importlib.import_module("func_defs."  + module_name)
        LOG.info(" module Loaded %s", mymodule.__name__)


        for oxo in inspect.getmembers(mymodule):
            #print("oxo", oxo)
            if inspect.isfunction(oxo[1]):
                # func_dict["function_name"] = function
                func_name = oxo[1].__name__
                LOG.info(" func_name %s", func_name)
                func_dict[func_name] = oxo[1]


    LOG.info("No of function defs: %s ", str(len(func_dict)))

    return func_dict

def load(dirname):
    _func_def_files = _get_def_files(dirname)
    return _import_func_defs(_func_def_files)

#def benchmark(func1, func2, test_string, check_str_list, inc_exc_switch):
def benchmark(func_dic, *arg_list):
    #functions = func1, func2
    # times = {f.__name__: [] for f in functions}

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

if __name__ == "__main__":
    func_dic = load(dirname="./func_defs")
    # test_string="Lives-Stack-5"
    # check_str_list=["Live-StAck"]
    # inc_exc_switch="include"

    for key, val in func_dic.items():
        print("\n X", key, val)
        #print(val(test_string, check_str_list, inc_exc_switch))

    print("\nYYYYYYYYYYYYYYYYYYYYYYYY\n")
    # arg_dict = {"test_string": "Lives-Stack-5",
    #             "check_str_list": ["Live-StAck"],
    #             "inc_exc_switch": "include"}

    arg_list = ["Lives-Stack-5", ["Live-StAck"], "include"]

    stats_dic = benchmark(func_dic, *arg_list)

    print("\nZZZZZZZZZZZZZZZZZZZZZZZZ\n")

    def make_graphs(stats_dic):

        fn_li = []
        median_li = []
        mean_li = []
        stddev_li = []
        for fn_name, values in stats_dic.items():
            fn_li.append(fn_name)
            #print("u", values)
            median_li.append(values[0]["fn_median"])
            mean_li.append(values[0]["fn_mean"])
            stddev_li.append(values[0]["fn_stdev"])

        return {"fn_li": fn_li,
                "median_li": median_li,
                "mean_li": mean_li,
                "stddev_li": stddev_li}


    for key, value in stats_dic.items():
        print("O", key, value)

    graph_data_dic = make_graphs(stats_dic)
    for key, value in graph_data_dic.items():
        print("5", key, value)

    def plot_graphs(graph_data_dic):
        """Plot bar graphs with error bars."""

        y_vals_keys = ["median_li", "mean_li"]
        x_axis = graph_data_dic["fn_li"]

        for y_key in y_vals_keys:
            fig_name = y_key + ".png"
            title_var = y_key

            y_vals = graph_data_dic[y_key]
            x_pos = list(range(0, len(y_vals), 1))
            print("\nCC", y_key, y_vals )

            fig = figure()
            plt.xticks(rotation=90)
            plt.title(title_var)

            ax1 = plt.subplot(1, 1, 1)


            ax1.grid(True)
            ax1.set_title(title_var)
            #ax1.axhline(y=2.0, color="grey", linestyle='dashed', lw=1.5)
            ax1.bar(x_pos,
                    y_vals,
                    width=0.8,
                    color="g",
                    ecolor="k",
                    yerr=graph_data_dic["stddev_li"],
                    tick_label=graph_data_dic["fn_li"],
                    capsize=0.2,
                    alpha=0.55)

            #ax1.plot(x_axis, value)

            # xxxxxxxxxxxxxx

            plt.tight_layout(pad=0.9, w_pad=0.5, h_pad=1.0)
            #plt.show()
            plt.savefig(fig_name)
            plt.cla()
            plt.close(fig)


    plot_graphs(graph_data_dic=graph_data_dic)






            #print(val[1](test_string, check_str_list, inc_exc_switch))
    #benchmark(check_substrings_artur_initial, check_substrings_artur, test_string, check_str_list, inc_exc_switch)