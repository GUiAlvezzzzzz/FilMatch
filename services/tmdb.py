import requests
import random

API_KEY = "b87c198c19ec168812af0faedcfa8129"
BASE_URL = "https://api.themoviedb.org/3"

GENRE_MAP = {
    "action": 28,
    "drama": 18,
    "comedy": 35,
    "scifi": 878
}


def fetch_discover_movies(pages=6):
    movies = []
    random_pages = random.sample(range(1, 20), pages)

    for page in random_pages:
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            params={
                "api_key": API_KEY,
                "language": "pt-BR",
                "sort_by": "popularity.desc",
                "vote_count.gte": 100,
                "page": page
            }
        )

        if response.status_code != 200:
            continue

        for movie in response.json().get("results", []):
            if not movie.get("poster_path"):
                continue

            movies.append({
                "id": movie["id"],
                "title": movie["title"],
                "genre_ids": movie["genre_ids"],
                "vote_average": movie["vote_average"],
                "popularity": movie["popularity"],
                "poster": f"https://image.tmdb.org/t/p/w300{movie['poster_path']}"
            })

    return movies
