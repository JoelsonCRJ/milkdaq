import numpy as np
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title='Milkdaq',
    layout='wide'
)
st_autorefresh(interval=1*60*1000, key='dataframerefresh')

janela = 24  # horas
qtd_pontos_hora = 12  # um ponto a cada 5min

qtd = int(janela*qtd_pontos_hora)
read_temp = f"https://api.thingspeak.com/channels/2222170/fields/1.json?api_key=O2J4LQKR35J19LHP&timezone=America%2FSao_Paulo&results={qtd}"
r = requests.get(read_temp)
data = r.json()['feeds']
r.close()
df_temp = pd.DataFrame.from_records(data).drop(['entry_id'], axis=1)
df_temp['created_at'] = pd.to_datetime(df_temp['created_at'])
df_temp['field1'] = round(df_temp['field1'].astype(float), 2)

read_dist = f"https://api.thingspeak.com/channels/2222170/fields/2.json?api_key=O2J4LQKR35J19LHP&timezone=America%2FSao_Paulo&results={qtd}"
r = requests.get(read_dist)
data = r.json()['feeds']
r.close()
df_dist = pd.DataFrame.from_records(data).drop(['entry_id'], axis=1)
df_dist['created_at'] = pd.to_datetime(df_dist['created_at'])
df_dist['field2'] = df_dist['field2'].astype(float)
df_dist['nivel'] = round((1.05 - (df_dist['field2']/1000)), 3)

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.075)

fig.add_trace(go.Scatter(
    x=df_temp['created_at'], y=df_temp['field1'], name='Temperatura', mode='lines+markers'), row=1, col=1)
fig.add_trace(go.Scatter(
    x=df_dist['created_at'], y=df_dist['nivel'], name='Nível', mode='lines+markers'), row=2, col=1)

fig.layout.yaxis.range = [0, 30]
fig.layout.xaxis.range = [df_temp['created_at'].max(
) - pd.Timedelta(12, 'h'), df_temp['created_at'].max()]
fig.layout.yaxis.title = 'Temperatura do Leite (°C)'
fig.layout.yaxis2.range = [0, 1]
fig.layout.yaxis2.title = 'Nível do Tanque (m)'

fig.update_layout(autosize=False,
                  width=1200,
                  height=600,
                  legend={'orientation': 'h', 'yanchor': 'bottom',
                          'y': 1.02, 'xanchor': 'center', 'x': 0.5},
                  hovermode='x unified',
                  title_text='Monitoramento do Tanque de Leite',
                  title={'font': {'size': 30}},
                  font={'size': 18}
                  )
st.plotly_chart(fig, use_container_width=True, theme=None)
