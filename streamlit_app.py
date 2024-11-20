import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

@st.cache
def load_data():
   dbMovies = list(db.collection('movies').stream())
   movies_dict = list(map(lambda x: x.to_dict(), dbMovies))
   movies_dataframe = pd.DataFrame(movies_dict)
   return movies_dataframe

def load_data_byname(name):
   filtered_data_byname = dstreamMovies[dstreamMovies['name'].str.contains(name,False)]
   return filtered_data_byname

def load_data_director(director):
    filtered_data_by_director = dstreamMovies[dstreamMovies['director'] == director]
    return filtered_data_by_director

dstreamMovies = load_data()

st.header('Netflix app')

chkAllMovies = st.sidebar.checkbox('Mostrar todos los filmes')
if (chkAllMovies):
    dstreamMovies = load_data()

movietitle = st.sidebar.text_input('Titulo del filme :')
btnSearch = st.sidebar.button('Buscar filmes')

if (btnSearch):
    dstreamMovies = load_data_byname(movietitle)
    count_row = dstreamMovies.shape[0]
    st.write(f"Total de filmes mostrados : {count_row}")

selected_director = st.sidebar.selectbox('Seleccionar Director', dstreamMovies['director'].unique())
btnDirector = st.sidebar.button('Filtrar Director')

if (btnDirector):
    dstreamMovies = load_data_director(selected_director)
    count_row = dstreamMovies.shape[0]
    st.write(f"Total de filmes : {count_row}")


st.sidebar.subheader('Nuevo filme')
newMovie = st.sidebar.text_input('Name:')
newSelectCompany = st.sidebar.selectbox('Company', dstreamMovies['company'].unique())
newSelectDirector = st.sidebar.selectbox('Director', dstreamMovies['director'].unique())
newSelectGenre = st.sidebar.selectbox('Genre', dstreamMovies['genre'].unique())
newFilme = st.sidebar.button("Crear nuevo filme")

if newMovie and newSelectCompany and newSelectDirector and newSelectGenre and newFilme:
    doc_ref = db.collection('movies').document().set({
    "name": newMovie,
    "company": newSelectCompany,
    "director": newSelectDirector,
    "genre": newSelectGenre      
    })
    st.sidebar.write("Registro insertado correctamente")

st.dataframe (dstreamMovies)