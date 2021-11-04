from sqlalchemy import create_engine
from sml_parser import parse
import pandas as pd

database="mydb"
user='postgres',
password='iot'
host='127.0.0.1'
port= '5432'

table_name = "EnergyManagement"

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:5432/{database}")

df = pd.read_sql(f"select * from \"{table_name}\"", engine.connect())

print(df)
