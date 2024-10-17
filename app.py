import requests
import time
import streamlit as st
from requests.exceptions import RequestException


# Récupérer la clé API TMDB
TMDB_API_KEY = "f5a3f7f14b4c47781a4e44c2e808692f"

# Fonction pour gérer les erreurs d'API et les tentatives de réessai
def handle_api_errors(func):
    def wrapper(*args, **kwargs):
        max_retries = 5  # Nombre maximum de tentatives
        retry_wait_time = 2  # Temps d'attente entre les tentatives (en secondes)
        retries = 0  # Compteur de tentatives

        while retries < max_retries:
            try:
                response = func(*args, **kwargs)  # Appel de la fonction décorée

                # Vérifier le code de statut de la réponse
                if response.status_code == 200:
                    return response.json()  # Retourner le JSON si la requête est réussie
                elif response.status_code == 429:  # Trop de requêtes
                    print("Trop de requêtes. Attente avant de réessayer...")
                    time.sleep(retry_wait_time)
                elif response.status_code in [500, 503]:  # Erreurs de serveur
                    print(f"Erreur serveur {response.status_code}. Réessayer...")
                    time.sleep(retry_wait_time)
                elif response.status_code in [401, 403]:  # Problèmes d'autorisation
                    return f"Erreur d'autorisation : {response.status_code}. Vérifiez votre clé API."
                elif response.status_code == 404:  # Ressource non trouvée
                    return f"Film avec l'ID {kwargs['movie_id']} non trouvé."
                else:
                    return f"Erreur inattendue : {response.status_code}"
            except RequestException as e:
                print(f"Échec de la requête : {e}. Réessayer...")
                time.sleep(retry_wait_time)
            retries += 1  # Incrémenter le compteur de tentatives

        return f"Échec après {max_retries} tentatives."  # Retourner une erreur après épuisement des tentatives

    return wrapper


@handle_api_errors
def make_tmdb_request(movie_id):
    """
    Effectue une requête à l'API TMDB pour obtenir des informations sur un film.

    :param movie_id: ID du film à rechercher
    :return: Réponse de l'API
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": TMDB_API_KEY}
    return requests.get(url, params=params)


def get_movie_details(movie_id):
    """
    Récupère les détails d'un film à partir de l'API TMDB.

    :param movie_id: ID du film
    :return: Dictionnaire contenant les détails du film
    """
    data = make_tmdb_request(movie_id)

    # Vérifier si la réponse est un dictionnaire
    if isinstance(data, dict):
        movie_details = {
            "title": data.get("title"),
            "release_date": data.get("release_date"),
            "genres": [genre['name'] for genre in data.get("genres", [])],
            "popularity": data.get("popularity"),
            "vote_average": data.get("vote_average")
        }
        return movie_details
    else:
        return data  # Retourner les erreurs en cas d'échec

# Utilisation de la mise en cache avec un TTL d'une heure
@st.cache_data(ttl=3600)  # Cache pour une durée d'une heure
def get_movie_details_cached(movie_id):
    """
    Récupère les détails d'un film en utilisant un cache.

    :param movie_id: ID du film
    :return: Détails du film
    """
    return get_movie_details(movie_id)

# Interface Streamlit
st.title("Détails des films")

# Récupération de l'ID du film via l'interface utilisateur
movie_id = st.text_input("Entrez l'ID du film", "550")

# Bouton pour obtenir les détails du film
if st.button("Obtenir les détails du film"):
    #details = get_movie_details_cached(movie_id)
  '''''  if st.button("Détails du film"):
        if
            not movie_id: st.error("Entrer un ID de film.")
        else:
        result = asyncio.run(get_movie_details(movie_id))
            if "error" in result:
        st.error(result["error"])        else:
        st.write(f"**Title**: {result['title']}")
        st.write(f"**Release Date**: {result['release_date']}")
        st.write(f"**Genres**: {', '.join(result['genres'])}")
        st.write(f"**Popularity**: {result['popularity']}")
        st.write(f"**Average Vote**: {result['vote_average']}")
else:
st.error("Impossible de récupérer les détails du film.")
else:
st.warning("Veuillez entrer un ID de film valide.")'''

if st.button("Rechercher") and movie_id:
    movie_data = get_movie_details(movie_id)

    if movie_data:
        # Afficher les détails du film
        st.subheader("Détails du Film")
        st.write(f"**Titre :** {movie_data.get('title')}")
        st.write(f"**Date de sortie :** {movie_data.get('release_date')}")
        st.write(f"**Genres :** {', '.join(movie_data['genres'])}")
        st.write(f"**Popularité :** {movie_data.get('popularity')}")
        st.write(f"**Note moyenne :** {movie_data.get('vote_average')}")
    elif "error" in movie_data:
        st.error("Impossible de récupérer les détails du film.")
    else:
        st.warning("Veuillez entrer un ID de film valide.")