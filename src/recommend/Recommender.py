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
        matches = {}

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

            tag_matches = set(movie.tags).intersection(user.liked_tags) if user.liked_tags else set()
            total_score += 1 * len(tag_matches)

            for watched_id in user.watched_movies:
                neighbors = self.graph.get_neighbors(watched_id)
                for neighbor_id, weight in neighbors:
                    if neighbor_id == movie.movie_id:
                        total_score += weight

            if total_score > 0:
                matches[movie] = total_score

        sorted_movies = sorted(matches.items(), key=lambda x: x[1], reverse=True)
        top_movies = sorted_movies[:20]

        for movie, score in top_movies:
            print(str(movie) + " - Score: " + str(score))

        return top_movies