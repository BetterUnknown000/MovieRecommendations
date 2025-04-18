import streamlit as st
from DatasetLoader import DatasetLoader

# ✅ This must be the first Streamlit call
st.set_page_config(page_title="🎬 Movie Recommender", layout="centered")

# Load and cache movie data
@st.cache_data
def load_movies():
    loader = DatasetLoader("cleaned_movies.csv")
    return loader.load_dataset(), loader

# Load data
movies, loader = load_movies()

# UI Layout
st.title("🎬 Movie Recommender")
st.write("Type a movie title to explore its genres and tags!")

# Input field
user_input = st.text_input("Enter a movie title")

# Search & Display Info
if st.button("Search"):
    movie = loader.get_movie_by_title(user_input)
    if movie:
        st.success(f"Found: {movie.title}")
        st.markdown(movie.get_info())
    else:
        st.error("Movie not found.")
