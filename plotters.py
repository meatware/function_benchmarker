import sys
import logging
import matplotlib
#matplotlib.use("agg")
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