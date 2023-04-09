from sqlalchemy.orm import sessionmaker
from import_to_database import Movies, RatingsWeighted, KMeansRatings
from sqlalchemy import create_engine, select
import streamlit as st
import pandas as pd
from time import time
# import numpy as np

engine = create_engine('sqlite:///project_database.db')
Session = sessionmaker(bind=engine)
sess = Session()

st.set_page_config(page_title= "Movies 25M Project", layout="centered")
st.title("Task 5) Movie Recommendation")
st.write("By using the clusters formed in the last task, we can determine if majority users like the type of movies in a cluster or not. Depending on this interest, we either suggest a movie from the same cluster or from the other clusters.")

def get_df_on_query(query):
    query_results = pd.read_sql_query(query, create_engine('sqlite:///project_database.db'))
    return query_results

userId = st.number_input('Insert a user ID', 1)


# GET K MEAN CLUSTERS
time_for_query_start = time()
k_means_query = select(KMeansRatings).where(KMeansRatings.userId == userId)
# st.write(k_means_query)
k_means_df = get_df_on_query(k_means_query)
time_for_query_end = time() - time_for_query_start
st.write("Time to query to find cluster: ", time_for_query_end)
# st.dataframe(k_means_df, width=800, height=400)


# LOGIC PART
# FIND THE CLUSTER THE USER BELONGS TO
cluster_number = k_means_df['KMeans'].value_counts().idxmax()
st.write("User belongs to cluster: ", cluster_number)

# GET THE DATA IN THIS CLUSTER
time_for_query_start = time()
k_means_query = select(KMeansRatings).where(KMeansRatings.KMeans == int(cluster_number))
# st.write(k_means_query)
k_means_cluster_df = get_df_on_query(k_means_query)
time_for_query_end = time() - time_for_query_start
st.write("Time to query all records in the cluster: ", time_for_query_end)

# SHOW THE CLUSTER IN DATAFRAME
st.dataframe(k_means_cluster_df, width=800, height=400)


# FIND THE GOOD/BAD RATED MOVIES
good_rows = k_means_cluster_df[k_means_cluster_df["rating"] >= 4]
bad_rows = k_means_cluster_df[k_means_cluster_df["rating"] < 4]

# GET ADDITIONAL DATA

# GET MOVIES
total_movies_query = select(Movies)
# st.write(total_movies_query)
movies_df = get_df_on_query(total_movies_query)

# GET WEIGHTED RATINGS
total_weighted_ratings_query = select(RatingsWeighted)
weighted_df = get_df_on_query(total_weighted_ratings_query)

# SELECT GOOD MOVIES THAT HAVE NOT BEEN RATED BY THIS USER
good_rows = good_rows[good_rows["userId"] != userId]
good_rows = good_rows.drop_duplicates(subset=['movieId'])

# RECOMMENDER SYSTEM
recommended_df = pd.DataFrame()

if good_rows.shape[0] >= 15:
    st.subheader("This group has made enough good ratings (i.e. >= 15 positive ratings). We suggest some movies from this cluster that the user has not previously seen/rated.")
    st.subheader("Suggested Movies: ")
    # GET THE WEIGHTED RATINGS FOR THE ABOVE MOVIES
    new_good_rows = pd.merge(good_rows, weighted_df[["movieId", "Weighted_Rating_W"]], on="movieId")

    # GET THE MOVIE TITLES AS WELL
    new_good_rows = pd.merge(new_good_rows, movies_df[["movieId", "title"]], on="movieId")

    # SHOW THE TOP 15 MOVIES - RECOMMENDED MOVIES FOR THIS USER (FROM THIS CLUSTER)
    recommended_df = new_good_rows.sort_values('Weighted_Rating_W', ascending=False).head(15)

    # FINAL RECOMMENDED MOVIES
    st.dataframe(recommended_df[['movieId','title', 'Weighted_Rating_W', 'genres', 'KMeans']], width=800, height=400)

# IF NEGATIVE RATINGS ARE MORE FREQUENT
elif good_rows.shape[0] < 15:
    st.subheader("This Group has made mostly negative ratings. In this cluster, we find the 3 three least negatively reviewed genres and use them to suggest new movies to the user which user has not seen/rated. In this case, the new movies will be suggested from the whole movies pool instead of just the current cluster.")
    st.subheader("Suggested Movies: ")

    # SELECT MOVIES THAT HAVE NOT BEEN RATED BY THIS USER
    bad_rows = bad_rows[bad_rows["userId"] != userId]
    bad_rows = bad_rows.drop_duplicates(subset=['movieId'])

    # GET 3 LEAST FREQUENT GENRES - THOSE WILL BE THE LEAST DISLIKED GENRES
    all_genres_repeated = list(bad_rows['genres'].str.split('|', expand=True).stack())
    all_genres_repeated_df = pd.DataFrame(all_genres_repeated, columns=["genres"])
    all_genres_repeated_df = all_genres_repeated_df.groupby(['genres'])['genres'].count().reset_index(name='counts').sort_values('counts', ascending=False)
    least_frequest_disliked_df = all_genres_repeated_df[-3:]
    print(least_frequest_disliked_df)

    # SEARCH FOR THOSE GENRES IN ALL THE MOVIES (INCLUDING OUTSIDE THE CLUSTER)
    movies_pool = movies_df[movies_df['genres'].str.contains(least_frequest_disliked_df.iloc[0][0] + '|' + least_frequest_disliked_df.iloc[1][0] + '|' + least_frequest_disliked_df.iloc[2][0])]
    recommended_df = pd.merge(movies_pool, weighted_df[["movieId", "Weighted_Rating_W"]], on="movieId")

    # RECOMMEND THE TOP 15 MOVIES
    recommended_df = recommended_df.sort_values('Weighted_Rating_W', ascending=False).head(15)

    # FINAL RECOMMENDED MOVIES
    st.dataframe(recommended_df[['movieId','title', 'Weighted_Rating_W', 'genres']], width=800, height=400)
    



