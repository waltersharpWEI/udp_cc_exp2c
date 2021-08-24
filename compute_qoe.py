#created by lai wei at 23/08/2021 13:29
#The qoe computers
import pandas as pd

def qos_qoe(th,delay,loss):
    a = 0.000005
    b = -0.002
    c = -0.01
    qoe = th * a + delay * b + loss * c
    return qoe

def compute_qoe(clean_path,qoe_path):
    df = pd.read_csv(clean_path)
    qoe = qos_qoe(df['th'],df['delay'],df['loss'])
    df_qoe = pd.DataFrame(qoe,columns=["qoe"])
    df_qoe.to_csv(qoe_path,index=False)
    return