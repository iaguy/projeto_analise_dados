import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from sqlalchemy import create_engine

# Criando a conexão com o banco de dados
db_url = 'mysql://root:2303@host.docker.internal/app-bi'
engine = create_engine(db_url)
query = "SELECT * FROM blip_msg_data"

# Criando o DataFrame
df = pd.read_sql_query(query, engine)
df = df.drop(['created_at', 'updated_at', 'id'], axis=1)

# Agrupando os dados por data e somando as mensagens enviadas e recebidas por dia
daily_msg_counts = df.groupby('date')[['msg_sent', 'msg_received']].sum().reset_index()

# Convertendo a coluna 'date' para uma string
daily_msg_counts['date'] = daily_msg_counts['date'].astype(str)

# Criando um gráfico de barras interativo para mensagens enviadas e recebidas por dia
fig = px.bar(daily_msg_counts, x='date', y=['msg_sent', 'msg_received'],
             labels={'date': 'Data', 'value': 'Quantidade de Mensagens'},
             title='Total de mensagens enviadas e recebidas por dia')
fig.update_xaxes(categoryorder='total ascending')

fig.show()

# Convertendo a coluna 'date' para datetime
df['date'] = pd.to_datetime(df['date'])

# Extrair ano e mês da coluna 'date' e criar uma nova coluna
df['year_month'] = df['date'].dt.to_period('M').dt.strftime('%Y-%m')

# Calculando o valor total por mês
monthly_total = df.groupby('year_month').agg({'msg_sent': 'sum', 'msg_received': 'sum'}).reset_index()

# Criando um gráfico de barras interativo para o valor total por mês
fig = px.bar(monthly_total, x='year_month', y=['msg_sent', 'msg_received'],
             labels={'year_month': 'Mês', 'value': 'Quantidade de Mensagens'},
             title='Total de mensagens enviadas e recebidas por mês')
fig.update_xaxes(type='category')  # Define o tipo do eixo x como categoria
fig.show()
