#created by lai wei at 23/08/2021 13:29
#The runner script for drawing the qoe_cdf from raw log

import pandas as pd
import numpy as np

def max_qoe(trace1,trace2,output):
    df1 = pd.read_csv(trace1)
    df2 = pd.read_csv(trace2)
    qoe1 = np.array(df1["qoe"])
    qoe2 = np.array(df2["qoe"])
    qoe_max = np.maximum(qoe1[:qoe2.size],qoe2) + 1
    df_max = pd.DataFrame(qoe_max,columns=["qoe"])
    df_max.to_csv(output)
    return