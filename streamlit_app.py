# streamlit_app.py

import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from psycopg2 import Error
import numpy as np
import plotly.graph_objects as gp
import squarify

def conection_sql(query:str):
  connection = psycopg2.connect(user="vyzgmpqsxeucnv",
                            password="480540f32aa53c6f6850fee0add13f0ae8211a9aa7c98ed18fab701a829869df",
                            host="ec2-54-157-79-121.compute-1.amazonaws.com",
                            port="5432",
                            database="d1evcvc2sccml6")
  #Creamos el cursor para las operaciones de la base de datos
  cursor = connection.cursor()
  #Creamos una variable con el codigo sql que queremos que se ejecute
  select_query = query
  #Executamos el comando
  cursor.execute(select_query)
  connection.commit()
  #Esto crea un data frame con la información que pediste de la base de datos
  df = pd.read_sql_query(select_query,connection)
  if (connection):
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")
  return df

df = conection_sql('''SELECT *
  FROM PUBLIC.accommodations a
  JOIN PUBLIC.cities c ON c.city_id = a.id_city
  ORDER BY a.id;''')


#'''Este es el codigo que se utiliza para la primer visualización, Top 5 Numero de visitas por ciudad ''', con estas comillas se puede imprimir 
#en pantalla de streamlit lo que quieras

#Agrupamos por el nombre de las ciudades y sumamos las visitas que han tenido por toda la ciudad
df_groupby_ciudad_visitas = df.groupby(by='name')['number_of_visits'].agg([sum, min, max])

#Reseteamos los index para que 'name' se ponga como columna y no se quede en indice
df_groupby_ciudad_visitas = df_groupby_ciudad_visitas.reset_index()

#Ordenamos el df por el 'sum' para que esten ordenados del que tiene mas visitas al que tiene menos
df_groupby_ciudad_visitas = df_groupby_ciudad_visitas.sort_values('sum', ascending=False)

#Codigo para visuzalizacion de numero de visitas por ciudad
st.header('Numero de visitas por ciudad')
x = df_groupby_ciudad_visitas['name']
y = df_groupby_ciudad_visitas['sum']
fig_visitas = plt.figure(figsize = (10, 5))
plt.bar(x, y, color='blue')
plt.xticks(rotation='vertical')
plt.xlabel('Ciudad')
plt.ylabel('Visitas')
st.pyplot(fig_visitas)

"""Podemos notar que cancun tiene muchas menos visitas, esto es raro porque en cancun normalmente hay muchos turistas"""

#Creamos la visualizacion de los alojamientos que hay por ciudad
#Agrupamos por ciudad y contamos el numero que hay por ciudad
df_alojamientos_por_ciudad = df.groupby('name')['id'].agg(['count','sum'])

#Reseteamos el index para poder manipular mejor el dataframe
df_alojamientos_por_ciudad = df_alojamientos_por_ciudad.reset_index()

#Ordenamos el dataframe para que vaya de manera descendente
df_alojamientos_por_ciudad = df_alojamientos_por_ciudad.sort_values('count',ascending=False)

st.header('Alojamientos por ciudad')
x = df_alojamientos_por_ciudad['name']
y = df_alojamientos_por_ciudad['count']
fig_alojamientos = plt.figure(figsize = (10, 5))
plt.barh(x, y, color='green')
plt.xticks(rotation='vertical')
plt.ylabel('Ciudad')
plt.xlabel('Numero de alojamientos')
plt.title('Alojamientos por ciudad')
st.pyplot(fig_alojamientos)

"""En esta grafica se muestra que Cancun es donde Airbnb tiene menos alojamientos, esta puede ser una oportunidad para que tengamos mas alojamientos en Cancun y cubrir la
la demanda"""

#Creamos la visualización del tiempo promedio de estacia por ciudad
#Creamos el dataframe
df_average_night_per_city = df.groupby(by='name')['average_nights'].agg(['mean', 'median'])
df_average_night_per_city = df_average_night_per_city.reset_index()

# import the circlify library
import circlify

# compute circle positions:
circles = circlify.circlify(
    df_average_night_per_city['mean'].tolist(), 
    show_enclosure=False, 
    target_enclosure=circlify.Circle(x=0, y=0, r=1)
)

#Create just a figure and only one subplot
fig_burbujas, ax = plt.subplots(figsize=(10,10))

# Title
#Este titulo va dentro de la visualizacion, del cuadro blanco 
# ax.set_title('Promedio de noches por ciudad')

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

#Esto es para que el ciclo for cambie de color las burbujas y sean todas de diferente color
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
st.header('Promedio de noches por ciudad')
st.pyplot(fig_burbujas)

#Hacemos la visualizacion de el total de los alojamientos
df_alojamientos_totales = df['id'].agg(['count','sum'])
total_accommodations = df_alojamientos_totales['count']
st.header('Total de alojamientos')
st.subheader(total_accommodations)

#Empezamos a contruir la piramide poblacional
#Ponemos el query en la función para que tengamos el dataframe de los usuarios
df_users = conection_sql('''SELECT *
FROM PUBLIC.users u
JOIN PUBLIC.cities c ON c.city_id = u.city_id
ORDER BY u.user_id;''')

