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

                tag_map = {
                    "new york": "new york city",
                    "female nudity": "nudity",
                    "male nudity": "nudity",
                    "gay": "lgbtq",
                    "homosexuality": "lgbtq",
                    "brother brother relationship": "family",
                    "wife husband relationship": "marriage",
                    "music": "musical",
                    "france": "paris"
                }

                allowed_tags = [
                    "adultery", "aftercreditsstinger", "alien", "based on novel", "based on true story", "biography",
                    "blood",
                    "family", "christmas", "college", "coming of age", "corruption", "dark comedy", "daughter", "death",
                    "detective", "doctor", "dog", "drug", "duringcreditsstinger", "dystopia", "escape",
                    "extramarital affair",
                    "father son relationship", "film noir", "friends", "friendship", "gangster", "ghost", "gore",
                    "high school",
                    "holiday", "hospital", "independent film", "infidelity", "investigation", "island", "japan",
                    "jealousy",
                    "kidnapping", "lawyer", "lgbt", "london england", "los angeles", "love", "magic", "nudity",
                    "marriage",
                    "martial arts", "money", "monster", "murder", "musical", "nazis", "new york city", "paris", "party",
                    "police", "prison", "prostitute", "rape", "remake", "revenge", "robbery", "romance", "scientist",
                    "sequel",
                    "serial killer", "sex", "short", "silent film", "slasher", "small town", "sport", "spy",
                    "stand-up comedy",
                    "student", "suicide", "superhero", "supernatural", "suspense", "teacher", "teenager", "torture",
                    "vampire",
                    "violence", "war", "wedding", "woman director", "world war ii", "zombie"
                ]

                tags = []
                if isinstance(row.tags, str):
                    raw_tags = [t.strip().lower() for t in row.tags.split(",")]
                    cleaned_tags = []
                    for tag in raw_tags:
                        tag = tag_map.get(tag, tag)
                        if tag in allowed_tags:
                            cleaned_tags.append(tag)
                    tags = list(set(cleaned_tags))

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

    def get_movie_by_id(self, movie_id):
        for movie in self.movie_objects:
            if movie.movie_id == movie_id:
                return movie
        return None