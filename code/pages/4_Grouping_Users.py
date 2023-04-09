from sqlalchemy.orm import sessionmaker
from import_to_database import KMeansRatings
from sqlalchemy import create_engine, select
import streamlit as st
import pandas as pd
from time import time
# import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

engine = create_engine('sqlite:///project_database.db')
Session = sessionmaker(bind=engine)
sess = Session()

st.set_page_config(page_title= "Movies 25M Project", layout="centered")
st.title("Task 4) Grouping Similar Users")
st.write("Using K Means to form clusters of users. The input data consists of the user rating and a binary value for each of the 20 categories. If a category is 1, the user voted for a movie with this category and vice versa.")


def get_df_on_query(query):
    query_results = pd.read_sql_query(query, create_engine('sqlite:///project_database.db'))
    return query_results

cluster_number = st.selectbox('Choose a Group to see how they are clustered', list(range(0, 20)))

time_for_query_start = time()
KMeans_clusters = select(KMeansRatings).where(KMeansRatings.KMeans == cluster_number)
# st.write(KMeans_clusters)
k_means_df = get_df_on_query(KMeans_clusters)
time_for_query_end = time() - time_for_query_start
st.write("Time to query the chosen cluster: ", time_for_query_end)

# k_means_df
st.dataframe(k_means_df, width=800, height=400)

# LOGIC TO FIND MEANING IN CLUSTERS
k_means_single_df = k_means_df.loc[k_means_df['KMeans'] == cluster_number]

genres_list = ['Comedy', 'Crime', 'Drama', 'Thriller', 'War', 'Musical', 'Romance', 'Adventure', 'Film-Noir', 'Sci-Fi', 'Western', 'Fantasy', 'Mystery', 'Children', 'Action', 'Documentary', 'Animation', 'Horror', 'IMAX', '(no genres listed)']
good_ratings = []
bad_ratings = []

num_of_rows = k_means_single_df.shape[0]
for genre in genres_list:
    contain_values = k_means_single_df[k_means_single_df['genres'].str.contains(genre)]
    good_rows = contain_values[contain_values["rating"] >= 4]
    bad_rows = contain_values[contain_values["rating"] < 4]

    good_rating_percentage = 0
    bad_rating_percentage = 0

    good_rating_percentage = good_rows.shape[0] / num_of_rows
    good_ratings.append(good_rating_percentage * 100)

    bad_rating_percentage = bad_rows.shape[0] / num_of_rows
    bad_ratings.append(bad_rating_percentage * 100)

# good_ratings


fig = plt.figure(figsize=(10, 10))
#add axis labels
plt.xlabel("% of Good Ratings")
plt.ylabel('Genres')
plt.xlim([0, 100])
sns.barplot(x=good_ratings, y=genres_list, orient='h')
st.pyplot(fig)


fig = plt.figure(figsize=(10, 10))
#add axis labels
plt.xlabel("% of Bad Ratings")
plt.ylabel('Genres')
plt.xlim([0, 100])
sns.barplot(x=bad_ratings, y=genres_list, orient='h')
st.pyplot(fig)

