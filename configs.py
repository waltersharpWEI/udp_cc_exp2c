#created by lai wei at 23/08/2021 13:29
#The enviroment varaiables for runner
import os
exp_id = 1
data_root = "data"
pdf_root = "pdf"
raw_root = os.path.join(data_root,"eid_"+str(exp_id),"raw")
clean_root = os.path.join(data_root,"eid_"+str(exp_id),"clean")
qoe_root = os.path.join(data_root,"eid_"+str(exp_id),"qoe_trace")