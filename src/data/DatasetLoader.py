#
# Code made by Ishaq Halimi
#
import pandas as pd
from models.Movie import Movie # For Movie.py class

class DatasetLoader:
    def __init__(self, path):
        self.path = path
        self.movie_objects = []

    def load_dataset(self):
        try:
            df = pd.read_csv(self.path)

            for i, row in enumerate(df.itertuples(), start=1):
                title = row.title
                genres = []

                if isinstance(row.genres, str):
                    genres = [g.strip() for g in row.genres.split(",")]

                tags = []
                if isinstance(row.tags, str):
                    tags = [t.strip() for t in row.tags.split(",")]

                movie = Movie(movie_id=i, title=title, genres=genres, tags=tags)
                self.movie_objects.append(movie)

            print("Dataset Loaded!")
            return self.movie_objects

        except Exception as e:
            print("Error loading dataset:", e)
            return []

    def _convert_to_objects(self):
        self.movie_objects = []
        for _, row in self.movies_df.iterrows():
            try:
                movie_id = hash(row['title'])  # or generate your own integer ID if needed
                title = row['title']
                genres = [g.strip() for g in str(row['genres']).split(",") if g.strip()]
                tags = [t.strip() for t in str(row['tags']).split(",") if t.strip()] if pd.notna(row['tags']) else []
                movie = Movie(movie_id, title, genres, tags)
                self.movie_objects.append(movie)
            except Exception as e:
                print(f"Skipped movie due to error: {e}")

    def get_movie_by_title(self, title):
        for movie in self.movie_objects:
            if movie.title.lower() == title.lower():
                return movie
        return None
