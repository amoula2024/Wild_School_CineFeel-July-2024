#Import des modules
import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from streamlit_authenticator import Authenticate
from streamlit_option_menu import option_menu
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

#Centrage affichage
#st.set_page_config(layout="wide")

# Nos données utilisateurs doivent respecter ce format
lesDonneesDesComptes = {'usernames': {'utilisateur': {'name': 'user',
   'password': 'userMDP',
   'email': 'amal.mouqadem@gmail.com',
   'failed_login_attemps': 0, # Sera géré automatiquement
   'logged_in': False, # Sera géré automatiquement
   'role': 'utilisateur'},
  'root': {'name': 'root',
   'password': 'rootMDP',
   'email': 'ericrascle42@gmail.com ',
   'failed_login_attemps': 0, # Sera géré automatiquement
   'logged_in': False, # Sera géré automatiquement
   'role': 'administrateur'}}}

authenticator = Authenticate(
    lesDonneesDesComptes, # Les données des comptes
    "cookie name", # Le nom du cookie, un str quelconque
    "cookie key", # La clé du cookie, un str quelconque
    30, # Le nombre de jours avant que le cookie expire 
)
authenticator.login()


def programme_cinefeel():


    #Titre et preheader
    st.title('Bienvenu(e) sur :movie_camera: :blue[_CinéFeel_] :clapper:')
    st.header('Vous manquez d&rsquo;idées pour une soirée ciné, nous vous aidons à en trouver !:bulb:')
    st.image('image1.jpg')

    #lecture des bases de données
    df_nn = pd.read_csv("movies_ACP.csv")
    df = pd.read_csv("datasettorun.csv")

    #Liste des films pour la boîte de sélection
    select_film = df.movie_title.sort_values()

    #Affichage checkbox sélection films et préparation des bases movies pour toute la famille
    choix_enfant = st.checkbox("Films pour toute la famille")
    if choix_enfant :
        df = df.loc[(df['age_restriction']=='G')|(df['age_restriction']=='PG')|(df['age_restriction']=='TV-G')|(df['age_restriction']=='TV-Y7')|(df['age_restriction']=='TV-Y7-FV')|(df['age_restriction']=='TV-Y')]
        df_nn = df_nn.loc[df.loc[(df['age_restriction']=='G')|(df['age_restriction']=='PG')|(df['age_restriction']=='TV-G')|(df['age_restriction']=='TV-Y7')|(df['age_restriction']=='TV-Y7-FV')|(df['age_restriction']=='TV-Y')].index]
        df.reset_index(drop=True,inplace=True)
        df_nn.reset_index(drop=True,inplace=True)
        select_film =df[(df['age_restriction']=='G')|(df['age_restriction']=='PG')|(df['age_restriction']=='TV-G')|(df['age_restriction']=='TV-Y7')|(df['age_restriction']=='TV-Y7-FV')|(df['age_restriction']=='TV-Y')].movie_title.sort_values()

    #Affichage boites de selection du titre du film
    choix = st.selectbox(
        "Sélectionnez un titre de film :",
        select_film)

    #Header + Saut de page
    st.header(':dizzy:_:blue[Votre sélection]_:dizzy:')
    saut1=f"<br>"
    st.markdown(saut1, unsafe_allow_html=True)

    #Lancement de l'algorithme et entrainement sur le modèle de données
    nn = NearestNeighbors(n_neighbors=6,metric='manhattan')
    nn.fit(df_nn.values)

    #récupèration des caractéristiques du film choisie par l'utilisateur
    ligne = df[df.movie_title==choix].index[0]

    #récupération des index des 5 recommandations
    distances, index = nn.kneighbors([df_nn.iloc[ligne, :]])

    #Affichage des caractéristiques du film sélectionné
    with st.container(border=True):
        col1, col2= st.columns([0.23,0.77],gap="small")
        with col1:
            if df.loc[index[0][0], "poster_link"] == '0' or type(df.loc[index[0][0], "poster_link"]) == float:
                pass
            else:
                st.image(df.loc[index[0][0], "poster_link"])
        
        with col2:
            selectl1 = f"<p style='font-weight: bold; font-size: 20px;line-height: 1;'>{df.loc[index[0][0], 'movie_title']}</p>"
            st.markdown(selectl1, unsafe_allow_html=True)
            if df.loc[index[0][0], 'awards'] == '0' or type(df.loc[index[0][0], 'awards']) == float:
                selectl2 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][0], 'director_name']}&nbsp; - &nbsp;{df.loc[index[0][0], 'country']}&nbsp; - &nbsp;{str(int(df.loc[index[0][0], 'title_year']))}</p>"
            else:
                selectl2 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][0], 'director_name']}&nbsp; - &nbsp;{df.loc[index[0][0], 'country']}&nbsp; - &nbsp;{str(int(df.loc[index[0][0], 'title_year']))}&nbsp; - &nbsp;{df.loc[index[0][0], 'awards']}</p>"
            st.markdown(selectl2, unsafe_allow_html=True)
            selectl3 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][0], 'actor_1_name']}&nbsp; - &nbsp;{df.loc[index[0][0], 'actor_2_name']}&nbsp; - &nbsp;{df.loc[index[0][0], 'actor_3_name']}</p>"
            st.markdown(selectl3, unsafe_allow_html=True)
            selectl4 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][0], 'genres']}&nbsp; - &nbsp;{str(df.loc[index[0][0], 'imdb_score'])}&nbsp; - &nbsp;{int(df.loc[index[0][0], 'budget']):,} $</p>"
            st.markdown(selectl4, unsafe_allow_html=True)
            if df.loc[index[0][0], 'plot'] == '0' or type(df.loc[index[0][0], 'plot']) == float:
                pass
            else:
                selectl5 = f"<p style='font-size: 16px;line-height: 1;'>Synopsis : {df.loc[index[0][0], 'plot']}</p>"
                st.markdown(selectl5, unsafe_allow_html=True)
            selectl6=f"<br>"
            st.markdown(selectl6, unsafe_allow_html=True)

    saut2=f"<br>"
    st.markdown(saut2, unsafe_allow_html=True)
    st.header(':sparkles:_:blue[Nos 5 recommandations]_:sparkles:')
    saut3=f"<br>"
    st.markdown(saut3, unsafe_allow_html=True)

    #Affichage des caractéristiques de la reco 1
    with st.container(border=True):
        col1, col2= st.columns([0.23,0.77],gap="small")
        with col1:
            if df.loc[index[0][1], "poster_link"] == '0' or type(df.loc[index[0][1], "poster_link"]) == float:
                pass
            else:
                st.image(df.loc[index[0][1], "poster_link"])
        
        with col2:
            selectl1 = f"<p style='font-weight: bold; font-size: 20px;line-height: 1;'>{df.loc[index[0][1], 'movie_title']}</p>"
            st.markdown(selectl1, unsafe_allow_html=True)
            if df.loc[index[0][1], 'awards'] == '0' or type(df.loc[index[0][1], 'awards']) == float:
                selectl2 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][1], 'director_name']}&nbsp; - &nbsp;{df.loc[index[0][1], 'country']}&nbsp; - &nbsp;{str(int(df.loc[index[0][1], 'title_year']))}</p>"
            else:
                selectl2 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][1], 'director_name']}&nbsp; - &nbsp;{df.loc[index[0][1], 'country']}&nbsp; - &nbsp;{str(int(df.loc[index[0][1], 'title_year']))}&nbsp; - &nbsp;{df.loc[index[0][1], 'awards']}</p>"
            st.markdown(selectl2, unsafe_allow_html=True)
            selectl3 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][1], 'actor_1_name']}&nbsp; - &nbsp;{df.loc[index[0][1], 'actor_2_name']}&nbsp; - &nbsp;{df.loc[index[0][1], 'actor_3_name']}</p>"
            st.markdown(selectl3, unsafe_allow_html=True)
            selectl4 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][1], 'genres']}&nbsp; - &nbsp;{str(df.loc[index[0][1], 'imdb_score'])}&nbsp; - &nbsp;{int(df.loc[index[0][1], 'budget']):,} $</p>"
            st.markdown(selectl4, unsafe_allow_html=True)
            if df.loc[index[0][1], 'plot'] == '0' or type(df.loc[index[0][1], 'plot']) == float:
                pass
            else:
                selectl5 = f"<p style='font-size: 16px;line-height: 1;'>Synopsis : {df.loc[index[0][1], 'plot']}</p>"
                st.markdown(selectl5, unsafe_allow_html=True)
            selectl6=f"<br>"
            st.markdown(selectl6, unsafe_allow_html=True)

    #Affichage des caractéristiques de la reco 2
        col1, col2= st.columns([0.23,0.77],gap="small")
        with col1:
            if df.loc[index[0][2], "poster_link"] == '0' or type(df.loc[index[0][2], "poster_link"]) == float:
                pass
            else:
                st.image(df.loc[index[0][2], "poster_link"])
        
        with col2:
            selectl1 = f"<p style='font-weight: bold; font-size: 20px;line-height: 1;'>{df.loc[index[0][2], 'movie_title']}</p>"
            st.markdown(selectl1, unsafe_allow_html=True)
            if df.loc[index[0][2], 'awards'] == '0' or type(df.loc[index[0][2], 'awards']) == float:
                selectl2 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][2], 'director_name']}&nbsp; - &nbsp;{df.loc[index[0][2], 'country']}&nbsp; - &nbsp;{str(int(df.loc[index[0][2], 'title_year']))}</p>"
            else:
                selectl2 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][2], 'director_name']}&nbsp; - &nbsp;{df.loc[index[0][2], 'country']}&nbsp; - &nbsp;{str(int(df.loc[index[0][2], 'title_year']))}&nbsp; - &nbsp;{df.loc[index[0][2], 'awards']}</p>"
            st.markdown(selectl2, unsafe_allow_html=True)
            selectl3 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][2], 'actor_1_name']}&nbsp; - &nbsp;{df.loc[index[0][2], 'actor_2_name']}&nbsp; - &nbsp;{df.loc[index[0][2], 'actor_3_name']}</p>"
            st.markdown(selectl3, unsafe_allow_html=True)
            selectl4 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][2], 'genres']}&nbsp; - &nbsp;{str(df.loc[index[0][2], 'imdb_score'])}&nbsp; - &nbsp;{int(df.loc[index[0][2], 'budget']):,} $</p>"
            st.markdown(selectl4, unsafe_allow_html=True)
            if df.loc[index[0][2], 'plot'] == '0' or type(df.loc[index[0][2], 'plot']) == float:
                pass
            else:
                selectl5 = f"<p style='font-size: 16px;line-height: 1;'>Synopsis : {df.loc[index[0][2], 'plot']}</p>"
                st.markdown(selectl5, unsafe_allow_html=True)
            selectl6=f"<br>"
            st.markdown(selectl6, unsafe_allow_html=True)

    #Affichage des caractéristiques de la reco 3
        col1, col2= st.columns([0.23,0.77],gap="small")
        with col1:
            if df.loc[index[0][3], "poster_link"] == '0' or type(df.loc[index[0][3], "poster_link"]) == float:
                pass
            else:
                st.image(df.loc[index[0][3], "poster_link"])
        
        with col2:
            selectl1 = f"<p style='font-weight: bold; font-size: 20px;line-height: 1;'>{df.loc[index[0][3], 'movie_title']}</p>"
            st.markdown(selectl1, unsafe_allow_html=True)
            if df.loc[index[0][3], 'awards'] == '0' or type(df.loc[index[0][3], 'awards']) == float:
                selectl2 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][3], 'director_name']}&nbsp; - &nbsp;{df.loc[index[0][3], 'country']}&nbsp; - &nbsp;{str(int(df.loc[index[0][3], 'title_year']))}</p>"
            else:
                selectl2 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][3], 'director_name']}&nbsp; - &nbsp;{df.loc[index[0][3], 'country']}&nbsp; - &nbsp;{str(int(df.loc[index[0][3], 'title_year']))}&nbsp; - &nbsp;{df.loc[index[0][3], 'awards']}</p>"
            st.markdown(selectl2, unsafe_allow_html=True)
            selectl3 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][3], 'actor_1_name']}&nbsp; - &nbsp;{df.loc[index[0][3], 'actor_2_name']}&nbsp; - &nbsp;{df.loc[index[0][3], 'actor_3_name']}</p>"
            st.markdown(selectl3, unsafe_allow_html=True)
            selectl4 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][3], 'genres']}&nbsp; - &nbsp;{str(df.loc[index[0][3], 'imdb_score'])}&nbsp; - &nbsp;{int(df.loc[index[0][3], 'budget']):,} $</p>"
            st.markdown(selectl4, unsafe_allow_html=True)
            if df.loc[index[0][3], 'plot'] == '0' or type(df.loc[index[0][3], 'plot']) == float:
                pass
            else:
                selectl5 = f"<p style='font-size: 16px;line-height: 1;'>Synopsis : {df.loc[index[0][3], 'plot']}</p>"
                st.markdown(selectl5, unsafe_allow_html=True)
            selectl6=f"<br>"
            st.markdown(selectl6, unsafe_allow_html=True)

    #Affichage des caractéristiques de la reco 4
        col1, col2= st.columns([0.23,0.77],gap="small")
        with col1:
            if df.loc[index[0][4], "poster_link"] == '0' or type(df.loc[index[0][4], "poster_link"]) == float:
                pass
            else:
                st.image(df.loc[index[0][4], "poster_link"])
        
        with col2:
            selectl1 = f"<p style='font-weight: bold; font-size: 20px;line-height: 1;'>{df.loc[index[0][4], 'movie_title']}</p>"
            st.markdown(selectl1, unsafe_allow_html=True)
            if df.loc[index[0][4], 'awards'] == '0' or type(df.loc[index[0][4], 'awards']) == float:
                selectl2 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][4], 'director_name']}&nbsp; - &nbsp;{df.loc[index[0][4], 'country']}&nbsp; - &nbsp;{str(int(df.loc[index[0][4], 'title_year']))}</p>"
            else:
                selectl2 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][4], 'director_name']}&nbsp; - &nbsp;{df.loc[index[0][4], 'country']}&nbsp; - &nbsp;{str(int(df.loc[index[0][4], 'title_year']))}&nbsp; - &nbsp;{df.loc[index[0][4], 'awards']}</p>"
            st.markdown(selectl2, unsafe_allow_html=True)
            selectl3 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][4], 'actor_1_name']}&nbsp; - &nbsp;{df.loc[index[0][4], 'actor_2_name']}&nbsp; - &nbsp;{df.loc[index[0][4], 'actor_3_name']}</p>"
            st.markdown(selectl3, unsafe_allow_html=True)
            selectl4 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][4], 'genres']}&nbsp; - &nbsp;{str(df.loc[index[0][4], 'imdb_score'])}&nbsp; - &nbsp;{int(df.loc[index[0][4], 'budget']):,} $</p>"
            st.markdown(selectl4, unsafe_allow_html=True)
            if df.loc[index[0][4], 'plot'] == '0' or type(df.loc[index[0][4], 'plot']) == float:
                pass
            else:
                selectl5 = f"<p style='font-size: 16px;line-height: 1;'>Synopsis : {df.loc[index[0][4], 'plot']}</p>"
                st.markdown(selectl5, unsafe_allow_html=True)
            selectl6=f"<br>"
            st.markdown(selectl6, unsafe_allow_html=True)

    #Affichage des caractéristiques de la reco 5 
        col1, col2= st.columns([0.23,0.77],gap="small")
        with col1:
            if df.loc[index[0][5], "poster_link"] == '0' or type(df.loc[index[0][5], "poster_link"]) == float:
                pass
            else:
                st.image(df.loc[index[0][5], "poster_link"])
        
        with col2:
            selectl1 = f"<p style='font-weight: bold; font-size: 20px;line-height: 1;'>{df.loc[index[0][5], 'movie_title']}</p>"
            st.markdown(selectl1, unsafe_allow_html=True)
            if df.loc[index[0][5], 'awards'] == '0' or type(df.loc[index[0][5], 'awards']) == float:
                selectl2 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][5], 'director_name']}&nbsp; - &nbsp;{df.loc[index[0][5], 'country']}&nbsp; - &nbsp;{str(int(df.loc[index[0][5], 'title_year']))}</p>"
            else:
                selectl2 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][5], 'director_name']}&nbsp; - &nbsp;{df.loc[index[0][5], 'country']}&nbsp; - &nbsp;{str(int(df.loc[index[0][5], 'title_year']))}&nbsp; - &nbsp;{df.loc[index[0][5], 'awards']}</p>"
            st.markdown(selectl2, unsafe_allow_html=True)
            selectl3 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][5], 'actor_1_name']}&nbsp; - &nbsp;{df.loc[index[0][5], 'actor_2_name']}&nbsp; - &nbsp;{df.loc[index[0][5], 'actor_3_name']}</p>"
            st.markdown(selectl3, unsafe_allow_html=True)
            selectl4 = f"<p style='font-size: 16px;line-height: 1;'>{df.loc[index[0][5], 'genres']}&nbsp; - &nbsp;{str(df.loc[index[0][5], 'imdb_score'])}&nbsp; - &nbsp;{int(df.loc[index[0][5], 'budget']):,} $</p>"
            st.markdown(selectl4, unsafe_allow_html=True)
            if df.loc[index[0][5], 'plot'] == '0' or type(df.loc[index[0][5], 'plot']) == float:
                pass
            else:
                selectl5 = f"<p style='font-size: 16px;line-height: 1;'>Synopsis : {df.loc[index[0][5], 'plot']}</p>"
                st.markdown(selectl5, unsafe_allow_html=True)
            selectl6=f"<br>"
            st.markdown(selectl6, unsafe_allow_html=True)
                


