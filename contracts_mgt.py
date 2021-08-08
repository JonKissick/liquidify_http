import psycopg2
import psycopg2.extras
import pandas as pd
import datetime as dt
from flask_login import logout_user, current_user
import os
import boto3
import json

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

    con = psycopg2.connect(dbname=str(rds_creds.get('engine')),

                           user=str(rds_creds.get('username')),

                           password=str(rds_creds.get('password')),

                           host=str(rds_creds.get('host')))

else:

    secrets_client = boto3.client('secretsmanager')

    secret_arn = os.getenv('SECRET_ARN')
    id_arn = os.getenv('ID_ARN')

    auth_token = json.loads(secrets_client.get_secret_value(SecretId=secret_arn).get('SecretString'))

    rds_creds = json.loads(secrets_client.get_secret_value(SecretId=auth_token["HORSE_ARN"]).get('SecretString'))

    IAM_token = json.loads(secrets_client.get_secret_value(SecretId=id_arn).get('SecretString'))
    aws_id = IAM_token.get('aws_key')
    aws_secret = IAM_token.get('aws_secret')


    con = psycopg2.connect(dbname=str(rds_creds.get('engine')),

                           user=str(rds_creds.get('username')),

                           password=str(rds_creds.get('password')),

                           host=str(rds_creds.get('host')))



def add_email(email):

    email_timestamp = dt.datetime.now()  ##### This wil run locally but will need to be update for UTC/Timezone

    column_names = ['email','email_timestamp']
    insert_frame = pd.DataFrame([[email,email_timestamp]],columns=column_names)

    cursor = con.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS liquidify.emails (email TEXT, email_timestamp TIMESTAMP)''')

    con.commit()

    def upload_data(data):
        psycopg2.extras.execute_batch(cursor,
                                      "INSERT INTO liquidify.emails (email,email_timestamp) VALUES(%s,%s)",
                                      (data))
    ##############

    b = ([tuple(x) for x in insert_frame.values])
    upload_data(b)
    con.commit()

#######################

def show_contracts():
    def get_rs_conn():
        return psycopg2.connect(dbname=str(rds_creds.get('engine')),

                           user=str(rds_creds.get('username')),

                           password=str(rds_creds.get('password')),

                           host=str(rds_creds.get('host')))

    def query_df(sql):
        with get_rs_conn() as conn:
            with conn.cursor() as cur:

                cur.execute(sql)
                result_set = cur.fetchall()
                colnames = [desc.name for desc in cur.description]
                df = pd.DataFrame.from_records(result_set, columns=colnames)

        return df

    def get_all_contracts():

        stats = query_df(f'''
        select * from public.contracts
        ''')

        return stats

    contracts = get_all_contracts()
    contracts = contracts.to_dict('records')
    return contracts


def get_contracts_df():
    def get_rs_conn():
        return psycopg2.connect(dbname=str(rds_creds.get('engine')),

                           user=str(rds_creds.get('username')),

                           password=str(rds_creds.get('password')),

                           host=str(rds_creds.get('host')))

    def query_df(sql):
        with get_rs_conn() as conn:
            with conn.cursor() as cur:

                cur.execute(sql)
                result_set = cur.fetchall()
                colnames = [desc.name for desc in cur.description]
                df = pd.DataFrame.from_records(result_set, columns=colnames)

        return df

    def get_all_contracts():

        stats = query_df(f'''
        select * from public.contracts
        ''')

        return stats

    contracts = get_all_contracts()

    return contracts
