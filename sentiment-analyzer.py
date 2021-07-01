import streamlit as st
import pandas as pd
import numpy as np
import requests
from plotly.offline import iplot
import plotly.graph_objs as go
import plotly.express as px
from pandas.io.json import json_normalize
from streamlit.ScriptRunner import StopException, RerunException

fig = go.Figure()
st.write("""
# Sentiments Analysis App ✌

""")

st.write('Sentiment analysis is the interpretation and classification of emotions (positive, negative and neutral) within text data using text analysis techniques. Sentiment analysis tools allow businesses to identify customer sentiment toward products, brands or services in online feedback.')
st.set_option('deprecation.showfileUploaderEncoding', False)
st.sidebar.header('User Input(s)')
st.sidebar.subheader('Single Review Analysis')
single_review = st.sidebar.text_input('Enter single review below:')
st.sidebar.subheader('Mutiple Reviews Analysis')
uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
count_positive = 0
count_negative = 0
count_neutral = 0
if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
    for i in range(input_df.shape[0]):
        url = 'https://aisentimentsanalyzer.herokuapp.com/classify/?text='+str(input_df.iloc[i])
        r = requests.get(url)
        result = r.json()["text_sentiment"]
        if result=='positive':
            count_positive+=1
        elif result=='negative':
            count_negative+=1
        else:
            count_neutral+=1 

    x = ["Positive", "Negative", "Neutral"]
    y = [count_positive, count_negative, count_neutral]

    if count_positive>count_negative:
        st.write("""# Great Work there! Majority of people liked your product 😃""")
    elif count_negative>count_positive:
        st.write("""# Try improving your product! Majority of people didn't find your product upto the mark 😔""")
    else:
        st.write("""# Good Work there, but there's room for improvement! Majority of people have neutral reactions to your product 😶""")
        
    layout = go.Layout(
        title = 'Multiple Reviews Analysis',
        xaxis = dict(title = 'Category'),
        yaxis = dict(title = 'Number of reviews'),)
    
    fig.update_layout(dict1 = layout, overwrite = True)
    fig.add_trace(go.Bar(name = 'Multi Reviews', x = x, y = y))
    st.plotly_chart(fig, use_container_width=True)

elif single_review:
    url = 'https://aisentimentsanalyzer.herokuapp.com/classify/?text='+single_review
    r = requests.get(url)
    result = r.json()["text_sentiment"]
    if result=='positive':
        st.write("""# Great Work there! You got a Positive Review 😃""")
    elif result=='negative':
        st.write("""# Try improving your product! You got a Negative Review 😔""")
    else:
        st.write("""# Good Work there, but there's room for improvement! You got a Neutral Review 😶""")

else:
    st.write("# ⬅ Enter user input from the sidebar to see the nature of the review.")

st.sidebar.subheader("""Created with 💖 in India by """)
st.sidebar.image('logo.jpg', width = 300)

