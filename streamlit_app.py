# streamlit_app.py

import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from psycopg2 import Error

try:
  connection = psycopg2.connect(user="vyzgmpqsxeucnv",
                                password="480540f32aa53c6f6850fee0add13f0ae8211a9aa7c98ed18fab701a829869df",
                                host="ec2-54-157-79-121.compute-1.amazonaws.com",
                                port="5432",
                                database="d1evcvc2sccml6")
  #Creamos el cursor para las operaciones de la base de datos
  cursor = connection.cursor()
  #Creamos una variable con el codigo sql que queremos que se ejecute
  select_query = '''SELECT *
FROM PUBLIC.accommodations a
JOIN PUBLIC.cities c ON c.id = a.id_city
ORDER BY a.id;'''
  #Executamos el comando
  cursor.execute(select_query)
  connection.commit()
  #con la funcion fetchall() podemos ver lo que retornaria la base de datos
  #df_accommodations = cursor.fetchall()
  #print(df_accommodations)
  #Esto crea un data frame con la información que pediste de la base de datos
  df = pd.read_sql_query(select_query,connection)
  # print("Result ", cursor.fetchall())

#Por si la conexion no fue exitosa
except (Exception, Error) as error:
  print("Error while connecting to PostgreSQL", error)
finally:
  if (connection):
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")





st.subheader('Raw data')
st.write(df)




