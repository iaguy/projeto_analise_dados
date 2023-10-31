import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Criando a conexão com o banco de dados
db_url = 'mysql://root:2303@host.docker.internal/app-bi'
engine = create_engine(db_url)
query = "SELECT * FROM blip_msg_data"

# Criando o dataframe
df = pd.read_sql_query(query, engine)
df = df.drop(['created_at', 'updated_at', 'id'], axis=1)

# Agrupando os dados por data e somando as mensagens enviadas e recebidas por dia
daily_msg_counts = df.groupby('date')[['msg_sent', 'msg_received']].sum()

# Criando o gráfico de barras para mensagens enviadas e recebidas por dia
ax = daily_msg_counts.plot(kind='bar', color=['blue', 'green'])
plt.title('Total de mensagens enviadas e recebidas por dia')
plt.xlabel('Data')
plt.ylabel('Quantidade de Mensagens')

# Rotacionar os rótulos do eixo x horizontalmente
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

# Convertendo a coluna 'date' para o tipo datetime
df['date'] = pd.to_datetime(df['date'])

# Calculando o valor total do mês
monthly_total = df.groupby(df['date'].dt.to_period('M')).agg({'msg_sent': 'sum', 'msg_received': 'sum'})

# Criar um segundo gráfico para o valor total do mês
ax2 = monthly_total.plot(kind='bar', color=['red', 'purple'])
plt.title('Total de mensagens enviadas e recebidas por mês')
plt.xlabel('Mês')
plt.ylabel('Quantidade de Mensagens')
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)

# Criando uma figura que contém os dois gráficos
fig, axes = plt.subplots(nrows=2, figsize=(12, 8))
daily_msg_counts.plot(kind='bar', color=['blue', 'green'], ax=axes[0], title='Total de mensagens enviadas e recebidas por dia', rot=0)
monthly_total.plot(kind='bar', color=['red', 'purple'], ax=axes[1], title='Total de mensagens enviadas e recebidas por mês', rot=0)


# Definindo espaçamento entre os dois gráficos
plt.tight_layout()

# Salvando a figura em uma imagem
plt.savefig('../graficos/blip_analise_msg.png')

plt.show()
