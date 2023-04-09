from sqlalchemy.orm import sessionmaker
from import_to_database import Movies
from sqlalchemy import create_engine, select
import streamlit as st
import pandas as pd
from time import time
import math
from sqlalchemy import func

engine = create_engine('sqlite:///project_database.db')
Session = sessionmaker(bind=engine)
sess = Session()

st.set_page_config(page_title= "Movies 25M Project", layout="centered")
st.title("Movie Recommender")

st.subheader("Task 1) Select Page to View Movies")

movie_per_page = 15
# CALCULATE TOTAL NUMBER OF MOVIES
# COUNT (*) WILL USE THE COVERING INDEX CREATED ON THE MOVIEID COLUMN
total_movies_query = select(func.count("*")).select_from(Movies)
total_movies = sess.execute(total_movies_query).first()[0]

# CALCULATE NUMBER OF PAGES FOR MOVIES
total_pages = math.ceil(total_movies / movie_per_page)

# DISPLAY TOTAL NUMBER OF PAGES
st.write("Total Pages are: ", total_pages)
page_number = st.number_input('Type a Page Number to view the results', 1, total_pages, 1)

starting_movie_index = (page_number - 1) * movie_per_page
ending_movie_index = (page_number) * movie_per_page - 1

start_movies_query = time()

part_query = select(Movies.movieId, Movies.title, Movies.genres).limit(movie_per_page).offset(starting_movie_index)

# st.write("Query: ", part_query)
part_query_results = pd.read_sql_query(part_query, create_engine('sqlite:///project_database.db'))
st.write("Time to query selected movies: ", time() - start_movies_query)

st.dataframe(part_query_results, width=800, height=500)


# Task 2
st.subheader("Task 2) Searching Movies")

input_text = st.text_input('Search for Movie Title', 'lord of')

# INDEXING WILL NOT BE USED HERE BECUASE THE FIRST LETTER IS AFTER THE FIRST WILDCARD
search_movie_title = select(Movies.movieId, Movies.title, Movies.genres).where(Movies.title.contains(input_text))
# st.write(search_movie_title)
start_movies_query = time()
search_movie_results = pd.read_sql_query(search_movie_title, create_engine('sqlite:///project_database.db'))
st.write("Time for searching movie with wildcard: ", time() - start_movies_query)

st.dataframe(search_movie_results, width=800, height=500)

