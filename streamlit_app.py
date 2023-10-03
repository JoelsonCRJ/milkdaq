import numpy as np
import pandas as pd
import streamlit as st
import requests
import plotly.graph_objects as go

st.title('MILKDAQ')

qtd = 1000
read_temp = f"https://api.thingspeak.com/channels/2222170/fields/1.json?api_key=O2J4LQKR35J19LHP&timezone=America%2FSao_paulo&results={qtd}"
r = requests.get(read_temp)
data = r.json()['feeds']
r.close()
df_temp = pd.DataFrame.from_records(data).drop(['entry_id'], axis=1)

read_dist = f"https://api.thingspeak.com/channels/2222170/fields/2.json?api_key=O2J4LQKR35J19LHP&timezone=America%2FSao_paulo&results={qtd}"
r = requests.get(read_dist)
data = r.json()['feeds']
r.close()
df_dist = pd.DataFrame.from_records(data).drop(['entry_id'], axis=1)

fig_temp = go.Figure()
fig_temp.add_trace(go.Scatter(x=df_temp['created_at'], y=df_temp['field1']))
st.plotly_chart(fig_temp, use_container_width=True, theme=None)

fig_dist = go.Figure()
fig_dist.add_trace(go.Scatter(x=df_dist['created_at'], y=df_dist['field2']))
st.plotly_chart(fig_dist, use_container_width=True, theme=None)
