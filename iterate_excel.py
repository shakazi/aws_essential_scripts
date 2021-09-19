from pprint import pprint
import boto3
import openpyxl
import time
import csv

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

def addtocsv(data):
    file = open('result.csv', 'a+', newline ='')
    # with file:    
    #     write = csv.writer(file)
    #     write.writerows(data)
    writer = csv.writer(file)
    for key in data:
        writer.writerow(key)

    file.close()

arr= []

def append_to_arr(res):
    res = res[2:]
    res = '['+ res+ ']'
    arr.append([res])

def calculate_unique(request):
    #request = request.split('}')
    d = '}'
    request =  [e+d for e in request.split(d) if e]
    request[0] = ", "+ request[0][1:]
    request.pop()
    
    myset = set()
    for i in request:
        myset.add(i)

    result = ""
    count =0 
    for j in myset:
        result = result + str(j)
        count = count+ 1
    
        #print(result)
    return result



if __name__ == '__main__':
    today = int(time.time())
    wb= openpyxl.load_workbook('final_record_sorted.xlsx')
    print('Workbook loaded!')
    sh1 = wb['final_record_sorted']
    for i in range (422199,422201):
            request = sh1.cell(i,2).value
            res =calculate_unique(request)
            append_to_arr(res)
            #output = put_object(fileHash, request, today)
            print("Success for item", i)
            #pprint(output, sort_dicts=False)
    #print(arr)
    addtocsv(arr)