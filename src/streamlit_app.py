import streamlit as stream
import os
import signal
import sys
import time
from models.User import User
from models.UserManager import UserManager
from recommend.Recommender import Recommender
from graph.MovieGraph import MovieGraph
from tree.GenreTree import GenreTree
from data.DatasetLoader import DatasetLoader
from tree.Tree import root

if "logged_in" not in stream.session_state:
    stream.session_state.logged_in = False
if "user_id" not in stream.session_state:
    stream.session_state.user_id = None
if "mode" not in stream.session_state:
    stream.session_state.mode = None
if "show_settings" not in stream.session_state:
    stream.session_state.show_settings = False
if "shutdown" not in stream.session_state:
    stream.session_state.shutdown = False

if stream.session_state.shutdown:
    stream.title("Server Shut Down")
    stream.write("Movie Recommendations App has been shut down.")
    time.sleep(2)
    os.kill(os.getpid(), signal.SIGTERM)
    sys.exit(0)

if "movies" not in stream.session_state:
    loader = DatasetLoader("../data/cleaned_movies.csv")
    movies = loader.load_dataset()
    movies = movies[:200]
    stream.session_state.loader = loader
    stream.session_state.movies = movies

    graph = MovieGraph()
    for movie in movies:
        graph.add_movie(movie)

    for i in range(len(movies)):
        for j in range(i + 1, len(movies)):
            movie1 = movies[i]
            movie2 = movies[j]
            shared_genres = set(movie1.genres).intersection(set(movie2.genres))
            if shared_genres:
                graph.add_edge(movie1.movie_id, movie2.movie_id, weight=len(shared_genres))

    tree = GenreTree(root)
    stream.session_state.graph = graph
    stream.session_state.tree = tree
else:
    loader = stream.session_state.loader
    movies = stream.session_state.movies
    graph = stream.session_state.graph
    tree = stream.session_state.tree

user_manager = UserManager()
recommender = Recommender(graph, tree, movies, {})

stream.title("Movie Recommendation App")

if not stream.session_state.logged_in:
    if stream.session_state.mode is None:
        stream.header("Welcome to the Movie Recommender")
        stream.write("Create an account or log in to start getting personalized movie recommendations.")

    col1, col2 = stream.columns(2)

    with col1:
        if stream.button("Create New User", key="mode_create"):
            stream.session_state.mode = "signup"

    with col2:
        if stream.button("Login", key="mode_login"):
            stream.session_state.mode = "login"

    if stream.session_state.mode == "signup":
        stream.header("Create Your Account")
        username = stream.text_input("Enter a Username: ")
        password = stream.text_input("Enter a Password:", type="password")

        liked_genres = stream.multiselect(
            "Pick the genres you like:",
            ["Action", "Drama", "Comedy", "Adventure", "Thriller", "Western", "Romance", "Crime", "Mystery", "Animation",
             "Music", "Family", "Sci-Fi", "Fantasy", "Foreign", "History", "Horror", "TV Movie", "Documentary", "War"]
        )

        common_tags = [
            "adultery", "aftercreditsstinger", "alien", "based on novel", "based on true story",
            "biography", "blood", "brother brother relationship", "christmas", "college",
            "coming of age", "corruption", "dark comedy", "daughter", "death", "detective",
            "doctor", "dog", "drug", "duringcreditsstinger", "dystopia", "escape",
            "extramarital affair", "family", "father son relationship", "female nudity",
            "film noir", "france", "friends", "friendship", "gangster", "gay", "ghost",
            "gore", "high school", "holiday", "homosexuality", "hospital", "independent film",
            "infidelity", "investigation", "island", "japan", "jealousy", "kidnapping",
            "lawyer", "lgbt", "london england", "los angeles", "love", "magic", "male nudity",
            "marriage", "martial arts", "money", "monster", "murder", "music", "musical",
            "nazis", "new york", "nudity", "paris", "party", "police", "prison", "prostitute",
            "rape", "remake", "revenge", "robbery", "romance", "scientist", "sequel",
            "serial killer", "sex", "short", "silent film", "slasher", "small town", "sport",
            "spy", "stand-up comedy", "student", "suicide", "superhero", "supernatural",
            "suspense", "teacher", "teenager", "torture", "vampire", "violence", "war",
            "wedding", "wife husband relationship", "woman director", "world war ii", "zombie"
        ]

        liked_tags = stream.multiselect(
            "Pick the tags you like: (OPTIONAL)",
            common_tags
        )

        if stream.button("Submit New User", key="create_user_submit"):
            if not username or not password:
                stream.error("Please enter both a username and password.")
            elif not liked_genres:
                stream.error("Please select at least one genre.")
            else:
                existing_usernames = [info['username'] for info in user_manager.users.values()]
                if username in existing_usernames:
                    stream.error("Username already taken. Try another Username.")
                else:
                    user_id = user_manager.add_user(username, password, liked_genres, liked_tags)
                    stream.success("Account created successfully. Please log in.")
                    stream.session_state.mode = "login"
                    stream.rerun()

    if stream.session_state.mode == "login":
        if user_manager.users:
            stream.header("Login to Your Account")
            username_to_id = {info['username']: uid for uid, info in user_manager.users.items()}
            usernames = list(username_to_id.keys())

            selected_username = stream.selectbox("Select your username:", usernames)
            entered_password = stream.text_input("Enter your password:", type="password")

            if stream.button("Login", key="user_login"):
                user_id = username_to_id[selected_username]
                loaded_user = user_manager.authenticate_user(user_id, entered_password)

                if loaded_user:
                    temp_user = User(
                        user_id=int(user_id),
                        username=loaded_user["username"],
                        password=loaded_user["password"],
                        watched_movies=loaded_user.get('watched_movies', []),
                        liked_genres=loaded_user.get('liked_genres', []),
                        liked_tags=loaded_user.get('liked_tags', [])
                    )

                    recommender.users[temp_user.user_id] = temp_user

                    stream.session_state.logged_in = True
                    stream.session_state.user_id = temp_user.user_id
                    stream.session_state.mode = None
                    stream.session_state.show_settings = False
                    stream.rerun()
                else:
                    stream.error("Invalid username or password.")
        else:
            stream.warning("No users exist yet. Create a new user first.")

