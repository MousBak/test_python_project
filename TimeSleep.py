import requests
import time

def request_with_retry(url, params=None, retries=3, backoff_factor=1.0):
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params)

            # Gestion des erreurs HTTP spécifiques
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Too Many Requests
                retry_after = int(response.headers.get('Retry-After', backoff_factor))
                print(f"Trop de requêtes. Pause de {retry_after} secondes.")
                time.sleep(retry_after)
            elif response.status_code in [500, 503]:  # Erreurs Serveur
                print(f"Erreur serveur {response.status_code}. Tentative {attempt + 1} après pause.")
                time.sleep(backoff_factor * (2 ** attempt))  # Exponential backoff
            elif response.status_code in [400, 401, 403, 404]:
                print(f"Erreur client {response.status_code}. Vérifiez la requête.")
                break
            else:
                print(f"Erreur inattendue {response.status_code}.")
                break
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête : {e}")
            time.sleep(backoff_factor * (2 ** attempt))  # Exponential backoff for network issues
    return None
