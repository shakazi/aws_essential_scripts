#Gathers folder names from s3 and generates a csv to save all data


import boto3
import csv
  
def addtocsv(data):
    file = open('claimNumbers.csv', 'a+', newline ='')
    with file:    
        write = csv.writer(file)
        write.writerows(data)

def list_bucket_keys(bucket_name):
    s3_client = boto3.client("s3")
    #result = s3_client.list_objects(Bucket=bucket_name, Prefix="April20-sep20-batch-1/policy/", Delimiter="/")
    
    paginator = s3_client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix="total-data-dump/policy/", Delimiter="/")
    res_list = []
    for page in page_iterator:
        res = [d['Prefix'].split('/')[-2] for d in page['CommonPrefixes']]
        res_list.append(res)
    return res_list

if __name__ == '__main__':
    data = list_bucket_keys("tagic-claims-data")
    print('Data gathered')
    addtocsv(data)
    print('Data loaded')
        
