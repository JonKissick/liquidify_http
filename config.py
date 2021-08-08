from sqlalchemy import create_engine
import os
import boto3
import json
import configparser

if os.environ.get('AWS_KEY') == None:

    aws_id = os.getenv('AWS_KEY_IAM_DATA')
    aws_secret = os.getenv('AWS_SECRET_IAM_DATA')

    secrets_client = boto3.client('secretsmanager',
    aws_access_key_id=aws_id,
    aws_secret_access_key=aws_secret,
    region_name = 'ap-southeast-2')

    secret_arn = os.getenv('SECRET_ARN')
    auth_token = json.loads(secrets_client.get_secret_value(SecretId=secret_arn).get('SecretString'))

    rds_creds = json.loads(secrets_client.get_secret_value(SecretId=auth_token["HORSE_ARN"]).get('SecretString'))

    con = 'postgresql+psycopg2://' + str(rds_creds.get('username')) + ':' + str(rds_creds.get('password')) + '@' + str(rds_creds.get('host')) + '/' + str(rds_creds.get('engine'))


else:

    secrets_client = boto3.client('secretsmanager')

    secret_arn = os.getenv('SECRET_ARN')
    id_arn = os.getenv('ID_ARN')

    auth_token = json.loads(secrets_client.get_secret_value(SecretId=secret_arn).get('SecretString'))

    rds_creds = json.loads(secrets_client.get_secret_value(SecretId=auth_token["HORSE_ARN"]).get('SecretString'))

    IAM_token = json.loads(secrets_client.get_secret_value(SecretId=id_arn).get('SecretString'))
    aws_id = IAM_token.get('aws_key')
    aws_secret = IAM_token.get('aws_secret')


    con = 'postgresql+psycopg2://' + str(rds_creds.get('username')) + ':' + str(rds_creds.get('password')) + '@' + str(rds_creds.get('host')) + '/' + str(rds_creds.get('engine'))


engine = create_engine(con)

config = configparser.ConfigParser()
config['database'] = {'con': con}