import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#this class is here to make it a bit easier to use the relevant properties of the event parameter in the handler function
class APIEvent:
    path: str
    httpMethod: str
    queryParams: dict
    body: str

    def __init__(self, event_dict: dict):
        self.path = event_dict['path']
        self.httpMethod = event_dict['httpMethod']
        self.queryParams = event_dict['queryStringParameters']
        if 'body' in event_dict:
            self.body = event_dict['body']
        else:
            self.body = None
    def __repr__(self):
        return f'APIEvent{self.__dict__}'

def get_keystrokes(queryParams):
    pass

def post_keystrokes(queryParams):
    pass

def lambda_handler(event: dict, context):
    api_event = APIEvent(event)
    # TODO implement
    handler_key = (api_event.path, api_event.httpMethod)
    handlers = {
        ('GET','/keystrokes'):get_keystrokes
        ('POST','/keystrokes'):post_keystrokes
    }
    logger.info(type(event))
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }