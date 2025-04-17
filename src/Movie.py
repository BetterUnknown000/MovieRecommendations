class Movie:

    # Basic constructor for our Movie class. This takes in the required attributes for a movie.
    def __init__(self, movie_id: int, title: str, genres: list[str], tags: list[str] = None):
        self.movie_id = movie_id # Movie must have a valid ID
        self.title = title # Movie must have a valid title
        self.genres = genres # Movie must have a genre (will be utilized in trees later)

        if tags is not None: # Tags are optional. If there is, append. If not, leave a blank list.
            self.tags = tags
        else:
            self.tags = []

    def get_info(self):
        genre_string = ", ".join(self.genres) # Genre string in case we need to call it.

        if self.tags: # Tags string, if they exist.
            tags_string = ", ".join(self.tags)
        else:
            tags_string = "No tags"

        return self.title + ": \n" + " * Genres: " + genre_string + "\n * Tags: " + tags_string # Return line for getting movie info

    def __repr__(self): # If we ever reference the object directly, this is what will be outputted instead.
        return "Movie ID: " + str(self.movie_id) + " - Title: " + str(self.title)

    def __hash__(self): # Very useful function that will make our objects usable in sets / dictionaries
        return hash(self.movie_id)
