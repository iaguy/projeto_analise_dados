import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Conexão com a base de dados
engine = create_engine('mysql://root:2303@host.docker.internal/app-bi')

# Query
query = "SELECT * FROM rd_mkt_auto_mail"

# Consulta ao banco de dados
df = pd.read_sql(query, engine)
df = df.drop(['created_at', 'updated_at', 'id'], axis=1)
df.dropna(inplace=True)

# Renomear as colunas para uso no Plotly
df = df.rename(columns={
    'email_name': 'Nome do Email',
    'contacts_count': 'Contagem de Contatos',
    'email_delivered_count': 'Contagem de Emails Entregues',
    'email_opened_unique_count': 'Contagem de Emails Abertos Únicos',
    'email_clicked_unique_count': 'Contagem de Cliques em Emails Únicos',
    'email_dropped_count': 'Contagem de Emails Descartados',
    'email_unsubscribed_count': 'Contagem de Cancelamentos de Inscrição em Emails',
    'email_spam_reported_count': 'Contagem de Emails Marcados como Spam'
})

# Crie um gráfico de barras Plotly
fig = px.bar(df,
             x='Nome do Email',
             y=['Contagem de Contatos', 'Contagem de Emails Entregues', 'Contagem de Emails Abertos Únicos',
                'Contagem de Cliques em Emails Únicos', 'Contagem de Emails Descartados',
                'Contagem de Cancelamentos de Inscrição em Emails', 'Contagem de Emails Marcados como Spam'],
             title="Estatísticas de Email Marketing",
             labels={'value': 'Contagem'},
             height=700,
             width=1200)

# Salva o gráfico em arquivo HTML
fig.write_html('../graficos/dinamicos/rd_crm_auto_mail.html')
# Mostra o gráfico Plotly
fig.show()
