import pandas as pd
import plotly.express as px
import sqlalchemy

# Conectar ao banco de dados
db_url = 'mysql://root:2303@host.docker.internal/app-bi'
engine = sqlalchemy.create_engine(db_url)

query = "SELECT * FROM rd_mkt_analise_mail"
df = pd.read_sql_query(query, engine)
df = df.drop(['created_at', 'updated_at', 'id', 'send_at'], axis=1)
df = df.dropna()

# Renomear as colunas para serem mais legíveis na legenda do gráfico
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

# Criar um gráfico dinâmico com Plotly Express
fig = px.bar(df, x='campaign_name', y=list(novo_nome_colunas.values()),
             title='Emails Enviados', labels={'campaign_name': 'Campanha', 'value': 'Quantidade'})
fig.update_xaxes(tickangle=0)  # Definir o ângulo dos rótulos no eixo x

# salvar o gráfico em um arquivo html
fig.write_html('../graficos/dinamicos/rd_mkt_analise_mail_interativo.html')

# Exibir o gráfico interativo
fig.show()
