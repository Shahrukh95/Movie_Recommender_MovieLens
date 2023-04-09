from sqlalchemy.orm import sessionmaker
from import_to_database import Movies, RatingsWeighted
from sqlalchemy import create_engine, select
import streamlit as st
import pandas as pd
from sqlalchemy import func
from time import time


engine = create_engine('sqlite:///project_database.db')
Session = sessionmaker(bind=engine)
sess = Session()

st.set_page_config(page_title= "Movies 25M Project", layout="centered")
st.title("Task 3) Top 10 by Categories")
st.write("Using Bayesian Estimate to calculate a weighted rating for each movie. Takes into account the number of votes for each movie, minimum votes required to be considered among the best and the average number of votes for all movies and also for each movie.")

def get_df_on_query(query):
    query_results = pd.read_sql_query(query, create_engine('sqlite:///project_database.db'))
    return query_results

# GET MOVIES AND FIND DISTINCT CATEGORIES (WITHOUT |)
total_movies_query = select(Movies.genres)
# st.write(total_movies_query)
movies_df = get_df_on_query(total_movies_query)
genres_list = list(movies_df['genres'].str.split('|', expand=True).stack().unique())

# PUT A STREAMLIT SELECTBOX
category_chosen = st.selectbox('Choose a category', genres_list)
st.write('You selected:', category_chosen)

# INNER JOIN ON MOVIES AND RATINGS_WEIGHTED TO GET TOP 10 CATEGORY
time_for_ratings_start = time()
query = select(Movies.movieId, Movies.title, Movies.genres, RatingsWeighted.Weighted_Rating_W).join(RatingsWeighted, Movies.movieId == RatingsWeighted.movieId).where(Movies.genres.contains(category_chosen)).order_by(RatingsWeighted.Weighted_Rating_W.desc()).limit(10)
weighted_ratings_df = get_df_on_query(query)
# st.write(query)

# PRINT TIME FOR QUERY
time_for_ratings_end = time() - time_for_ratings_start
st.write("Time for query: ", time_for_ratings_end)


# PRINT FINAL RESULT AS DATAFRAME
st.dataframe(weighted_ratings_df, width=800, height=400)


