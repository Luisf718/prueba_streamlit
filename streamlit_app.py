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



#'''Este es el codigo que se utiliza para la primer visualización, Top 5 Numero de visitas por ciudad ''', con estas comillas se puede imprimir 
#en pantalla de streamlit lo que quieras

#Agrupamos por el nombre de las ciudades y sumamos las visitas que han tenido por toda la ciudad
df_groupby_ciudad_visitas = df.groupby(by='name')['number_of_visits'].agg([sum, min, max])

#Reseteamos los index para que 'name' se ponga como columna y no se quede en indice
df_groupby_ciudad_visitas = df_groupby_ciudad_visitas.reset_index()

#Ordenamos el df por el 'sum' para que esten ordenados del que tiene mas visitas al que tiene menos
df_groupby_ciudad_visitas = df_groupby_ciudad_visitas.sort_values('sum', ascending=False)

#Codigo para imprimir el grafico creado con matplotlib
st.subheader('TOP 5 visitas por ciudad')
x = df_groupby_ciudad_visitas['name'][:5]
y = df_groupby_ciudad_visitas['sum'][:5]
fig_top5 = plt.figure(figsize = (10, 5))
plt.bar(x, y, color='red')
plt.xlabel('Ciudad')
plt.ylabel('Visitas')
# plt.title('TOP 5 visitas por ciudad')
st.pyplot(fig_top5)

#Codigo para segunda visualización, Top 10 Numero de visitas por ciudad
st.subheader('TOP 10 visitas por ciudad')
x = df_groupby_ciudad_visitas['name'][:10]
y = df_groupby_ciudad_visitas['sum'][:10]
fig_top10 = plt.figure(figsize = (10, 5))
plt.barh(x, y, color='blue')
plt.xlabel('Ciudad')
plt.ylabel('Visitas')
st.pyplot(fig_top10)

#Creamos la visualización del tiempo promedio de estacia por ciudad
#Creamos el dataframe
df_average_night_per_city = df.groupby(by='name')['average_nights'].agg(['mean', 'median'])
df_average_night_per_city = df_average_night_per_city.reset_index()
st.dataframe(df_average_night_per_city)

# import the circlify library
import circlify

# compute circle positions:
circles = circlify.circlify(
    df_average_night_per_city['mean'].tolist(), 
    show_enclosure=False, 
    target_enclosure=circlify.Circle(x=0, y=0, r=1)
)

#Create just a figure and only one subplot
fig, ax = plt.subplots(figsize=(10,10))

# Title
ax.set_title('Promedio de noches por ciudad')

# Remove axes
ax.axis('off')

# Find axis boundaries
lim = max(
    max(
        abs(circle.x) + circle.r,
        abs(circle.y) + circle.r,
    )
    for circle in circles
)
plt.xlim(-lim, lim)
plt.ylim(-lim, lim)

# list of labels
labels = df_average_night_per_city['name']


colors = [
          'yellow',
          'blue',
          'red',
          'grey',
          'purple',
          'green',
          'white',
          'pink',
          'orange',
          '#30D5C8',
          '#C8A2C8'
]
count = 0
for circle, label in zip(circles, labels):
    x, y, r = circle
    ax.add_patch(plt.Circle((x, y), r, alpha=1, linewidth=2, facecolor=colors[count], edgecolor="black"))
    plt.annotate(label, (x,y ) ,va='center', ha='center', bbox=dict(facecolor=colors[count], edgecolor=colors[count]))
    count+=1
