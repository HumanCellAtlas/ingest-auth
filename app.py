import boto3
import json


client = boto3.client('secretsmanager')


def _retrieve_and_format_secrets(stage):
    response = client.get_secret_value(SecretId='dcp/ingest/{0}/secrets'.format(stage))
    secret_dict = json.loads(response['SecretString'])
    email_string = secret_dict["emails"]
    email_list = email_string.split(",")
    return email_list


def _is_user_allowed(stage, email):
    email_list = _retrieve_and_format_secrets(stage)
    email_family = email.split("@", 1)[1]
    if email in email_list or email_family in email_list:
        return ["wrangler"]
    else:
        return []


def handler(event, context):
    """Main function"""
    stage = event['requestContext']['stage']
    email = event['queryStringParameters']['email']
    roles = json.dumps(_is_user_allowed(stage, email))
    response = {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'application/json',
        },
        "body": roles
    }
    return response
