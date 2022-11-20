from database.database import Database
import streamlit as st
from datetime import datetime as dt
import time 
import requests

# convert data to show dates 
def show_date(time_in_secs):
    return time.strftime("%m/%d/%Y", time.localtime(int(time_in_secs)))


def show_time(start_time, end_time):

    start = dt.fromtimestamp(int(start_time))
    end = dt.fromtimestamp(int(end_time))
    return str(end - start)

def cal_time(start, end, cat):
    t1 = time.localtime(int(start))
    t2 = time.localtime(int(end))

    return time.mktime(t2) - time.mktime(t1) if cat != "WORKOUT" else (time.mktime(t2) - time.mktime(t1)) * 2

# def metric():
#     # retrieve data 
#     db = Database()
#     rows = db.get_all()

#     left_time= 80 * 60 * 60 
#     prev_catup = 0
#     total_catup = 0
#     for row in rows:
#         id, cat, start, end = row
#         prev_catup = total_catup
#         total_catup += end - start if cat != "WORKOUT" else (end - start) * 2

#     col1, col2 = st.columns(2)

#     with col1:
#         value, delta = str(show_time(total_catup, left_time)), str(int(total_catup - prev_catup)) + " secs"
#         st.metric(label="Time to catch up...", value=value, delta=delta)


import pandas as pd
import numpy as np

# import data scource as rows 
db = Database()
rows = db.get_all()

df = pd.DataFrame(
    np.array(rows),
    columns=['id', 'catagory', 'start_time','end_time','time_stamp'])

df["date"] = df.apply(lambda row: show_date(row.start_time), axis = 1)
df['duration'] = df.apply(lambda row: show_time(row.start_time, row.end_time), axis = 1)
df['duration_in_sec'] = df.apply(lambda row: cal_time(row.start_time, row.end_time, row.catagory), axis = 1)

# df_withonly_dates = df.loc[:, ~df.columns.isin(['start_time', 'end_time'])]
# filter data for different graphs 
data_by_date = df[["date","duration_in_sec"]]
data_by_cat = df[["date", 'catagory','duration_in_sec']]

# layout 

col1, col2 = st.columns(2)

with col1:
    st.line_chart(data_by_date.groupby("date").sum())

with col2:
    st.bar_chart(data_by_cat.groupby('catagory').sum())


with st.sidebar:
    left_time= 80 * 60 * 60 
    prev_catup = 0
    total_catup = 0
    for row in rows:
        id, cat, start, end, _ = row
        prev_catup = total_catup
        total_catup += end - start if cat != "WORKOUT" else (end - start) * 2


    value, delta = str(show_time(total_catup, left_time)), str(int(total_catup - prev_catup)) + " secs"
    st.metric(label="Time to catch up...", value=value, delta=delta)



