class Recommender:

    def __init__(self, graph, tree, movies, users: dict[int, 'User']):
        self.graph = graph
        self.tree = tree
        self.movies = movies
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

    def recommend_user(self, user):
        matches = []

        for movie in self.movies:
            if movie.movie_id in user.watched_movies:
                continue

            total_score = 0

            for liked_genre in user.liked_genres:
                for movie_genre in movie.genres:
                    distance = self.tree.find_genre_distance(liked_genre, movie_genre)
                    if distance == 0:
                        total_score += 4
                    elif distance == 1:
                        total_score += 2
                    elif distance == 2:
                        total_score += 1

            if set(movie.tags).intersection(user.liked_tags):
                total_score += 1

            matches.append((movie, total_score))  # FIXED: add movie, not user

        matches.sort(key=lambda x: x[1], reverse=True)
        top_movies = [movie for movie, score in matches[:20]]  # Now it works
        return top_movies