import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
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

# Crie um gráfico de barras
ax = df.plot(kind='bar', rot=0, figsize=(17, 8))
ax.yaxis.set_major_locator(MultipleLocator(500))
plt.title('Análise de Conversão')
plt.ylabel('Quantidade')

# Posicione a legenda do lado de fora do gráfico
plt.legend(loc='upper left', title='Caminho dos Formularios')
plt.grid(True)

plt.savefig('graficos/rd_mkt_analise_conversao.png')
plt.show()
