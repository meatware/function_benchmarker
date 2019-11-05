from function_loader import load
from benchmarker import benchmark
from plotters import make_graphs, plot_graphs


if __name__ == "__main__":

    # load function
    func_dic = load(dirname="./func_defs")

    # supply argument list
    arg_list = ["Lives-Stack-5", ["Live-StAck"], "include"]

    # run benchmarking
    stats_dic = benchmark(func_dic, *arg_list)

    # create graph dictionary
    graph_data_dic = make_graphs(stats_dic)

    # plot graphs
    plot_graphs(graph_data_dic=graph_data_dic)




