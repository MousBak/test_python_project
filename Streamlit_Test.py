import unittest

import streamlit as st
import requests
from cachetools import TTLCache

# Cache avec expiration d'une heure
cache = TTLCache(maxsize=100, ttl=3600)


def get_movie_details(movie_id, API_KEY='f5a3f7f14b4c47781a4e44c2e808692f'):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        'api_key': API_KEY,
        'language': 'fr-FR'
    }

    if url in cache:
        return cache[url]
    else:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            cache[url] = data
            return data
        else:
            return None


# Interface Streamlit
st.title("Détails du Film")
movie_id = st.text_input("Entrez l'ID du film", "550")

if st.button("Afficher les détails"):
    details = get_movie_details(movie_id)
    if details:
        st.write(details)
    else:
        st.write("Erreur lors de la récupération des données.")


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # si tu veux tester que True est égal à True


if __name__ == '__main__':
    unittest.main()
