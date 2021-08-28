#created by lai wei at 23/08/2021 13:29
#The runner script for drawing the qoe_cdf from raw log
#The script sync the trace with dynamodb when env local is set False
#The intermideite result is stored into file, this can be improved in
#the future using redis
import os
import prep_data
import compute_qoe
import qoe_cdf
from configs import raw_root,clean_root,qoe_root,pdf_root,exp_id,local

import os.path
#get the extension name of a file
def file_extension(path):
  return os.path.splitext(path)[1]


if __name__=="__main__":
    #The list of traces, must be the same as .csv filename
    lid_list = ["tod10","tod11","tod12","tod13"]
    #The list of traces in txt format, this is tailored for iperf log
    txt_list = set([])
    #The name of the figure to be outputed
    fig_name = "propagation_delay_mot.pdf"
    fig_path = os.path.join(pdf_root,fig_name)
    for lid in lid_list:
        if lid in txt_list:
            raw_ext = ".txt"
        else:
            raw_ext = ".csv"
        ext = ".csv"
        raw_path = os.path.join(raw_root,lid+raw_ext)
        clean_path = os.path.join(clean_root,lid+ext)
        #process the raw data log to standard format ones
        #save the file to clean_path anyway
        #if env local is set, the qos trace will be uploaded to dynamodb
        if file_extension(raw_path) == '.txt':
            prep_data.prep_txt(raw_path,clean_path,lid,not local)
        elif file_extension(raw_path) == '.csv':
            prep_data.prep_raw(raw_path, clean_path,lid,not local)
        qoe_path = os.path.join(qoe_root,lid+ext)
        #compute the qoe given standard format qos log
        #if env local is set to be True, the qos trace should be
        #get from the dynamodb
        if local:
            compute_qoe.compute_qoe_local(clean_path,qoe_path)
        else:
            compute_qoe.compute_qoe(exp_id,lid,qoe_path)
    #draw the qoe cdf
    qoe_cdf.plot_qoe_cdf(lid_list,fig_path)