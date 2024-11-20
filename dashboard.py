from datetime import datetime
import datetime as dt
import json
import pandas as pd
import streamlit as st
import streamlit as st
import numpy as np

tickers = ['TSLA', 'NVDA']
ticks = pd.read_csv('stock_ticks.csv')

displayed_stock = st.sidebar.selectbox('Select a stock', tuple(tickers))

today = dt.date.today()
before = today - dt.timedelta(days=1)
start_date = st.sidebar.date_input('Start date', before)
end_date = st.sidebar.date_input('End date', today)
if start_date < end_date:
    st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    st.sidebar.error('Error: End date must fall after start date.')

# Plot High, Low, Open, Close
low_point = np.min(ticks[ticks["Ticker"]==displayed_stock]["Close"])
high_point = np.max(ticks[ticks["Ticker"]==displayed_stock]["High"])
st.write('Stock Data')
st.line_chart(data=ticks[ticks["Ticker"]==displayed_stock], x="Timestamp", y=["High", "Low", "Open", "Close"], )
st.line_chart(data=ticks[ticks["Ticker"]==displayed_stock], x="Timestamp", y=["Volume"], )