import streamlit as st
import pickle
import pandas as pd
import requests

s = requests.Session()

def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=ff908b9511e6589713db6bf7d3093231&language=en-US'.format(
        movie_id)
    data = s.get(url)
    data = data.json()
    poster_path = data['poster_path']
    if poster_path is not None:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        full_path = None
    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[0:30]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


def make_grid(cols, rows):
    grid = [0] * cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid

def show_recommendations(selected_movie):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    for i in range(0, 30, 3):
        recommended_movie_name_c1 = recommended_movie_names[i]
        recommended_movie_poster_c1 = recommended_movie_posters[i]
        recommended_movie_name_c2 = recommended_movie_names[i + 1]
        recommended_movie_poster_c2 = recommended_movie_posters[i + 1]
        recommended_movie_name_c3 = recommended_movie_names[i + 2]
        recommended_movie_poster_c3 = recommended_movie_posters[i + 2]

        grid_index = int(i / 3)
        my_grid[grid_index][0].write(recommended_movie_name_c1)
        try:
            my_grid[grid_index][0].image(recommended_movie_poster_c1)
        except:
            my_grid[grid_index][0].write("Poster unavailable")

        my_grid[grid_index][1].write(recommended_movie_name_c2)
        try:
            my_grid[grid_index][1].image(recommended_movie_poster_c2)
        except:
            my_grid[grid_index][0].write("Poster unavailable")

        my_grid[grid_index][2].write(recommended_movie_name_c3)
        try:
            my_grid[grid_index][2].image(recommended_movie_poster_c3)
        except:
            my_grid[grid_index][0].write("Poster unavailable")

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')
movie_list = movies['title'].values
selected_movie = st.selectbox(
    'How would you like to be contacted?',
    movie_list
)
if st.button('Show Recommendation'):
    my_grid = make_grid(10, (3, 3, 3))
    show_recommendations(selected_movie)


hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''
st.markdown(hide_img_fs, unsafe_allow_html=True)