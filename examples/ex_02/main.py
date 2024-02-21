import requests
from icecream import ic

def get_random_cat_fact():
    response = requests.get("https://catfact.ninja/fact")
    return response.json().get("fact")

if __name__ == "__main__":
    print(get_random_cat_fact())
