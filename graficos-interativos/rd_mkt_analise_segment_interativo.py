import pandas as pd
import sqlalchemy as sql
import plotly.express as px

# Conexão com o banco de dados
db_url = 'mysql://root:2303@host.docker.internal/app-bi'
engine = sql.create_engine(db_url)

# Query
query = "SELECT * FROM rd_mkt_analise_segmentacao"

# Importando os dados do banco de dados e criando o DataFrame
df = pd.read_sql_query(query, engine)

# Caucalando a quantidade de empresas em 'segmentation_name'
quantidade = df['segmentation_name'].value_counts().reset_index()
quantidade.columns = ['Nome da Segmentação', 'Quantidade']

# Criação do gráfico interativo usando Plotly Express
fig = px.bar(quantidade, x='Nome da Segmentação', y='Quantidade', title='Quantidade de Empresas por Segmentação')
fig.update_xaxes(tickangle=26)

# Salva o gráfico em um arquivo HTML
fig.write_html('../graficos/dinamicos/rd-mkt-analise-segmentacao.html')
# Exibir o gráfico
fig.show()
