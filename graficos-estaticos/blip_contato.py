import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Conecta ao banco de dados
db_url = 'mysql://root:2303@host.docker.internal/app-bi'
engine = create_engine(db_url)

query = "SELECT * FROM blip_contato"
df = pd.read_sql_query(query, engine)
df = df.drop(['created_at', 'updated_at', 'id', 'lastMessageDate', 'sugestao', 'name'], axis=1)
df = df.dropna()

# Calcular a contagem para cada rótulo único na coluna 'source'
action_counts = df['source'].value_counts()

labels = action_counts.index
sizes = action_counts.values

plt.figure(figsize=(8, 8))
explode = (0.05, 0.1, 0.4, 0.85)
label_props = {'rotation': 'horizontal', 'verticalalignment': 'center_baseline', 'horizontalalignment': 'left'}
plt.pie(
    sizes,
    labels=labels,
    autopct='%1.1f%%',
    startangle=140,
    explode=explode,
    textprops=label_props,
    pctdistance=0.8,
    labeldistance=1.1
)
plt.title('Canais de Atendimentos')

# Adiciona o total de contatos como uma anotação
total_contatos = len(df)
plt.annotate(f'Total de Contatos: {total_contatos}', (0.1, 0.1), fontsize=12, color='black',
             xycoords='axes fraction', textcoords='axes fraction', va='center', ha='center')


plt.savefig('../graficos/blip-contato.png')
plt.show()
