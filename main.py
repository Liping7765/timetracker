import requests
import streamlit as st 
import random


# response = requests.get('https://motivational-quote-api.herokuapp.com/quotes/random')

quotes = requests.get('https://type.fit/api/quotes').json()

quote = quotes[random.randint(0,len(quotes))]

st.markdown(f""" "{quote['text']}" """)

col1, col2, col3 = st.columns([3,6,2])
with col2:
    st.text(quote['author'])