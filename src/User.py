#
# Code made by Earl Hibbs
#
class User:

    def __init__(self, user_id: int, username: str, watched_movies: list[int] = None, liked_genres: list[str] = None, liked_tags: list[str] = None):
        self.user_id = user_id # All users must have a valid ID. Everything else can be none if they don't want to be.
        self.username = username # Provide a username to the User class.

        if watched_movies is not None: # Sets watched movies if there are some provided. Makes it empty otherwise.
            self.watched_movies = watched_movies
        else:
            self.watched_movies = []

        if liked_genres is not None: # Sets liked genres if there are some provided. Makes it empty otherwise.
            self.liked_genres = liked_genres
        else:
            self.liked_genres = []

        if liked_tags is not None: # Sets liked tags if there are some provided. Makes it empty otherwise.
            self.liked_tags = liked_tags
        else:
            self.liked_tags = []


    def watch_movie(self, movie_id: int):
        # This function adds movies to the watchlist of the user, and checks to make sure it isn't added twice if it is already on there.
        if movie_id not in self.watched_movies:
            self.watched_movies.append(movie_id)

    def like_genre(self, genre: str):
        # This adds a liked genre to the user's liked genres. This will probably be a setting we can utilize in our GUI.
        if genre not in self.liked_genres:
            self.liked_genres.append(genre)

    def like_tag(self, tag: str):
        # This adds a liked tag to the user's liked tags.
        if tag not in self.liked_tags:
            self.liked_tags.append(tag)

    def get_profile(self):
        # Gets user's profile stats in case we need it. Stores as a dictionary.
        return {
            "User ID": self.user_id,
            "Username": self.username,
            "Watched Movies": self.watched_movies,
            "Liked Genres": self.liked_genres,
            "Liked Tags": self.liked_tags
        }

    def __repr__(self): # In case we reference the object itself, this is what will be outputted.
        return "User ID: " + str(self.user_id) + "\nUsername: " + str(self.username)
