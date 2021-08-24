#created by lai wei at 23/08/2021 13:29
#The data preprocessors
#created by lai wei on 19/08/2021 14:59 (UTC+8)
#process the raw log data
import pandas as pd
import numpy as np
import os

#trim the meaningless data at the start
#of exp, and save the file to path_out
def trim_head(path_in, path_out):
    df = pd.read_csv(path_in)
    df = df[df["bandwith.googActualEncBitrate"] > 0]
    df.to_csv(path_out,index=False)
    #print(df)


#read the trace, return the numpy array
#of the tranmitBitrate
def pull_th1(path):
    df = pd.read_csv(path)
    th1 = df["bandwith.googTransmitBitrate"]
    th1 = np.array(th1)
    return th1

def pull_th2(path):
    df = pd.read_csv(path)
    th2 = df["bandwith.googAvailableSendBandwidth"]
    th2 = np.array(th2)
    return th2

def pull_loss(path):
    df = pd.read_csv(path)
    loss = df["result.results.packetsLost"]
    loss = np.array(loss)
    return loss

def pull_delay(path):
    df = pd.read_csv(path)
    delay = df["result.results.googCurrentDelayMs"]
    delay = np.array(delay)
    return delay

#calculate current loss from acc loss
#needs test
def diff_loss(loss):
    diff = []
    for i in range(1,len(loss)):
        diff.append(loss[i]-loss[i-1])
    diff.append(0)
    return np.array(diff)

def prep_raw(raw_path, clean_path):
    trim_head(raw_path,raw_path)
    th1 = pull_th1(raw_path)
    delay1 = pull_delay(raw_path)
    loss1 = pull_loss(raw_path)
    loss1 = diff_loss(loss1)
    df = pd.DataFrame({'th': th1, 'delay': delay1, 'loss':loss1})
    df.to_csv(clean_path,index=False)
    return

if __name__=="__main__":
    print("This is prep")
    #prep_raw("data/raw/default.csv","data/gcc/default.csv")