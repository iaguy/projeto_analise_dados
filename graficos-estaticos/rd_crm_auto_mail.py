import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Conexão com a base de dados
engine = create_engine('mysql://root:2303@host.docker.internal/app-bi')

# Query
query = "SELECT * FROM rd_mkt_auto_mail"

# Consulta ao banco de dados
df = pd.read_sql(query, engine)
df = df.drop(['created_at', 'updated_at', 'id'], axis=1)
df.dropna(inplace=True)


ax = df.rename(columns={
    'email_name': 'Nome do Email',
    'contacts_count': 'Contagem de Contatos',
    'email_delivered_count': 'Contagem de Emails Entregues',
    'email_opened_unique_count': 'Contagem de Emails Abertos Únicos',
    'email_clicked_unique_count': 'Contagem de Cliques em Emails Únicos',
    'email_dropped_count': 'Contagem de Emails Descartados',
    'email_unsubscribed_count': 'Contagem de Cancelamentos de Inscrição em Emails',
    'email_spam_reported_count': 'Contagem de Emails Marcados como Spam'
}).plot.bar(x='Nome do Email',
            y=[
                'Contagem de Contatos',
                'Contagem de Emails Entregues',
                'Contagem de Emails Abertos Únicos',
                'Contagem de Cliques em Emails Únicos',
                'Contagem de Emails Descartados',
                'Contagem de Cancelamentos de Inscrição em Emails',
                'Contagem de Emails Marcados como Spam'
            ],
            rot=0, figsize=(14, 8))

plt.xticks(rotation=0)

# Mostra o Grafico
plt.savefig('../graficos/rd_mkt_auto_mail.png')
plt.show()
