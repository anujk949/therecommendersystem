import streamlit as st
import pickle as pkl
import pandas as pd
import requests
import sys
from streamlit import cli as stcli


def main():
    st.title('Movie Recommender System')

    df = pd.read_csv('updated_movies_data.csv')
    movies_array = df['title'].values
    with open('recommender_model.pkl', 'rb') as file:
        cs = pkl.load(file)


    def recommend(movie_name):
        movie_index = df[df.title == movie_name].index[0]
        list_of_top_5 = sorted(enumerate(cs[movie_index]),reverse=True, key=lambda x:x[1])[1:6]
        recommended_names = {df.loc[i[0],'movie_id'] : df.loc[i[0],'title'] for i in list_of_top_5}
        return recommended_names, movie_index

    option = st.selectbox('Select Movie',movies_array)


    def fetch(index):
        data = requests.get(f'https://api.themoviedb.org/3/movie/{index}?api_key=7a859e4a9dee524249a39a6e5c8ff6aa').json()
        return data


    if st.button('Search'):
        recommended_movies, index = recommend(option)
        poster_path = {key:fetch(key) for key,value in recommended_movies.items()}
        data = fetch(df.loc[index,'movie_id'])
        poster = 'https://image.tmdb.org/t/p/w500'+data['poster_path']

        col1, col2 = st.columns([1,3])
        with col1:
            st.image(poster,width=200)

        with col2:
            st.markdown(f'**Release Date: **{data["release_date"]}')
            st.markdown(f'**Overview: **{data["overview"]}')
            genres = []
            for i in data['genres']:
                genres.append(i['name'])
            st.markdown(f'**Genres: **{", ".join(genres)}')
        st.write('')
        st.subheader('Recommended Movies')
        col1, col2, col3, col4, col5 = st.columns(5)
        poster,caption = [],[]
        for key in poster_path.keys():
            poster.append('https://image.tmdb.org/t/p/w500'+poster_path[key]['poster_path'])
            caption.append(poster_path[key]['title'])
        with col1:
            st.image(poster[0],caption[0],width=150)
        with col2:
            st.image(poster[1],caption[1],width=150)
        with col3:
            st.image(poster[2],caption[2],width=150)
        with col4:
            st.image(poster[3],caption[3],width=150)
        with col5:
            st.image(poster[4],caption[4],width=150)
            # st.markdown(f'**Overview: **{data["overview"]}')
    st.write('')
    st.subheader('New Release')
    new_release = requests.get('https://api.themoviedb.org/3/movie/upcoming?api_key=7a859e4a9dee524249a39a6e5c8ff6aa&language=en-US&page=1').json()
    new_release_df = pd.DataFrame(new_release['results'])
    new_release_df = new_release_df.sort_values('release_date',ascending=False).reset_index(drop=True)
    new_release_df = new_release_df.iloc[:5,:]

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        poster = 'https://image.tmdb.org/t/p/w500'+new_release_df.loc[0,'poster_path']
        caption = new_release_df.loc[0,'title']
        st.image(poster,caption,width=150)
    with col2:
        poster = 'https://image.tmdb.org/t/p/w500'+new_release_df.loc[1,'poster_path']
        caption = new_release_df.loc[1,'title']
        st.image(poster,caption,width=150)
    with col3:
        poster = 'https://image.tmdb.org/t/p/w500'+new_release_df.loc[2,'poster_path']
        caption = new_release_df.loc[2,'title']
        st.image(poster,caption,width=150)
    with col4:
        poster = 'https://image.tmdb.org/t/p/w500'+new_release_df.loc[3,'poster_path']
        caption = new_release_df.loc[3,'title']
        st.image(poster,caption,width=150)
    with col5:
        poster = 'https://image.tmdb.org/t/p/w500'+new_release_df.loc[4,'poster_path']
        caption = new_release_df.loc[4,'title']
        st.image(poster,caption,width=150)


    st.write('')
    st.subheader('Popular Movies')
    trending = requests.get('https://api.themoviedb.org/3/trending/all/day?api_key=7a859e4a9dee524249a39a6e5c8ff6aa').json()
    trending_df = pd.DataFrame(trending['results'])
    trending_df = trending_df.dropna(subset=['title','poster_path']).reset_index(drop=True)
    trending_df = trending_df.sort_values('popularity',ascending=False).reset_index(drop=True)
    trending_df = trending_df.iloc[:5,:]

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        poster = 'https://image.tmdb.org/t/p/w500'+trending_df.loc[0,'poster_path']
        caption = trending_df.loc[0,'title']
        st.image(poster,caption,width=150)
    with col2:
        poster = 'https://image.tmdb.org/t/p/w500'+trending_df.loc[1,'poster_path']
        caption = trending_df.loc[1,'title']
        st.image(poster,caption,width=150)
    with col3:
        poster = 'https://image.tmdb.org/t/p/w500'+trending_df.loc[2,'poster_path']
        caption = trending_df.loc[2,'title']
        st.image(poster,caption,width=150)
    with col4:
        poster = 'https://image.tmdb.org/t/p/w500'+trending_df.loc[3,'poster_path']
        caption = trending_df.loc[3,'title']
        st.image(poster,caption,width=150)
    with col5:
        poster = 'https://image.tmdb.org/t/p/w500'+trending_df.loc[4,'poster_path']
        caption = trending_df.loc[4,'title']
        st.image(poster,caption,width=150)


if __name__ == '__main__':
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())