import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Conecta ao banco de dados
db_url = 'mysql://root:2303@host.docker.internal/app-bi'
engine = create_engine(db_url)

query = "SELECT * FROM rd_mkt_analise_conversao"
df = pd.read_sql_query(query, engine)
df = df.drop(['asset_created_at', 'asset_updated_at', 'id'], axis=1)
df.dropna(inplace=True)

# Renomear as colunas antes da transposição
df = df.rename(columns={
    'conversion_count': 'Contagem de Conversões',
    'visits_count': 'Contagem de Visitas',
    'conversion_rate': 'Taxa de Conversão'
})

# Use 'asset_identifier' como índice
df.set_index('asset_identifier', inplace=True)

# Transponha o DataFrame para que as colunas sejam usadas no eixo x
df = df.T

# Crie um gráfico de barras interativo com Plotly Express
fig = px.bar(df, barmode='group')
fig.update_xaxes(categoryorder='total ascending')
fig.update_layout(
    title='Análise de Conversão',
    xaxis_title='Caminho dos Formulários',
    yaxis_title='Quantidade',
)
fig.write_html('../graficos/dinamicos/rd_mkt_analise_conversao_interativo.html')
fig.show()
