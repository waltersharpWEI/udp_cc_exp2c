#created by lai wei at 23/08/2021 13:29
#The data preprocessors
#created by lai wei on 19/08/2021 14:59 (UTC+8)
#process the raw log data
import pandas as pd
import numpy as np
from aws_db import put_item
from configs import exp_id

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

def prep_txt_pantheon(raw_path, clean_path,lid,upload=False):
    losss = []
    delays = []
    ths = []
    with open(raw_path,'r') as f1:
        for line in f1.readlines():
            tokens = line.split()
            loss = 5
            th = float(tokens[1]) * 1000000 * 0.2
            th = int(th)
            delay = int(float(tokens[2])*200)
            losss.append(loss)
            delays.append(delay)
            ths.append(th)
    delays = np.array(delays)
    losss = np.array(losss)
    ths = np.array(ths)
    df = pd.DataFrame({'th': ths, 'delay': delays, 'loss': losss})
    df.to_csv(clean_path, index=False)
    if upload:
        print("upload to aws db")
        put_item(exp_id,lid,df)
        print("finished uploading")
    return

def prep_txt(raw_path, clean_path,lid,upload=False):
    losss = []
    delays = []
    ths = []
    with open(raw_path,'r') as f1:
        for line in f1.readlines():
            tokens = line.split()
            sub_tokens = tokens[10].split('/')
            loss = float(sub_tokens[0])/float(sub_tokens[1])
            loss = int(loss * 100)
            th = float(tokens[6]) * 10000
            th = int(th)
            delay = 55
            losss.append(loss)
            delays.append(delay)
            ths.append(th)
    delays = np.array(delays)
    losss = np.array(losss)
    ths = np.array(ths)
    df = pd.DataFrame({'th': ths, 'delay': delays, 'loss': losss})
    df.to_csv(clean_path, index=False)
    if upload:
        print("upload to aws db")
        put_item(exp_id,lid,df)
        print("finished uploading")
    return

def prep_raw(raw_path, clean_path,lid, upload=False):
    trim_head(raw_path,raw_path)
    th1 = pull_th1(raw_path)
    delay1 = pull_delay(raw_path)
    loss1 = pull_loss(raw_path)
    loss1 = diff_loss(loss1)
    df = pd.DataFrame({'th': th1, 'delay': delay1, 'loss':loss1})
    df.to_csv(clean_path,index=False)
    if upload:
        print("upload to aws db")
        put_item(exp_id,lid,df)
        print("finished uploading")
    return

if __name__=="__main__":
    print("This is prep")
    #prep_raw("data/raw/default.csv","data/gcc/default.csv")