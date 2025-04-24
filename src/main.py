from data.DatasetLoader import DatasetLoader
from graph.MovieGraph import MovieGraph
from recommend.Recommender import Recommender
from models.User import User
from tree.Tree import root
from tree.GenreTree import GenreTree
import os
print("File exists:", os.path.exists("../data/cleaned_movies.csv"))
loader = DatasetLoader("../data/cleaned_movies.csv")
movies = loader.load_dataset()

graph = MovieGraph()
for movie in movies:
    graph.add_movie(movie)

'''for movie1 in movies:
    for movie2 in movies:
        if movie1 != movie2:
            shared_genres = set(movie1.genres).intersection(set(movie2.genres))
            if shared_genres:
                graph.add_edge(movie1.movie_id, movie2.movie_id, weight=len(shared_genres))'''

tree = GenreTree(root)

user = User(
    user_id=1,
    username="Test",
    watched_movies=[movies[0].movie_id],
    liked_genres=[],
    liked_tags=[]
)

userinput = input("What is a genre you enjoy? ")
user.like_genre(userinput)

users = {1: user}

print(user.get_profile())

recommender = Recommender(graph, tree, loader, users)

print("\n--- Genre Recommendation (Action) ---")
print(recommender.recommend_genre("Action"))

print("\n--- Graph Recommendation (based on first movie) ---")
print(recommender.recommend_graph(movies[0].movie_id))

print("\n--- Personalized Recommendation ---")
print(recommender.recommend_user(user))