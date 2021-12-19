#standard lib
import os
import json
import decimal

#external libraries
import boto3#pip install boto3

#local files
import aws_config#./aws_config.py

from botocore.exceptions import ClientError

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name=os.environ["AWS_DEFAULT_REGION"])

table = dynamodb.Table('test')

#Insert new user data into the system
try:
    response = table.put_item(
       Item={
            'id': "hello",
            "name":"world"
        }
    )
except ClientError as e:
    print(e)
    print("client error:",e.response['Error']['Message'])
else:
    print("PutItem succeeded:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))

'''
TODO: make into rest api web server
endpoints:
PUT /sentence?id=example
request body is the sentence itself

PUT /keystrokes?user=example&session=example2
request body is the csv-formatted data, with each row like this:
user-id, session-id, sentence-id, timestamp, key

GET /sentence?id=example

GET /keystrokes?user=example
GET /keystrokes?session=example2 ???
GET /keystrokes?user=example&session=example2 ???
If each session is unique and only has one user, we might only need it to accept session as a query param and it can ignore user

GET /keystrokes?sentence=example-sentence-id ??? if we need to get all keystrokes typed for a certain sentence


'''