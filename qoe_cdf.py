#created by lai wei at 23/08/2021 13:29
#The qoe cdf plotter

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from configs import qoe_root

def compute_cdf(qoes,bins):
    count, bins_count = np.histogram(qoes, bins=bins)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    return cdf,bins_count[1:]

def plot_qoe_cdf(lid_list,fig_path):
    asize = 36
    bsize = 36
    lwidth = 5
    # set up the figure canvas
    figure = plt.figure(figsize=(16, 9), dpi=80)
    # set up the margin
    ax = figure.add_axes([0.115, 0.15, 0.8, 0.8])
    # set up the tick size
    ax.tick_params(pad=18, labelsize=bsize - 2)

    line_colors = {"CUBIC":"red","PCC":"blue"}

    for lid in lid_list:
        ext=".csv"
        qoe_path = os.path.join(qoe_root, lid + ext)
        df = pd.read_csv(qoe_path)
        qoes = np.array(df["qoe"])
        cdf,bins = compute_cdf(qoes,100)
        plt.plot(bins,cdf,label=lid, color=line_colors[lid], linewidth=lwidth)

    ax.set_xlabel('QoE', fontsize=asize)
    ax.set_ylabel('CDF', fontsize=asize)
    # ax.set_ylabel('CDF', fontsize=asize)
    ax.set_xlim(4, 11)
    ax.set_ylim(0, 1)
    plt.legend(loc='upper left', fontsize=asize - 10)
    plt.savefig(fig_path)
    plt.show()
    return