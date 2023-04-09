from time import time
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd

def Load_Data(file_name):
    df = pd.read_csv(file_name, sep=',')
    df = df.values
    return df

Base = declarative_base()


class Movies(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, autoincrement=True) 
    movieId = Column(Integer) 
    title = Column(String)
    genres = Column(String)

class RatingsWeighted(Base):
    __tablename__ = 'ratings_weighted'
    id = Column(Integer, primary_key=True, autoincrement=True)
    movieId = Column(Integer, ForeignKey('movies.movieId'))
    No_of_votes_v = Column(Integer) 
    Avg_Rating_R = Column(Float)
    Weighted_Rating_W = Column(Float)
    # title = Column(String)
    # genres = Column(String)

class GenomeScores(Base):
    __tablename__ = 'genome_scores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    movieId = Column(Integer, ForeignKey('movies.movieId'))
    tagId = Column(Integer)
    relevance = Column(Float)

class GenomeTags(Base):
    __tablename__ = 'genome_tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tagId = Column(Integer, ForeignKey('genome_scores.tagId'))
    tag = Column(String)

class Links(Base):
    __tablename__ = 'links'
    id = Column(Integer, primary_key=True, autoincrement=True)
    movieId = Column(Integer, ForeignKey('movies.movieId'))
    imdbId = Column(Integer)
    tmdbId = Column(Integer)

class Ratings(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer)
    movieId = Column(Integer, ForeignKey('movies.movieId'))
    rating = Column(Float)
    timestamp = Column(String)

class Tags(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey('ratings.userId'))
    movieId = Column(Integer, ForeignKey('movies.movieId'))
    tag = Column(String)
    timestamp = Column(String)


class KMeansRatings(Base):
    __tablename__ = 'k_means_ratings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey('ratings.userId'))
    movieId = Column(Integer) 
    rating = Column(Float)
    genres = Column(String)
    KMeans = Column(Integer)


