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
    for lid in lid_list:
        ext=".csv"
        qoe_path = os.path.join(qoe_root, lid + ext)
        df = pd.read_csv(qoe_path)
        qoes = np.array(df["qoe"])
        cdf,bins = compute_cdf(qoes,100)
        plt.plot(bins,cdf,label=lid)
    plt.xlim(2,12)
    plt.legend()
    plt.savefig(fig_path)
    plt.show()
    return