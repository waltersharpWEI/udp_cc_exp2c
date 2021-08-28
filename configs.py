#created by lai wei at 23/08/2021 13:29
#The enviroment varaiables for runner
import os
#whether upload and get the data from dynamoDB
local=False
is_debug=False
#table name
table_name = 'gcc_qoe_exp_1'
#the experiment id, each constitutes to all the data for a plot
exp_id = 2
#the root path of the data
data_root = "data"
#the root path of the output pdf plot
pdf_root = "pdf"
#the root path of the raw log
raw_root = os.path.join(data_root,"eid_"+str(exp_id),"raw")
#the cleaned path of the qos log in standard format
clean_root = os.path.join(data_root,"eid_"+str(exp_id),"clean")
#the qoe trace path
qoe_root = os.path.join(data_root,"eid_"+str(exp_id),"qoe_trace")