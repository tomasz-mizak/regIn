import cx_Oracle as oracle
import sqlalchemy as alchemy
import pandas as pd

from config import Config

conf = Config()

oracle.init_oracle_client(conf.get('IC_PATH'))

class Context():

    def __init__(self, user=None, password=None):
        erro = False
        if user == None and password == None:
            try:
                user = conf.get('USER')
                password = conf.get('PASSWORD')
            except KeyError as e:
                erro = True
                print(f"W pliku środowiskowym nie znaleziono kluczy przynależnych do logowania.")

        if not erro:
            self.engine = alchemy.create_engine(f"oracle+cx_oracle://{user}:{password}@{conf.get('IPA')}:{conf.get('PORT')}/?service_name={conf.get('DBN')}&encoding=UTF-8&nencoding=UTF-8")

    def is_connection(self):
        try:
            with self.engine.connect() as connection:
                with connection.begin():
                    r1 = connection.execute("select * from tab")
        except alchemy.exc.SQLAlchemyError as e:
            self.exc = str(e)
            return False
        return True

    def query(self, sql_string):
        return pd.read_sql(sql_string, con=self.engine)

    def insert(self, sql_string):
        return self.engine.execute(sql_string)