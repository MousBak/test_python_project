import requests
from cachetools import TTLCache

# Cache avec TTL d'une heure (3600 secondes) et une taille maximale de 100 éléments
cache = TTLCache(maxsize=100, ttl=3600)

def get_data_with_cache(url, params=None):
    """
    Récupère les données d'une URL en utilisant un cache.
    Si les données sont en cache et que le TTL n'a pas expiré, elles sont renvoyées depuis le cache.
    Sinon, une nouvelle requête est effectuée, et les données sont mises en cache.

    :param url: L'URL de l'API à appeler
    :param params: Les paramètres à inclure dans la requête (facultatif)
    :return: Les données sous forme de dictionnaire ou None en cas d'erreur
    """
    if url in cache:
        print(f"Cache utilisé pour {url}")
        return cache[url]
    else:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            cache[url] = data
            print(f"Données récupérées depuis l'API pour {url}")
            return data
        else:
            print(f"Erreur {response.status_code} pour l'URL : {url}")
            return None

# Exécuter pour chaque URL individuellement pour voir le cache en action
urls = [
    "https://jsonplaceholder.typicode.com/todos/1",
    "https://jsonplaceholder.typicode.com/todos/2"
]

# Récupérer les données de chaque URL
for url in urls:
    print(get_data_with_cache(url))  # Première requête (sans cache)
    print(get_data_with_cache(url))  # Deuxième requête (utilise le cache)
