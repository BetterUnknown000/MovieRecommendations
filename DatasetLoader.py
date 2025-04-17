import pandas as pd
from Movie import Movie  # For Movie.py class

class DatasetLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.movies_df = None
        self.movie_objects = []

    def load_dataset(self):
        try:
            self.movies_df = pd.read_csv(self.file_path)
            print(f"Loaded {len(self.movies_df)} movies from {self.file_path}")
            self._convert_to_objects()
            return self.movie_objects
        except Exception as e:
            print(f" Error loading dataset: {e}")
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
                print(f"⚠️ Skipped movie due to error: {e}")

    def get_movie_by_title(self, title):
        for movie in self.movie_objects:
            if movie.title.lower() == title.lower():
                return movie
        return None