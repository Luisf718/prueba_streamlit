# streamlit_app.py

import streamlit as st
import psycopg2

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

connection = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results

rows = run_query(''' SELECT * 
  FROM PUBLIC.landlords
  WHERE id > 500;''')

# Print results.
for row in rows:
    st.write(row)