else:
    loaded_user = user_manager.users.get(str(stream.session_state.user_id))

    if loaded_user:
        user = User(
            user_id=int(stream.session_state.user_id),
            username=loaded_user["username"],
            password=loaded_user["password"],
            watched_movies=loaded_user.get('watched_movies', []),
            liked_genres=loaded_user.get('liked_genres', []),
            liked_tags=loaded_user.get('liked_tags', [])
        )

        recommender.users[user.user_id] = user

        stream.header("Welcome, " + user.username)

        recommendations = recommender.recommend_user(user)

        stream.subheader("Your Top 20 Movie Recommendations:")
        movie_map = {f"{movie.title} (Score: {score:.1f})": movie for movie, score in recommendations}
        selected_watched = stream.selectbox("Select a movie you’ve watched:", list(movie_map.keys()))

        if stream.button("Add Selected Movie to Watched List"):
            selected_movie = movie_map[selected_watched]
            if selected_movie.movie_id not in user.watched_movies:
                user.watched_movies.append(selected_movie.movie_id)
                user_manager.users[str(user.user_id)]["watched_movies"] = user.watched_movies
                user_manager.save_users()
                stream.success(f"Added '{selected_movie.title}' to your watched movies.")
                stream.rerun()
            else:
                stream.info(f"'{selected_movie.title}' is already in your watched list.")

        for movie, score in recommendations:
            stream.write(f"{str(movie)} - Recommendation Score: {score}")

        stream.subheader("Your Watched Movies:")
        for watched_id in user.watched_movies:
            watched_movie = loader.get_movie_by_title(
                next((m.title for m in movies if m.movie_id == watched_id), None)
            )
            if watched_movie:
                stream.write(str(watched_movie))

        stream.subheader("Remove Movies from Watched List")
        if user.watched_movies:
            watched_titles = []
            for watched_id in user.watched_movies:
                watched_movie = loader.get_movie_by_id(watched_id)
                if watched_movie:
                    watched_titles.append(f"{watched_movie.title} (ID: {watched_id})")

            movies_to_remove = stream.multiselect("Select movies to remove:", watched_titles)

            if stream.button("Remove Selected Movies"):
                for title_str in movies_to_remove:
                    movie_id = int(title_str.split("ID: ")[1][:-1])
                    if movie_id in user.watched_movies:
                        user.watched_movies.remove(movie_id)

                user_manager.users[str(user.user_id)]["watched_movies"] = user.watched_movies
                user_manager.save_users()
                stream.success("Selected movies removed from watched list.")
                stream.rerun()
        else:
            stream.write("No movies in your watched list.")

        if stream.button("Settings", key="open_settings"):
            stream.session_state.show_settings = not stream.session_state.show_settings

        if stream.session_state.show_settings:
            stream.subheader("Account Settings")
            delete_password = stream.text_input("Enter your password to delete your account:", type="password")
            if stream.button("Delete My Account", key="delete_account"):
                loaded_user_data = user_manager.users.get(str(stream.session_state.user_id))
                if loaded_user_data and user_manager.hash_password(delete_password) == loaded_user_data["password"]:
                    del user_manager.users[str(stream.session_state.user_id)]
                    user_manager.save_users()
                    stream.success("Account deleted successfully.")
                    stream.session_state.logged_in = False
                    stream.session_state.user_id = None
                    stream.session_state.mode = None
                    stream.session_state.show_settings = False
                    stream.rerun()
                else:
                    stream.error("Incorrect password. Account not deleted.")

        if stream.button("Logout", key="logout_button"):
            stream.session_state.logged_in = False
            stream.session_state.user_id = None
            stream.session_state.mode = None
            stream.session_state.show_settings = False
            stream.rerun()
    else:
        stream.error("User not found. Please log in again.")
        stream.session_state.logged_in = False
        stream.session_state.user_id = None
        stream.session_state.mode = None
        stream.session_state.show_settings = False
        stream.rerun()

stream.markdown("---")
stream.markdown("<br>", unsafe_allow_html=True)

shutdown = stream.button("Shutdown Server", key="shutdown_server_button", type="primary")

if shutdown:
    stream.session_state.shutdown = True
    stream.rerun()

stream.markdown(
    """
    <style>
    button[kind="primary"] {
        background-color: red !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)