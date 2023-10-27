import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Conecte-se ao banco de dados
db_url = 'mysql://root:2303@host.docker.internal/app-bi'
engine = create_engine(db_url)
query = "SELECT * FROM rd_crm_negociacoes"

df = pd.read_sql_query(query, engine)
df = df.drop(['created_at', 'updated_at', 'id'], axis=1)

# Agrupe os dados por 'deal_stage' e 'deal_lost_reason' e conte as ocorrências em cada grupo
grouped_data = df.groupby(['deal_stage', 'deal_lost_reason']).size().unstack(fill_value=0)

# Redefina o índice para compatibilidade com o Plotly
grouped_data = grouped_data.reset_index()

# Crie um gráfico de barras empilhadas dinâmico usando o Plotly
fig = px.bar(grouped_data,
             x='deal_stage',
             y=grouped_data.columns[1:],  # Exclua a coluna 'deal_stage'
             barmode='relative',
             title='Análise de Negociações por Estágio e Razão de Perda',
             labels={col: 'Razão de Perda' for col in grouped_data.columns[1:]},
             height=600,
             width=1000)

# Personalize o layout
fig.update_xaxes(title='Estágio de Negociação')
fig.update_yaxes(title='Quantidade de Empresas')
fig.update_layout(showlegend=True, legend_title_text='Razão de Perda')

# Salve o gráfico como um arquivo HTML
fig.write_html('../graficos/dinamicos/rd_crm_analise_negociacoes_interativo.html')

# Mostre o gráfico dinâmico do Plotly
fig.show()
