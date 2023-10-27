import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Conecta ao banco de dados
db_url = 'mysql://root:2303@host.docker.internal/app-bi'
engine = create_engine(db_url)

query = "SELECT * FROM blip_contato"
df = pd.read_sql_query(query, engine)
df = df.drop(['created_at', 'updated_at', 'id', 'lastMessageDate', 'sugestao', 'name'], axis=1)
df = df.dropna()

# Calcular a contagem para cada rótulo único na coluna 'source'
action_counts = df['source'].value_counts().reset_index()
action_counts.columns = ['source', 'count']

# Criar um gráfico dinâmico com Plotly
fig = px.pie(action_counts, names='source', values='count', title='Canais de Atendimentos')

# Adicionar o total de contatos como um anotação
total_contatos = len(df)
fig.add_annotation(
    text=f'Total de Contatos: {total_contatos}',
    x=0.9,
    y=0.9,
    showarrow=False,
    font=dict(size=12),
)

# Salvar o gráfico em um arquivo HTML
fig.write_html('../graficos/dinamicos/blip-contato.html')

# Mostrar o gráfico
fig.show()
