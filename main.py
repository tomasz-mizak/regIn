import os, pandas, tqdm
from cx_Oracle import init_oracle_client
from sqlalchemy import create_engine, text

# Import Config class from config.py - enviroment variables helper
from config import Config
conf = Config()

# Initial settins
DEBUG = conf.get('DEBUG')

# Initialize InstantClient on NT systems
if (os.name == 'nt'):
    init_oracle_client(conf.get('INSTANT_CLIENT'))

# Connection string - as easy to read format
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

# Define engine for connection
engine = create_engine(connection_string)

# TODO: handle timeout and other erros and send log to zi@wpia.uni.lodz.pl

# pbar definition
pbar = None

# Prepare connection
with engine.connect() as conn:
    # Read instructions from file
    with open('script.sql', 'r', encoding='cp856') as f:
        query = text(f.read())
        # Use pandas to fetch data
        r = pandas.read_sql(query, con=conn)
        # Initialize bpar
        pbar = tqdm(total=r.shape[0])
        # Display possible inserts
        print(f'Inserts todo: {r.shape[0]}')

        for i, r in r.iterrows():
            ii = r[0].replace(';', '') # insert instruction, remove semi-colon charcter from instruction
            try:
                #conn.execute(ii)
                pbar.update(1)
            except Exception as ex:
                if (DEBUG):
                    print(ex.args)

        # Close pbar
        pbar.close()