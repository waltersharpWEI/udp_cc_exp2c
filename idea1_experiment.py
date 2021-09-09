#created by lai wei at 08/09/2021 14:24
#the script to analysis the logs in the experiment 1
#for our idea 1
import numpy as np
import pandas as pd
import os
import random
from configs import raw_root,exp_id,clean_root
from compute_qoe import compute_acc_qoe_local,compute_qoe_local_numpy
import matplotlib.pyplot as plt

def clean_trace_pcc(raw_path,clean_path):
    with open(raw_path,'r') as f1:
        line = f1.readline()
        rates = line.split(", ")
        bitrates = []
        for rate in rates:
            bitrates.append(int(float(rate) * 1000000))
    trace_len = 30
    bitrates = bitrates[30:60]
    losss = np.zeros(trace_len)
    delays = np.zeros(trace_len)
    df = pd.DataFrame({"th": bitrates, "loss": losss, "delay": delays})
    df.to_csv(clean_path,index=False)
    return df

def plot_qoe_time(opt_path,bad_path,fig_path):
    pcc_color='blue'
    opt_color='red'
    opt_qoes = compute_qoe_local_numpy(opt_path)
    bad_qoes = compute_qoe_local_numpy(bad_path)
    opt_qoe = compute_acc_qoe_local(clean_path=opt_path)
    bad_qoe = compute_acc_qoe_local(clean_path=bad_path)
    plt.plot(opt_qoes,label="optimal",color=opt_color)
    plt.plot(bad_qoes,label="pcc", color=pcc_color)
    plt.annotate("Optimal accQoE=%.1f" % opt_qoe,
                 (22,470),color=opt_color)
    plt.annotate("PCC accQoE=%.1f" % bad_qoe,xy=(20,610),color=pcc_color)
    plt.xlabel("Time(s)")
    plt.ylabel("QoE")
    plt.legend()
    plt.show()
    plt.savefig(fig_path)

if __name__=="__main__":
    lid = ["pcc","optimal"]
    span = 10
    opt_path = os.path.join(clean_root, lid[1] + ".csv")
    bad_path = os.path.join(clean_root, lid[0] + ".csv")
    bad_raw_path = os.path.join(raw_root, lid[0] + ".txt")
    print(bad_raw_path)
    print(bad_path)
    df_opt = clean_trace_pcc(bad_raw_path,bad_path)
    #generate the tcp congestion control trace for a congestion event
    #with start rate 100 and end rate 20, and fluctuation intensity of 1
    #df_bad = gen_trace_bad(100,20,10,intensity)
    print("writting trace to eid_"+str(exp_id))

    #df_opt.to_csv(opt_path,index=False)
    #df_bad.to_csv(bad_path,index=False)
    print("finished writting.")
    print("computing accumulated QoE of two traces...")
    opt_qoe = compute_acc_qoe_local(clean_path=opt_path)
    bad_qoe = compute_acc_qoe_local(clean_path=bad_path)
    plot_qoe_time(opt_path,bad_path,"qoe_time.pdf")
    print("Optimal QoE:"+str(opt_qoe))
    print("TCP QoE:"+str(bad_qoe))