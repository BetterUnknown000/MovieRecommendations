class MovieGraph:

    def __init__(self):
        self.movies = {}
        self.edges = {}

    def add_movie(self, movie):
        if movie.movie_id not in self.movies:
            self.movies[movie.movie_id] = movie
            self.edges[movie.movie_id] = []

    def add_edge(self, id1, id2, weight=1.0):
        if id1 in self.movies and id2 in self.movies:
            self.edges[id1].append((id2, weight))
            self.edges[id2].append((id1, weight))

    def get_neighbors(self, movie_id):
        if movie_id in self.edges:
            return self.edges[movie_id]
        return []

    def print_graph(self):
        for movie_id in self.movies:
            movie_title = self.movies[movie_id].title
            connections = [(self.movies[n_id].title, w) for n_id, w in self.edges[movie_id]]
            print(movie_title + " --> " + str(connections))