def programme_dashboard():

    #Mise en forme et tire
    st.title(':blue[Tableau de bord BDD Movies]')

    #import des données
    movies=pd.read_csv("final_movie_dataset_omdb.csv")

    #Calcul de la colonne ROI et remplissage des valeurs vides par 0
    movies.gross.fillna(0,inplace=True)
    movies["ROI"]=(movies["gross"]/movies["budget"]).round(2)

    #Initialisation des filtres quali
    options_director = pd.concat([pd.Series(['All']),pd.Series(list(set(list(movies.director_name)))).sort_values()])
    options_actor= pd.concat([pd.Series(['All']),pd.Series(list(set(list(movies.actor_1_name)+list(movies.actor_2_name)+list(movies.actor_3_name)))).sort_values()])
    options_language=pd.concat([pd.Series(['All']),pd.Series(list(set(list(movies.language)))).sort_values()])
    options_country=pd.concat([pd.Series(['All']),pd.Series(list(set(list(movies.country)))).sort_values()])
    options_genre=['All'] + sorted(list(movies.columns[29:55]))

    filtered_movies=movies
    
    #Création de la colonne Acteurs (concaténation acteur 1,2 et 3)
    filtered_movies['Acteurs'] = filtered_movies['actor_1_name'] + ' / ' + filtered_movies['actor_2_name'] + ' / ' + filtered_movies['actor_3_name']

    #Création des filtres
    col1, col2, col3= st.columns([0.25,0.25,0.5],gap="large")

    with col1:   
        #Filtre selection nombre de lignes visibles
        n_list = [i for i in range(5, 51, 5)]
        n=st.selectbox("Nombre de lignes à afficher", n_list, index=3)  

        #Filtre Top/Flop
        min_max=st.selectbox("Classement Min/Max",["Max" , "Min"]) 

        #Filtre Type Classement
        classement=st.selectbox("Classement par",["Budget","ROI","Score IMDb"]) 

    with col2:
        #Filtre réalisateur
        filtered_director=st.selectbox("Réalisateur",options_director)
        if filtered_director != 'All':
            filtered_movies = filtered_movies.loc[filtered_movies.director_name == filtered_director]
        
        #Filtre acteur principal
        filtered_actor=st.selectbox("Acteur",options_actor)
        if filtered_actor != 'All':
            filtered_movies = filtered_movies.loc[(filtered_movies.actor_1_name == filtered_actor) | (filtered_movies.actor_2_name == filtered_actor) | (filtered_movies.actor_3_name == filtered_actor)] 

        #Filtre genre
        filtered_genre=st.selectbox("Genre",options_genre)
        if filtered_genre != 'All':
            filtered_movies = filtered_movies.loc[filtered_movies[filtered_genre] == 1] 

        #Filtre pays
        filtered_country=st.selectbox("Pays",options_country)
        if filtered_country != 'All':
            filtered_movies = filtered_movies.loc[filtered_movies.country == filtered_country]

        #Filtre langue
        filtered_language=st.selectbox("Langue",options_language)
        if filtered_language != 'All':
            filtered_movies = filtered_movies.loc[filtered_movies.language == filtered_language]

    with col3:
            #Filtre année
        min_year = movies["title_year"].min()
        max_year = movies["title_year"].max()
        step = (max_year - min_year) / 100
        filtred_year= st.slider("Année film", min_year, max_year,value=(min_year, max_year),step=step)
        filtered_movies = filtered_movies[filtered_movies["title_year"].between(*filtred_year)]

        #Filtre Budget
        min_budget = movies["budget"].min()
        max_budget = movies["budget"].max()
        step = (max_budget - min_budget) / 100
        filtred_budget= st.slider("Budget ($)", min_value=min_budget, max_value=max_budget, value=(min_budget, max_budget),step=step)
        filtered_movies = filtered_movies[filtered_movies["budget"].between(*filtred_budget)]

        #Filtre ROI
        min_roi = float(movies["ROI"].min())
        max_roi = float(movies["ROI"].max())
        step = (max_roi - min_roi) / 100
        filtred_roi= st.slider("ROI", min_value=min_roi, max_value=max_roi, value=(min_roi, max_roi),step=step)
        filtered_movies = filtered_movies[filtered_movies["ROI"].between(*filtred_roi)]

        #Filtre imdb score
        min_imdb = movies["imdb_score"].min()
        max_imdb = movies["imdb_score"].max()
        step = (max_imdb - min_imdb) / 100
        filtred_imdb = st.slider("Score IMDb", min_value=min_imdb, max_value=max_imdb, value=(min_imdb, max_imdb),step=step)
        filtered_movies = filtered_movies[filtered_movies["imdb_score"].between(*filtred_imdb)]

    #Saut de ligne
    saut1=f"<br>"
    st.markdown(saut1, unsafe_allow_html=True)

    #labelisation des colonnes
    filtered_movies.rename(columns={'movie_title':'Titre du film','director_name':'Réalisateur','title_year':'Année du film','budget':'Budget','imdb_score':'Score IMDb','movie_imdb_link':'URL IMDB du film'},inplace=True)

    #Affichage des différents charts
    st.subheader(f':blue[Classement des {n} films par {min_max} {classement}]')

    #Application des filtres "Min/Max" , "Nb de lignes à afficher" et "Classement par"
    if min_max=="Max":
        filtered_movies_1=filtered_movies[["Titre du film","Réalisateur","Acteurs","Année du film",'Budget','ROI','Score IMDb','URL IMDB du film']].nlargest(n , classement).sort_values(by=classement,ascending=False)
    elif min_max=="Min" and classement!="ROI":
        filtered_movies_1=filtered_movies[["Titre du film","Réalisateur","Acteurs","Année du film","Budget",'ROI','Score IMDb','URL IMDB du film']].nsmallest(n , classement).sort_values(by=classement,ascending=True)    
    elif min_max=="Min" and classement=="ROI":
        filtered_movies=filtered_movies[filtered_movies['ROI']!=0]
        filtered_movies_1=filtered_movies[["Titre du film","Réalisateur","Acteurs","Année du film","Budget",'ROI','Score IMDb','URL IMDB du film']].nsmallest(n , classement).sort_values(by=classement,ascending=True)

    #Affichage tableau de données
    st.dataframe(filtered_movies_1,hide_index=True,column_config={'URL IMDB du film':st.column_config.LinkColumn()})


    #Affichage des histogrammes de classement
    with st.container(border=True):
        col1, col2, col3= st.columns([1/3,1/3,1/3],gap="medium")

        with col1:
            fig, ax = plt.subplots(figsize=(3, 8))
            sns.barplot(x='Budget', y='Titre du film',color = 'steelblue',edgecolor='black',data=filtered_movies_1)
            ax.set_xlabel('Budget')
            ax.set_ylabel('Film')
            ax.set_title(f'Classement par Budget')
            st.pyplot(fig)

        with col2:
            fig, ax = plt.subplots(figsize=(3, 8))
            sns.barplot(x='ROI', y='Titre du film',color = 'mediumseagreen',edgecolor='black',data=filtered_movies_1)
            ax.set_xlabel('ROI')
            ax.set_ylabel('Film')
            ax.set_title(f'Classement par ROI')
            st.pyplot(fig)

        with col3:
            fig, ax = plt.subplots(figsize=(3, 8))
            sns.barplot(x='Score IMDb', y='Titre du film',color = 'goldenrod',edgecolor='black',data=filtered_movies_1)
            ax.set_xlabel('Score IMDb')
            ax.set_ylabel('Film')
            ax.set_title(f'Classement par Score IMDb')
            st.pyplot(fig)

    #création des valeurs moyennes agrégées par année du film
    filtered_movies_mean=filtered_movies[['Année du film','Budget','ROI','Score IMDb']].groupby('Année du film').mean()
    filtered_movies.rename(columns={'Année du film':'Year'})

    #Affichage des différents charts
    st.subheader(f':blue[Evolution des Budgets, ROI et Score IMDb moyens]')

    #Affichage des graphiques budget, ROI et Score IMDb moyen par année
    with st.container(border=True):
        col1, col2, col3= st.columns([1/3,1/3,1/3],gap="small")

        with col1:
            fig, ax1 = plt.subplots()
            sns.lineplot(x='Année du film', y='Budget', marker='o', color = 'steelblue',data=filtered_movies_mean,ax=ax1,linewidth=2)
            ax2 = ax1.twinx()
            sns.lineplot(x='Année du film', y='ROI', marker='o' , color = 'mediumseagreen',data=filtered_movies_mean,ax=ax2,linewidth=2)
            ax1.set_title('Budget VS ROI moyen par année')
            ax1.set_xlabel('Année')
            ax1.set_ylabel('Budget ($)')
            ax2.set_ylabel('ROI')
            ax1.legend(['Budget'],loc='upper left')
            ax2.legend(['ROI'],loc='upper right')
            st.pyplot(fig)

        with col2:
            fig, ax1 = plt.subplots()
            sns.lineplot(x='Année du film', y='Budget', marker='o', color = 'steelblue',data=filtered_movies_mean,ax=ax1,linewidth=2)
            ax2 = ax1.twinx()
            sns.lineplot(x='Année du film', y='Score IMDb', marker='o' , color = 'goldenrod',data=filtered_movies_mean,ax=ax2,linewidth=2)
            ax1.set_title('Budget VS Score IMDB moyen par année')
            ax1.set_xlabel('Année')
            ax1.set_ylabel('Budget ($)')
            ax2.set_ylabel('Score IMDb')
            ax1.legend(['Budget'],loc='upper left')
            ax2.legend(['Score IMDb'],loc='upper right')
            st.pyplot(fig)

        with col3:
            fig, ax1 = plt.subplots()
            sns.lineplot(x='Année du film', y='ROI', marker='o', color = 'mediumseagreen',data=filtered_movies_mean,ax=ax1,linewidth=2)
            ax2 = ax1.twinx()
            sns.lineplot(x='Année du film', y='Score IMDb', marker='o' , color = 'goldenrod',data=filtered_movies_mean,ax=ax2,linewidth=2)
            ax1.set_title('ROI VS Score IMDB moyen par année')
            ax1.set_xlabel('Année')
            ax1.set_ylabel('ROI')
            ax2.set_ylabel('Score IMDb')
            ax1.legend(['ROI'],loc='upper left')
            ax2.legend(['Score IMDb'],loc='upper right')
            st.pyplot(fig)



if st.session_state["authentication_status"]:
      
    with st.sidebar:
        selection = option_menu(
                menu_title="Menu",
                options = ["CinéFeel", "Dashboard"],
                menu_icon='cast',
                icons=['gear', "list-task"],
            )
    
        # Le bouton de déconnexion
        authenticator.logout("Déconnexion")

    if selection == "CinéFeel":
        programme_cinefeel()

    elif selection == "Dashboard":
        programme_dashboard()

elif st.session_state["authentication_status"] is False:
    st.error("Le username ou le password est/sont incorrect(s)")
elif st.session_state["authentication_status"] is None:
    st.warning('Les champs username et mot de passe doivent être rempli')
