#created by lai wei at 23/08/2021 13:29
#The runner script for drawing the qoe_cdf from raw log
import os
import prep_data
import compute_qoe
import qoe_cdf
from configs import raw_root,clean_root,qoe_root
import os.path
def file_extension(path):
  return os.path.splitext(path)[1]


if __name__=="__main__":
    #The list of traces, must be the same as .csv filename
    lid_list = ["alpha85","default","iperf_log"]
    txt_list = set(["iperf_log"])
    for lid in lid_list:
        if lid in txt_list:
            raw_ext = ".txt"
        else:
            raw_ext = ".csv"
        ext = ".csv"
        raw_path = os.path.join(raw_root,lid+raw_ext)
        clean_path = os.path.join(clean_root,lid+ext)
        #process the raw data log to standard format ones
        if file_extension(raw_path) == '.txt':
            prep_data.prep_txt(raw_path,clean_path)
        else:
            prep_data.prep_raw(raw_path, clean_path)
        qoe_path = os.path.join(qoe_root,lid+ext)
        #compute the qoe given standard format qos log
        compute_qoe.compute_qoe(clean_path,qoe_path)
    #draw the qoe cdf
    qoe_cdf.plot_qoe_cdf(lid_list)