#Agrupamos por genero y edad
df_piramide_poblacional = df_users.groupby(['gender', 'age'])['user_id'].agg(['count'])
df_test=df_users.groupby(['gender', 'age'])['user_id']
df_test=df_users[['gender','age']]

#Creamos los rangos de edades
df_test.loc[(df_test['age'] >=18) & (df_test['age'] <22) , 'Rango'] = '18-27' 
df_test.loc[(df_test['age'] >=28) & (df_test['age'] <32) , 'Rango'] = '28-37'
df_test.loc[(df_test['age'] >=38) & (df_test['age'] <42) , 'Rango'] = '38-47' 
df_test.loc[(df_test['age'] >=48) & (df_test['age'] <52) , 'Rango'] = '48-57' 
df_test.loc[(df_test['age'] >=58) & (df_test['age'] <62) , 'Rango'] = '58-67' 
df_test.loc[(df_test['age'] >=68) & (df_test['age'] <72) , 'Rango'] = '68-77'
df_test.loc[(df_test['age'] >=78) & (df_test['age'] <80) , 'Rango'] = '78-+'

df_test.insert(2, "prev", 1, True)
df_t2=pd.pivot_table(df_test,index="Rango", columns="gender", values="prev", aggfunc=np.sum)
df_t2.reset_index(inplace=True)
y_r=df_t2['Rango']
X_M=df_t2['Male']
X_F=df_t2['Female'] * -1

#Creamos el grafico
st.header('Piramide Poblacional de Usuarios')
# Creating instance of the figure
fig_piramide_users = gp.Figure()
  
# Adding Male data to the figure
fig_piramide_users.add_trace(gp.Bar(y= y_r, x = X_M,
                     name = 'Male',
                     orientation = 'h'))

# Adding Female data to the figure
fig_piramide_users.add_trace(gp.Bar(y = y_r, x = X_F,
                     name = 'Female', orientation = 'h'))

# Updating the layout for our graph
fig_piramide_users.update_layout(
                 barmode = 'relative',
                 bargap = 0.0, bargroupgap = 0,
                 xaxis = dict(tickvals = [-10, -25, -45,
                                          0, 10, 25, 45],
                                
                              ticktext = ['10', '25', '45', '0', 
                                          '10', '25', '45'],
                                
                              title = 'Population age',
                              title_font_size = 14)
                 )
# st.pyplot(fig_piramide_users)
# fig_piramide_users.show()
st.plotly_chart(fig_piramide_users)

#Crear aqui la piramide de los host

#Parte de Cristhian 
# == Min and max prices by city

df = conection_sql('''select min(a.price), max(a.price), c."name"
   	from public.accommodations a
   	join public.cities c on c.city_id = a.id_city 
   	group by c."name"
   	order by c."name"''')

df_cities = df['name']
df_min = df['min']
df_max = df['max']

st.subheader('Min and max prices by city')

fig_min_max, ax1 = plt.subplots(figsize=(10,10))

color = 'tab:red'
ax1.set_xlabel('cities')
ax1.set_ylabel('min prices', color=color)
ax1.plot(df_cities, df_min, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('max prices', color=color)  # we already handled the x-label with ax1
ax2.plot(df_cities, df_max, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig_min_max.tight_layout()  # otherwise the right y-label is slightly clipped
st.pyplot(fig_min_max)

# =


# == Guest capacity by city

df = conection_sql('''select PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY a.person_capacity) capacity, c."name"
   from public.accommodations a
   join public.cities c on c.city_id = a.id_city 
   group by c."name"
   order by capacity desc;''')

df_cities = df['name']
df_capacity = df['capacity']

st.subheader('Guest capacity by city')

df = pd.DataFrame({'cities':df['capacity'], 'group':df['name'] })

fig_pie = plt.figure(figsize = (10, 5))
squarify.plot(sizes=df['cities'], label=df['group'], alpha=.8 )
plt.axis('off')
st.pyplot(fig_pie)

# Pie chart
# guest_capacity_city, ax1 = plt.subplots()
# ax1.pie(df_capacity, labels=df_cities, autopct='%.1f')
# st.pyplot(guest_capacity_city)

# =

# == Average stars by city

df = conection_sql('''select avg(a.star_rating), count(a.star_rating), c."name"
   from public.accommodations a
   join public.cities c on c.city_id = a.id_city 
   group by c."name"
   order by c."name";''')

df_cities = df['name']
df_starts_avg = df['avg']
df_starts_count = df['count']

st.subheader('Guest capacity by city')

x = df_cities
y = df_starts_avg
s = df_starts_count

fig_scatter = plt.figure(figsize = (12, 8))
plt.scatter(x, y, s, c="b", alpha=0.5, label="Stars")
plt.xlabel("Cities")
plt.ylabel("Qualification")
plt.legend(loc='upper left')

for i, txt in enumerate(s):
    x1 = i+0.2
    plt.annotate(txt, (x1, y[i]))

st.pyplot(fig_scatter)

