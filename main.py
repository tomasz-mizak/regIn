from cx_Oracle import init_oracle_client
from sqlalchemy import create_engine, text

# import Config class from config.py - enviroment variables helper
from config import Config
conf = Config()

# initialize oracle client
init_oracle_client(conf.get('INSTANT_CLIENT_PATH'))

# connection string - as easy to read format
# .env keys USERNAME, PASSWORD, DATABASE_IP, DATABASE_PORT, DATABASE_NAME
connection_string = "oracle+cx_oracle://%s:%s@%s:%s/?service_name=%s&encoding=UTF-8&nencoding=UTF-8"
connection_string.format(
    conf.get('USERNAME'), 
    conf.get('PASSWORD'), 
    conf.get('DATABASE_IP'), 
    conf.get('DATABASE_PORT'), 
    conf.get('DATABASE_NAME'))

# define engine for connection
engine = create_engine(connection_string)

# prepare connection
with engine.connect() as conn:
    # read sql from file to prepare as query
    with open('script.sql') as f:
        query = text(f.read())
        conn.execute(query)
        # TODO: Check execute result and insert + commit this result to database.

