import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Conecta ao banco de dados
db_url = 'mysql://root:2303@host.docker.internal/app-bi'
engine = create_engine(db_url)
query = "SELECT * FROM blip_eventos"

df = pd.read_sql_query(query, engine)

# Converta as strings "NaN" na coluna 'action' para NaN (valor nulo)
df['action'] = df['action'].apply(lambda x: float('nan') if x == 'NaN' else x)

# Agora,pode usar dropna() para remover as linhas com valores NaN
df = df.dropna()
df = df.drop(['created_at', 'updated_at', 'id', 'storageDate'], axis=1)

action_counts = df['action'].value_counts()
plt.figure(figsize=(8, 6))
action_counts.plot(kind='bar', edgecolor='k')
plt.title('Nota de Atendimento')
plt.xlabel('Valores')
plt.ylabel('Contagem')

plt.savefig('graficos/blip-eventos.png')
plt.show()
