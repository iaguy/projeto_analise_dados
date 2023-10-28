import pandas as pd
import sqlalchemy as sql
import matplotlib.pyplot as plt

# Conexão com o banco de dados
db_url = 'mysql://root:2303@host.docker.internal/app-bi'
engine = sql.create_engine(db_url)

# Query
query = "SELECT * FROM rd_mkt_analise_segmentacao"

# Importando os dados do banco de dados e criando o DataFrame
df = pd.read_sql_query(query, engine)

# Calculate a quantidade de empresas em 'segmentation_name'
quantidade = df['segmentation_name'].value_counts().reset_index()
quantidade.columns = ['Nome da Segmentação', 'Quantidade']

# Criação do gráfico
ax = quantidade.plot.bar(x='Nome da Segmentação', y='Quantidade', rot=26, figsize=(25, 10), width=0.5)

plt.xlabel('Nome da Segmentação')
plt.ylabel('Quantidade')
plt.title('Quantidade por Segmentação')

plt.show()
