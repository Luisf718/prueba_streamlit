# streamlit_app.py

import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
#     return psycopg2.connect(**st.secrets["postgres"])
     return psycopg2.connect(user="vyzgmpqsxeucnv",
                                password="480540f32aa53c6f6850fee0add13f0ae8211a9aa7c98ed18fab701a829869df",
                                host="ec2-54-157-79-121.compute-1.amazonaws.com",
                                port="5432",
                                database="d1evcvc2sccml6")

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        df = pd.read_sql_query(query,conn)
        return cur.fetchall()

# rows = run_query("SELECT * from PUBLIC.accommodations;")

# # Print results.
# for row in rows:
#     st.write(f"{row[0]} has a :{row[1]}:")



df = run_query("SELECT * FROM PUBLIC.accommodations a JOIN PUBLIC.cities c ON c.id = a.id_city ORDER BY a.id;")



st.subheader('Raw data')
st.write(df)




