#created by lai wei at 23/08/2021 13:29
#The qoe computers
import pandas as pd
import numpy as np
from aws_db import get_item

def qos_qoe(th,delay,loss):
    #the relative weight of th, delay, loss
    a = 0.000005
    b = -0.002
    c = -0.01
    th = np.array(th).astype(int)
    delay = np.array(delay).astype(int)
    loss = np.array(loss).astype(int) / 100.0
    qoe = th * a + delay * b + loss * c
    return qoe

#get the qos trace from the local path
def compute_qoe_local(clean_path,qoe_path):
    df = pd.read_csv(clean_path)
    qoe = qos_qoe(df['th'],df['delay'],df['loss'])
    df_qoe = pd.DataFrame(qoe,columns=["qoe"])
    df_qoe.to_csv(qoe_path,index=False)
    return

#get the qos trace from dynamodb
def compute_qoe(eid,lid,qoe_path):
    #get the dataframe from the db
    df = get_item(eid,lid)
    qoe = qos_qoe(df['th'],df['delay'],df['loss'])
    df_qoe = pd.DataFrame(qoe,columns=["qoe"])
    #cache the dataframe locally
    df_qoe.to_csv(qoe_path,index=False)
    return