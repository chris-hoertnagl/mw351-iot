from sqlalchemy import create_engine
from sml_parser import parse
import pandas as pd

database="postgrest"
user='postgres',
password='password'
host='127.0.0.1'
port= '5432'

table_name = "EnergyManagement"

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:5432/{database}")

def write_to_db(data):
    parsed = parse(data)
    df = pd.DataFrame(parsed)
    df = df.fillna(method="bfill")
    df.iloc[[0],:]
    df.to_sql(table_name, engine, if_exists='append', index=False) 
