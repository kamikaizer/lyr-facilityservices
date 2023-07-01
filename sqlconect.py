import sqlalchemy
import pandas as pd

url = 'mysql+mysqlconnector://root:root1234@localhost:3306/prueba'
engine = sqlalchemy.create_engine(url)

from sqlalchemy.sql import text
sql = '''
    
'''
with engine.connect() as conn:
    query = conn.execute(text(sql))         
df = pd.DataFrame(query.fetchall())

print(df)