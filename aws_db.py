# Get the service resource.
import boto3
import time
import pandas as pd

def put_item(eid,lid,th1,delay1,loss1):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('gcc_qoe_exp_1')
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
        print(e)
        print("error when insert to dynamoDB!")

def get_item(eid,lid):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('gcc_qoe_exp_1')
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
        print(e)
        print("error when get from dynamoDB!")