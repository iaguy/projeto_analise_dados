import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from matplotlib.ticker import MultipleLocator

# Conecta ao banco de dados
db_url = 'mysql://root:2303@host.docker.internal/app-bi'
engine = create_engine(db_url)
query = "SELECT * FROM rd_crm_negociacoes"

df = pd.read_sql_query(query, engine)
df = df.drop(['created_at', 'updated_at', 'id'], axis=1)

# Agrupa os dados por 'deal_stage' e 'deal_lost_reason' e conta o número de ocorrências em cada grupo
grouped_data = df.groupby(['deal_stage', 'deal_lost_reason']).size().unstack(fill_value=0)

# Cria um gráfico de barras empilhadas
plt.figure(figsize=(12, 6))
ax = grouped_data.plot(kind='bar', figsize=(12, 6))
plt.title('Análise de Negociações por Estágio e Razão de Perda')
plt.xlabel('Estágio de Negociação')
plt.ylabel('Quantidade de Empresas')
plt.xticks(rotation=0)
plt.grid(True)

# Define os intervalos desejados no eixo y (de 5 em 5)
ax.yaxis.set_major_locator(MultipleLocator(5))

# Define a legenda
handles, labels = ax.get_legend_handles_labels()
plt.legend(handles, labels, title='Razão de Perda')

plt.savefig('../graficos/rd_crm_negociacoes_combined.png')
plt.show()
