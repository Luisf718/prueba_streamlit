# streamlit_app.py

import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

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
    connection = init_connection()
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
        df = pd.read_sql_query(query,connection)
        cursor.close()
        connection.close()
        return df

cursor = connection.cursor()
try:
  #Creamos el cursor para las operaciones de la base de datos
#   cursor = connection.cursor()
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
 
df = run_query("SELECT * FROM PUBLIC.accommodations a JOIN PUBLIC.cities c ON c.id = a.id_city ORDER BY a.id;")

#Agrupamos por el nombre de las ciudades y sumamos las visitas que han tenido por toda la ciudad
df_groupby_ciudad_visitas = df.groupby(by='name')['number_of_visits'].agg([sum, min, max])
#Reseteamos los index para que 'name' se ponga como columna y no se quede en indice
df_groupby_ciudad_visitas = df_groupby_ciudad_visitas.reset_index()
#Ordenamos el df por el 'sum' para que esten ordenados del que tiene mas visitas al que tiene menos
df_groupby_ciudad_visitas = df_groupby_ciudad_visitas.sort_values('sum', ascending=False)

x = df_groupby_ciudad_visitas['name'][:5]
y = df_groupby_ciudad_visitas['sum'][:5]
plt.bar(x, y, color='red')
plt.xlabel('Ciudad')
plt.ylabel('Visitas')
plt.title('TOP 5 visitas por ciudad')
st.write("Hola mundo")
st.write(plt.show())



# # Print results.
# for row in rows:
#     st.write(row)
