import requests

def get_random_cat_fact():
    response = requests.get("https://catfact.ninja/fact")
    return response.json().get("fact")
