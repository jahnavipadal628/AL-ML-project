import streamlit as st
import pickle
import requests
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to right, #141e30, #243b55);
    }

    .title {
        text-align: center;
        font-size: 45px;
        color: white;
        font-weight: bold;
        margin-bottom: 20px;
    }

    div.stButton > button {
        background-color: #ff4b4b;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        width: 100%;
        height: 3em;
    }

    div.stButton > button:hover {
        background-color: #ff1e1e;
    }

    .movie-card:hover {
        transform: scale(1.05);
        transition: 0.3s;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Fetch poster from TMDB
def fetch_poster(movie_id):

    api_key = "212aa41448ab21c17cf033fe80cabbcc"

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

    data = requests.get(url)

    data = data.json()

    poster_path = data['poster_path']

    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

    return full_path
def fetch_trailer(movie_title):
    query = movie_title.replace(" ", "+")
    return f"https://www.youtube.com/results?search_query={query}+trailer"

# Recommendation function
def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:

        movie_id = movies.iloc[i[0]].id

        recommended_movies.append(movies.iloc[i[0]].title)

        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# Streamlit UI
st.markdown('<div class="title">🎬 Movie Recommendation System</div>', unsafe_allow_html=True)
st.markdown("### 🍿 Get 5 similar movies instantly")
selected_movie = st.selectbox(
    "🎬 Search your favorite movie",
    sorted(movies['title'].values)
)

if st.button("Recommend"):

    names, posters = recommend(selected_movie)

    movies_data = list(zip(names, posters))

    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]

    for i in range(5):
        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    background-color: rgba(255,255,255,0.08);
                    padding: 10px;
                    border-radius: 15px;
                    text-align: center;
                ">
                    <h4 style="color:white;">{movies_data[i][0]}</h4>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.image(movies_data[i][1], use_container_width=True)