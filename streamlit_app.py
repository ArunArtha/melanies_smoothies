# Import python packages
import streamlit as st

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie!"""
)

from snowflake.snowpark.functions import col
name_on_order = st.text_input('Name on smoothie:')
st.write('The name on smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

Ingredients_List = st.multiselect(
    'Choose up to 5 Ingredients:'
    , my_dataframe
    , max_selections=5
)

if Ingredients_List:
    ingredients_string = ''
    for fruit_chosen in Ingredients_List:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

import requests  
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
#st.text(smoothiefroot_response.json())
st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
