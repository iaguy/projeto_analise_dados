import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from sqlalchemy import create_engine

db_url = 'mysql://root:2303@host.docker.internal/app-bi'
engine = create_engine(db_url)

query = "SELECT * FROM rd_mkt_analise_mail"
df = pd.read_sql_query(query, engine)
df = df.drop(['created_at', 'updated_at', 'id', 'send_at'], axis=1)
df = df.dropna()

# Renomear as colunas para serem mais legíveis na legenda do grafico
novo_nome_colunas = {
    'email_dropped_count': 'Quantidade de E-mails Descartados',
    'email_delivered_count': 'Quantidade de E-mails Entregues',
    'email_bounced_count': 'Quantidade de E-mails Devolvidos',
    'email_opened_count': 'Quantidade de E-mails Abertos',
    'email_clicked_count': 'Quantidade de E-mails Clicados',
    'email_spam_reported_rate': 'Taxa de E-mails Sinalizados como Spam',
    'contacts_count': 'Número de Contatos'
}
df = df.rename(columns=novo_nome_colunas)

# Montando o gráfico
ax = df.plot.bar(x='campaign_name',
                 y=list(novo_nome_colunas.values()),
                 rot=0,
                 figsize=(10, 5))
# Define o intervalo desejado no eixo y (de 500 em 500)
ax.yaxis.set_major_locator(MultipleLocator(500))
plt.title('Emails Enviados')
plt.xlabel('Campanha')
plt.ylabel('Quantidade')
plt.legend(loc='upper left')
plt.grid(True)
plt.savefig('../graficos/rd_mkt_analise_mail.png')
plt.show()
