import os, pandas
from tqdm import tqdm
from cx_Oracle import init_oracle_client
from sqlalchemy import create_engine, text
from datetime import datetime
from string import Template
from pprint import pprint

# Import Config class from config.py - enviroment variables helper
from config import Config
conf = Config()

# Import MailService class - mail sending service
from mail_service import MailService

# Initial settins
DEBUG = conf.get('DEBUG')

# Setup mail server
mail_service = MailService(login=conf.get('MAIL_LOGIN'), password=conf.get('MAIL_PASSWORD'))
MONIT_TARGET = conf.get('MAIL_MONITS_TARGET')

# Mail patterns
from mail_patterns import SUCCESS_PATTERN, EXCEPTION_PATTERN, NOTHING_TODO

# Initialize InstantClient on NT systems
if (os.name == 'nt'):
    init_oracle_client(conf.get('INSTANT_CLIENT'))

# Connection string - as easy to read format
# .env keys USERNAME, PASSWORD, DATABASE_IP, DATABASE_PORT, DATABASE_NAME
connection_string = "oracle+cx_oracle://%s:%s@%s:%s/?service_name=%s&encoding=UTF-8&nencoding=UTF-8" % (
    conf.get('DATABASE_USERNAME'), 
    conf.get('DATABASE_PASSWORD'), 
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

# TODO: Add exception handling to script reading and executing.

# TODO: Builder of persons list
def not_exist(list, el):
    for e in list:
        if e == el:
            return False
    return True

def build_persons_list(persons):
    # pore over by target class
    classes = []
    for c in persons:
        if not_exist(classes, c['targetClass']):
            classes.append(c['targetClass'])
    string = ""
    for c in classes:
        string = string + f"<b>Class: {c}</b>"
        for p in persons:
            if p['targetClass'] == c:
                erro = ""
                if not p['insertException']:
                    erro = "<span style='color: green'>SUCCESS!</span>"
                else:
                    erro = "<span style='color: red'>FAIL!</span>"
                string = string + f"<li>[{p['index']}] {p['firstName']} {p['lastName']} [{erro}]</li>"
    return string
        

# Prepare connection
with engine.connect() as conn:
    # Read instructions from file
    with open('script.sql', 'r', encoding='cp856') as f:
        query = text(f.read())
        # Use pandas to fetch data
        r = pandas.read_sql(query, con=conn)
        # Save lenght of result
        possible_inserts = r.shape[0]
        if (possible_inserts > 0):
            # Display possible inserts
            print(f'Inserts todo: {possible_inserts}')
            # Initialize bpar
            pbar = tqdm(total=possible_inserts)
            # For exception handling
            ex_counter = 0
            ex_handler = []
            successful = 0
            # For handling persons
            persons = []
            select_person_sql = "select o.imie, o.nazwisko, s.indeks from dz_osoby o, dz_studenci s where o.id = {os_id} and s.os_id = o.id"
            # Insert inserts :)
            for i, r in r.iterrows():
                # insert instruction, remove semi-colon charcter from instruction
                ii = r[0].replace(';', '')
                # Cut os_id from insert
                os_id = int(ii[int(ii.find(",'")):len(ii)].replace(",'", '').replace("')", ''))
                target_class = ii[int(ii.find("('"))+1:ii.find("',")].replace("'", '')
                # Fetch and save to persons
                r2 = pandas.read_sql(select_person_sql.format(os_id=os_id), con=conn)
                insert_exception = False # variable for status of insert
                try:
                    conn.execute(ii)
                    pbar.update(1)
                    successful = successful + 1
                except Exception as ex:
                    ex_counter = ex_counter + 1
                    ex_handler.append(ex.args)
                    insert_exception = True
                    if (DEBUG):
                        print(ex.args)
                person_dict = {
                    'firstName': r2['imie'][0],
                    'lastName': r2['nazwisko'][0],
                    'index': r2['indeks'][0],
                    'targetClass': target_class,
                    'insertException': insert_exception
                }
                persons.append(person_dict)
            # Close pbar
            pbar.close()
            # Defina variable for pattern
            msg = None
            # Format pattern
            title = '[regIn] Successful import'
            # Use builder to get persons list
            html_persons = "<i>No persons found</i>"
            if len(persons)>0:
                html_persons = build_persons_list(persons)
            # Any exceptions?
            if (ex_counter > 0):
                title = '[regIn] Detected problems'
                html_exceptions = ""
                for i, r in enumerate(ex_handler, start=1):
                    html_exceptions = html_exceptions + f"<li>{r}</li>"
                msg = EXCEPTION_PATTERN.substitute(date=datetime.now(), imports=possible_inserts, successful=successful, exceptions=ex_counter, exceptions_list=html_exceptions, persons=html_persons)
            else:
                msg = SUCCESS_PATTERN.substitute(date=datetime.now(), imports=possible_inserts, successful=successful, exceptions=ex_counter, persons=html_persons)
            # Try to send monit
            mail_service.send(to=MONIT_TARGET, subject=title, msg=msg)
        else:
            mail_service.send(to=MONIT_TARGET, subject='[regIn] Nothing todo', msg=NOTHING_TODO.substitute(date=datetime.now()))