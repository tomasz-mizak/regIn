import os
from pprint import pprint
from cx_Oracle import init_oracle_client
from sqlalchemy import create_engine, text
import pandas as pd

# import Config class from config.py - enviroment variables helper
from config import Config
conf = Config()

# initial settins
DEBUG = conf.get('DEBUG')

# initialize oracle client
if (os.name == 'nt'):
    init_oracle_client(conf.get('INSTANT_CLIENT'))

# connection string - as easy to read format
# .env keys USERNAME, PASSWORD, DATABASE_IP, DATABASE_PORT, DATABASE_NAME
connection_string = "oracle+cx_oracle://%s:%s@%s:%s/?service_name=%s&encoding=UTF-8&nencoding=UTF-8" % (
    conf.get('USERNAME'), 
    conf.get('PASSWORD'), 
    conf.get('DATABASE_IP'), 
    conf.get('DATABASE_PORT'), 
    conf.get('DATABASE_NAME'))

# Print connection string if debug settings is enabled
if DEBUG:
    print(connection_string)

# define engine for connection
engine = create_engine(connection_string)

# TODO: handle timeout and other erros and send log to zi@wpia.uni.lodz.pl

# prepare connection
with engine.connect() as conn:
    # read sql from file to prepare as query
    with open('script.sql', 'r', encoding='cp856') as f:
        query = text(f.read())
        r = pd.read_sql(query, con=conn)
        print(f'Inserts todo: {r.shape[0]}')
        for i, r in r.iterrows():
            print(f"{i+1}) ----------------")
            ii = r[0].replace(';', '') # insert instruction
            if DEBUG:
                print(ii)
            try:
                conn.execute(ii)
                print("success!")
            except Exception as ex:
                if (DEBUG):
                    print(ex.args)
