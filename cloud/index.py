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