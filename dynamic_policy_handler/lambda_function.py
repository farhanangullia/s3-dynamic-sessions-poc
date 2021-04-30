""" This lambda function acts as a policy handler 
    to return temporary credentials with appropriate
    session permissions
"""
import json
import boto3
import os

AWS_REGION = os.environ['AWS_REGION']
ROLE_ARN = os.environ['ROLE_ARN']

# To be retrieved dynamically/passed in when calling the API for this function
USER = os.environ['USER']

# To be passed in from calling function/service [currently hardcoded in env variables for POC]. Optional if you permit the role attached to this function to assume the target role
ACCESS_KEY = os.environ['ACCESS_KEY']
SECRET_KEY = os.environ['SECRET_KEY']


def get_session_policy_document():  # Ideally, this IAM policy should be fetched from a datastore or passed in as a payload when calling the API for this function
    session_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "s3:GetObject",
                "Resource": [
                    "arn:aws:s3:::<BUCKET_NAME>/beverages/hot/*",
                    "arn:aws:s3:::<BUCKET_NAME>/fruits/*"
                ]
            }
        ]
    }
    return session_policy


def get_client(service, aws_access_key_id=None, aws_secret_access_key=None):
    return boto3.client(service, region_name=AWS_REGION, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)


def get_external_id(name):
    response = get_client("ssm").get_parameter(
        Name=name)
    return response["Parameter"]["Value"]


def assume_role(role_arn, role_session_name, policy, user, external_id):
    return get_client("sts", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY).assume_role(
        RoleArn=role_arn,
        RoleSessionName=role_session_name,
        Policy=policy,
        ExternalId=external_id
    )["Credentials"]


def lambda_handler(event, context):
    print("assuming role with inline session policy...")
    credentials = assume_role(ROLE_ARN, "S3SessionRole-{}".format(USER),
                              json.dumps(get_session_policy_document()), USER, get_external_id('ExternalId'))
    print(credentials)
    return {
        'statusCode': 200,
        'body': json.dumps(credentials, default=str)
    }
