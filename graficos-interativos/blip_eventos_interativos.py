import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Conecta-se ao banco de dados
db_url = 'mysql://root:2303@host.docker.internal/app-bi'
engine = create_engine(db_url)
query = "SELECT * FROM blip_eventos"

df = pd.read_sql_query(query, engine)

# Converta as strings "NaN" na coluna 'action' para NaN (valor nulo)
df['action'] = df['action'].apply(lambda x: float('nan') if x == 'NaN' else x)

# Agora, pode usar dropna() para remover as linhas com valores NaN
df = df.dropna()
df = df.drop(['created_at', 'updated_at', 'id', 'storageDate'], axis=1)

action_counts = df['action'].value_counts().reset_index()
action_counts.columns = ['Valores', 'Contagem']

# Crie um gráfico de barras dinâmico com o Plotly
fig = px.bar(action_counts, x='Valores', y='Contagem', title='Nota de Atendimento')
fig.update_xaxes(title_text='Valores')
fig.update_yaxes(title_text='Contagem')

# Salve o gráfico dinâmico do Plotly em HTML
fig.write_html('../graficos/dinamicos/blip-eventos.html')

# Mostre o gráfico dinâmico do Plotly
fig.show()
