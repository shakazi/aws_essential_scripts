import json
import boto3
import json
import csv

_bucket='tagic-car-img-fraud-data'
s3 = boto3.client("s3")

def get_matching_s3_keys(bucket, prefix='', suffix=''):
    s3 = boto3.client('s3')
    kwargs = {'Bucket': bucket}
    if isinstance(prefix, str):
        kwargs['Prefix'] = prefix
    while True:
        resp = s3.list_objects_v2(**kwargs)
        for obj in resp['Contents']:
            ans = []
            key = obj['Key']
            etag = obj['ETag']
            ans = [key, etag]
            if key.startswith(prefix) and key.endswith(suffix):
                print(ans)
                yield ans
        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break

def get_required_keys():
  req_keys =[]
  req_keys = get_matching_s3_keys(bucket=_bucket, suffix=('.jpg', '.JPG','.png','.PNG','.pdf','.PDF','.jpeg','.JPEG'))
  return list(req_keys)

def generate_csv(hashes):
    print('\nCSV generation started...')
    i = 0
    multiLine = ""
    for item in hashes:
        newLine = ','.join(map(str, item))
        if (i > 0):
            multiLine = multiLine + '\n'
        multiLine = multiLine + newLine
        i = i+ 1
    print('multiline generated!')
    print('uploading csv to s3 bucket...')
    client = boto3.client('s3')
    client.put_object(
        Body=multiLine,
        Bucket= 'image-reuse-test',
        Key='full_bucket_data.csv'
    )

def lambda_handler(event, context):
    ans = list(get_matching_s3_keys(_bucket, '1-year'))
    ans.append()
    flag = 0
    req_hashes = []
    i=0
    print('LENGTH', len(ans))
    for obj in ans:
      address = obj[0].split('/')
      i=0
      flag = 0
      for word in address:
        if(word=='policy'):
            flag =1
            break
        i = i+1
      claimId = ""
      if(flag ==1):
        claimId = address[i+1]
      hash = obj[1]
      hash = hash[1:33]
      a= [hash, claimId, address]
      req_hashes.append(a)
    generate_csv(req_hashes)
    print('Upload success!')

if __name__=="__main__":
    lambda_handler(0,0)
