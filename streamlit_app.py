# streamlit_app.py

import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from psycopg2 import Error
import numpy as np


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
JOIN PUBLIC.cities c ON c.city_id = a.id_city
ORDER BY a.id;'''
#Executamos el comando
cursor.execute(select_query)
connection.commit()
#con la funcion fetchall() podemos ver lo que retornaria la base de datos
#df_accommodations = cursor.fetchall()
#print(df_accommodations)
#Esto crea un data frame con la información que pediste de la base de datos
df = pd.read_sql_query(select_query,connection)
# st.write("Result: ", cursor.fetchall())


if (connection):
  cursor.close()
  connection.close()
  print("PostgreSQL connection is closed")




# Con esto imprimes el dataframe
# st.subheader('Raw data')
# st.dataframe(data=df)

# st.subheader('Top 5 Numero de visitas')
# number_of_visits_histogram = np.histogram(
#     df["number_of_visits"], bins=24, range=(0,24))[0]
# st.bar_chart(number_of_visits_histogram)

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
number_of_visits_char = plt.show()
st.bar_chart(number_of_visits_char)
