from pprint import pprint
import boto3
import openpyxl
import time

def put_object(fileHash, request='', today = int(time.time()), dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table('image-reuse-image-hash-dev')
    response = table.put_item(
       Item={        
                'fileHash': fileHash,
                'createdOn': today,
                'requests': request,
                'updatedOn': today
        }
    )
    return response


if __name__ == '__main__':
    today = int(time.time())
    wb= openpyxl.load_workbook('final_db_data.xlsx')
    print('Workbook loaded!')
    sh1 = wb['Sheet1']
    for i in range (2,640901):
            fileHash = sh1.cell(i,1).value
            request= [
                {
                "sourceElementId": sh1.cell(i,2).value,
                "clientId": "BACKFILL",
                "subLob": sh1.cell(i,4).value,
                "sourceSystem": "ICAN",
                "createdOn": today,
                "lob": "motor"
                }
                ]
            output = put_object(fileHash, request, today)
            print("Put object succeeded for item",i, fileHash)
            #pprint(output, sort_dicts=False)