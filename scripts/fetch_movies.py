import requests
import json

API_KEY = "b87c198c19ec168812af0faedcfa8129"
URL = "https://api.themoviedb.org/3/movie/popular"

movies = []

for page in range(1, 29):  
    response = requests.get(URL, params={
        "api_key": API_KEY,
        "language": "en-US",
        "page": page
    })
    data = response.json()

    for movie in data["results"]:
        movies.append({
            "title": movie["title"],
            "action": 1,
            "drama": 1,
            "comedy": 1,
            "scifi": 1
        })

with open("data/movies.json", "w", encoding="utf-8") as f:
    json.dump(movies, f, ensure_ascii=False, indent=2)
