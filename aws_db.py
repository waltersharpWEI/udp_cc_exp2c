#aws dynamoDB helpers
import boto3
import time
import pandas as pd
import numpy as np
from configs import table_name, is_debug
#eid: experiment id, strictly increase int
#lid: line id, string


#put item to the dynamodb given eid and lid
#input: the dataframe in standard qos format
def put_item(eid,lid,df):
    th1 = np.array(df['th'])
    delay1 = np.array(df['delay'])
    loss1 = np.array(df['loss'])
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    try:
        table.put_item(
            Item={
                'eid':str(eid),
                'lid':str(lid),
                'th':th1.tolist(),
                'delay':delay1.tolist(),
                'loss':loss1.tolist(),
                'timestamp': int(time.time())
            }
        )
    except Exception as e:
        print("Error when put to dynamoDB:")
        print(e)

#get item from the dynamodb given eid and lid
#output: the dataframe in standard qos format
def get_item(eid,lid):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    try:
        response = table.get_item(
            Key={
                'eid':str(eid),
                'lid':str(lid)
            }
        )
        item = response["Item"]
        df = pd.DataFrame({'th':item['th'],'delay':item['delay'],'loss':item['loss']})
        return df
    except Exception as e:
        print("Error when get from dynamoDB:")
        print(e)