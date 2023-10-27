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

# Renomear as colunas
df = df.rename(columns={
    'conversion_count': 'Contagem de Conversões',
    'visits_count': 'Contagem de Visitas',
    'conversion_rate': 'Taxa de Conversão',
    'asset_identifier': 'Formulário de Conversão'
})

# Use 'asset_identifier' como índice
df.set_index('Formulário de Conversão', inplace=True)

# Cria um gráfico de barras interativo com Plotly
fig = px.bar(df.T, labels={'index': 'Formulário de Conversão'}, height=800, width=1200)

# Posicione a legenda ao lado do gráfico
fig.update_layout(
    legend=dict(
        orientation="v",  # Define a orientação da legenda para vertical
        yanchor="top",    # Ajusta o ponto de ancoragem vertical
        y=0.5,            # Define a posição vertical
        xanchor="right",  # Ajusta o ponto de ancoragem horizontal
        x=10            # Define a posição horizontal
    )
)

fig.write_html('graficos/dinamicos/rd_mkt_analise_conversao.html')
# Exiba o gráfico interativo
fig.show()
