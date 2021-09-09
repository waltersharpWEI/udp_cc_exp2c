#created by lai wei at 08/09/2021 14:24
#a simulator that generate a standard qos trace
#for our idea 1
import numpy as np
import pandas as pd
import os
import random
from configs import raw_root,exp_id
from compute_qoe import compute_acc_qoe_local

def gen_trace_bad(start_rate,end_rate,span,intensity=1):
    df = pd.DataFrame()
    bitrates = np.linspace(start_rate,end_rate,span)
    offset = np.random.randint(-intensity,+intensity,span)
    bitrates += offset
    bitrates[bitrates<0] = 0
    losss = np.zeros(span)
    losss[offset>0] += abs(offset[offset>0]/bitrates[offset>0])
    delays = np.zeros(span)
    #delays[offset>0] += 20
    df = pd.DataFrame({"th": bitrates, "loss": losss, "delay": delays})
    return df

def gen_trace_optimal(start_rate,end_rate,span):
    df = pd.DataFrame()
    bitrates = np.linspace(start_rate, end_rate, span)
    losss = np.zeros(span)
    delays = np.zeros(span)
    df = pd.DataFrame({"th": bitrates, "loss": losss, "delay": delays})
    return df

if __name__=="__main__":
    print("starting idea 1 simulator")
    lid = ["bad","optimal"]
    span = 30
    intensity = 50
    print("generating trace for " + lid[0] +" and " + lid[1])
    #generate the optimal trace for a congestion event with start rate 100 and end rate 20
    df_opt = gen_trace_optimal(13000000,10000000,span)
    #generate the tcp congestion control trace for a congestion event
    #with start rate 100 and end rate 20, and fluctuation intensity of 1
    df_bad = gen_trace_bad(100,20,span,intensity)
    print("writting trace to eid_"+str(exp_id))
    opt_path = os.path.join(raw_root, lid[1] + ".csv")
    bad_path = os.path.join(raw_root, lid[0] + ".csv")
    df_opt.to_csv(opt_path,index=False)
    df_bad.to_csv(bad_path,index=False)
    print("finished writting.")
    print("computing accumulated QoE of two traces...")
    opt_qoe = compute_acc_qoe_local(clean_path=opt_path)
    bad_qoe = compute_acc_qoe_local(clean_path=bad_path)
    print("Optimal QoE:"+str(opt_qoe))
    print("TCP QoE:"+str(bad_qoe))