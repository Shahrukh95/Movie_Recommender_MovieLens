# Movie Recommender

Using the [MovieLens](https://grouplens.org/datasets/movielens/) dataset, I have developed a recommendation system by clustering users according to their ratings for genres.

## Installation

Use streamlit to start the application in an Anaconda environment.

```bash
conda install -c conda-forge streamlit
```
Use SQLAlchemy to connect to database
```bash
conda install -c anaconda sqlalchemy
```
Create a SQLite database with my script initializing the tables, primary and foreign keys and the data types for all columns
```bash
python code\import_to_database.py
```

## Usage
Run the application with the following command:
```bash
streamlit run code\homepage.py
```

