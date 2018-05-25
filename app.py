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
        return "Authorized"
    else:
        return "Denied"


def handler(event, context):
    """Main function"""
    stage = event['requestContext']['stage']
    print(stage)
    email = event['queryStringParameters']['email']
    print(email)
    access_status = _is_user_allowed(stage, email)
    print(access_status)
    response = {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'text/html; charset=utf-8',
        },
        "body": access_status
    }
    return response
