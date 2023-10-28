import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Conecta ao banco de dados
db_url = 'mysql://root:2303@host.docker.internal/app-bi'

engine = create_engine(db_url)
query = "SELECT * FROM rd_mkt_auto_mail"

# Criação do DataFrame
df = pd.read_sql_query(query, engine)

df = df.drop(['created_at', 'updated_at', 'id'], axis=1)

print(df)