if __name__ == "__main__":
    #Create the database
    engine = create_engine('sqlite:///project_database.db')
    Base.metadata.create_all(engine)

    #Create the session
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()
    
    # Import Movies
    t = time()
    try:
        file_name = "D:\\Masters\\University of South Bohemia\\Database\\Other Projects\\with_database\\data\\ml-25m\\movies.csv"
        data = Load_Data(file_name) 

        for i in data:
            record = Movies(**{
                'movieId' : int(i[0]),
                'title' : str(i[1]),
                'genres' : str(i[2]),
            })
            s.add(record) #Add all the records

        s.commit() #Attempt to commit all the records
    except:
        s.rollback() #Rollback the changes on error
    finally:
        s.close() #Close the connection
    print(f"Time elapsed: " + str(time() - t) + " s." )



    # # Import Genome Scores
    # t = time()
    # try:
    #     file_name = "D:\\Masters\\University of South Bohemia\\Database\\Other Projects\\with_database\\data\\ml-25m\\genome-scores.csv"
    #     data = Load_Data(file_name) 

    #     for i in data:
    #         record = GenomeScores(**{
    #             'movieId' : int(i[0]),
    #             'tagId' : int(i[1]),
    #             'relevance' : float(i[2]),
    #         })
    #         s.add(record) #Add all the records

    #     s.commit() #Attempt to commit all the records
    # except:
    #     s.rollback() #Rollback the changes on error
    # finally:
    #     s.close() #Close the connection
    # print(f"Time elapsed: " + str(time() - t) + " s." )



    # # Import Genome Tags
    # t = time()
    # try:
    #     file_name = "D:\\Masters\\University of South Bohemia\\Database\\Other Projects\\with_database\\data\\ml-25m\\genome-tags.csv"
    #     data = Load_Data(file_name) 

    #     for i in data:
    #         record = GenomeTags(**{
    #             'tagId' : int(i[0]),
    #             'tag' : str(i[1]),
    #         })
    #         s.add(record) #Add all the records

    #     s.commit() #Attempt to commit all the records
    # except:
    #     s.rollback() #Rollback the changes on error
    # finally:
    #     s.close() #Close the connection
    # print(f"Time elapsed: " + str(time() - t) + " s." )



    # # Import Links
    # t = time()
    # try:
    #     file_name = "D:\\Masters\\University of South Bohemia\\Database\\Other Projects\\with_database\\data\\ml-25m\\links.csv"
    #     data = Load_Data(file_name) 

    #     for i in data:
    #         record = Links(**{
    #             'movieId' : int(i[0]),
    #             'imdbId' : int(i[1]),
    #             'tmdbId' : int(i[2]),
    #         })
    #         s.add(record) #Add all the records

    #     s.commit() #Attempt to commit all the records
    # except:
    #     s.rollback() #Rollback the changes on error
    # finally:
    #     s.close() #Close the connection
    # print(f"Time elapsed: " + str(time() - t) + " s." )



    # # Import Ratings
    # t = time()
    # try:
    #     file_name = "D:\\Masters\\University of South Bohemia\\Database\\Other Projects\\with_database\\data\\ml-25m\\ratings.csv"
    #     data = Load_Data(file_name) 

    #     for i in data:
    #         record = Ratings(**{
    #             'userId' : int(i[0]),
    #             'movieId' : int(i[1]),
    #             'rating' : float(i[2]),
    #             'timestamp' : str(i[3]),
    #         })
    #         s.add(record) #Add all the records

    #     s.commit() #Attempt to commit all the records
    # except:
    #     s.rollback() #Rollback the changes on error
    # finally:
    #     s.close() #Close the connection
    # print(f"Time elapsed: " + str(time() - t) + " s." )



    # # Import Tags
    # t = time()
    # try:
    #     file_name = "D:\\Masters\\University of South Bohemia\\Database\\Other Projects\\with_database\\data\\ml-25m\\tags.csv"
    #     data = Load_Data(file_name) 

    #     for i in data:
    #         record = Tags(**{
    #             'userId' : int(i[0]),
    #             'movieId' : int(i[1]),
    #             'tag' : str(i[2]),
    #             'timestamp' : str(i[3]),
    #         })
    #         s.add(record) #Add all the records

    #     s.commit() #Attempt to commit all the records
    # except:
    #     s.rollback() #Rollback the changes on error
    # finally:
    #     s.close() #Close the connection
    # print(f"Time elapsed: " + str(time() - t) + " s." )



    # # Import Ratings Weighted
    # t = time()
    # try:
    #     file_name = "D:\\Masters\\University of South Bohemia\\Database\\Other Projects\\with_database\\data\\ml-25m\\my_generated\\ratings_weighted_task_3.csv"
    #     data = Load_Data(file_name)
    #     # Iteration has to be from 1 because this data comes from a dataframe
    #     for i in data:
    #         record = RatingsWeighted(**{
    #             'movieId' : int(i[0]),
    #             'No_of_votes_v' : int(i[1]),
    #             'Avg_Rating_R' : float(i[2]),
    #             'Weighted_Rating_W' : float(i[3])
    #         })
    #         s.add(record) #Add all the records

    #     s.commit() #Attempt to commit all the records
    # except:
    #     s.rollback() #Rollback the changes on error
    # finally:
    #     s.close() #Close the connection
    # print(f"Time elapsed: " + str(time() - t) + " s." )



    # # Import K Means Ratings
    # t = time()
    # try:
    #     file_name = "D:\\Masters\\University of South Bohemia\\Database\\Other Projects\\with_database\\data\\ml-25m\\my_generated\\k_means_ratings_task_4.csv"
    #     data = Load_Data(file_name)
    #     # Iteration has to be from 1 because this data comes from a dataframe
    #     for i in data:
    #         record = KMeansRatings(**{
    #             'userId' : int(i[0]),
    #             'movieId' : int(i[1]),
    #             'rating' : float(i[2]),
    #             'genres' : str(i[3]),
    #             'KMeans' : int(i[4])
    #         })
    #         s.add(record) #Add all the records

    #     s.commit() #Attempt to commit all the records
    # except:
    #     s.rollback() #Rollback the changes on error
    # finally:
    #     s.close() #Close the connection
    # print(f"Time elapsed: " + str(time() - t) + " s." )