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

    def build_edges(self):
        from collections import defaultdict
        tag_to_movies = defaultdict(set)
        MAX_MOVIES_PER_TAG = 200
        MAX_NEIGHBORS_PER_MOVIE = 50
        for movie in self.movies.values():
            for tag in movie.tags:
                tag_to_movies[tag].add(movie.movie_id)
        for tag in list(tag_to_movies.keys()):
            if len(tag_to_movies[tag]) > MAX_MOVIES_PER_TAG:
                tag_to_movies[tag] = set()
        for movie_id, movie in self.movies.items():
            connected_ids = set()
            for tag in movie.tags:
                for neighbor_id in tag_to_movies[tag]:
                    if neighbor_id == movie_id or neighbor_id in connected_ids:
                        continue
                    shared_tags = set(movie.tags).intersection(self.movies[neighbor_id].tags)
                    if shared_tags:
                        weight = len(shared_tags)
                        if len(self.edges[movie_id]) >= MAX_NEIGHBORS_PER_MOVIE:
                            break
                        if len(self.edges[neighbor_id]) >= MAX_NEIGHBORS_PER_MOVIE:
                            continue
                        self.add_edge(movie_id, neighbor_id, weight)
                        connected_ids.add(neighbor_id)