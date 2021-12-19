import os
'''
necessary environment variables (also in the right format for .env):
AWS_ACCESS_KEY_ID=EXAMPLEEXAMPLEEXAMPLE
AWS_SECRET_ACCESS_KEY=EXAMPLEEXAMPLEEXAMPLE
AWS_DEFAULT_REGION=us-north-69
'''
try:
    with open(".env") as f:
        for line in f:
            key, val = line.strip().split("=")
            os.environ[key]=val
except FileNotFoundError:
    pass