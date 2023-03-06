import streamlit
import snowflake.connector
import pandas
import requests
from urllib.error import URLError

streamlit.title("My Parents New Healthy Diner")
streamlit.header("Breakfast Menu")
streamlit.text("🍓 Omega 3 and Bleuberry Oatmeal")
streamlit.text("🍎 Kale, Spinach and Rocket Smoothie")
streamlit.text("🥑 Hard Boiled Free Ranged Egg")

#import pandas
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),["Avocado", "Strawberries"])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(my_fruit_list)
#import requests
# New section to display Fruityvice API Response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
  streamlit.error("Please select a fruit to get information.")
  else:
       fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
       # Take the JSON version and normalize it
       fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
       # Puts it in a dataframe as a table
       streamlit.dataframe(fruityvice_normalized)
except URLLError as e:
    streamlit.error()




streamlit.stop()

#import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

# Allow the end user to add a fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('Thanks for adding', add_my_fruit)
