class Recommender:

    def __init__(self, graph, tree, dataset, users: dict[int, 'User']):
        self.graph = graph
        self.tree = tree
        self.dataset = dataset
        self.users = users

    def recommend_genre(self, genre: str):
        node = self.tree.find_node(self.tree.root, genre)
        if node:
            return node.movies
        else:
            return []

    def recommend_graph(self, movie_id: int):
        if movie_id in self.graph.edges:
            neighbors = self.graph.edges[movie_id]
            neighbors.sort(key=lambda x: x[1], reverse=True)
            return [self.graph.movies[n_id] for n_id, _ in neighbors]
        else:
            return []

    def recommend_user(self, user: 'User'):
        matches = []
        for movie in self.dataset.movies:
            if movie.movie_id in user.watched_movies:
                continue
            shared_genres = set(movie.genres).intersection(user.liked_genres)
            shared_tags = set(movie.tags).intersection(user.liked_tags)
            if shared_genres or shared_tags:
                matches.append(movie)
        return matches
