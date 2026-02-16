import requests

API_KEY = "b87c198c19ec168812af0faedcfa8129"

GENRE_MAP = {
    "action": 28,
    "drama": 18,
    "comedy": 35,
    "scifi": 878
}


def fetch_discover_movies(pages=5, language="pt-BR"):
    movies = []

    for page in range(1, pages + 1):
        res = requests.get(
            "https://api.themoviedb.org/3/discover/movie",
            params={
                "api_key": API_KEY,
                "language": language,
                "page": page
            }
        )

        data = res.json()

        for movie in data.get("results", []):
            movies.append({
                "id": movie["id"],
                "title": movie["title"],
                "overview": movie.get("overview"),
                "release_date": movie.get("release_date"),
                "genre_ids": movie["genre_ids"],
                "vote_average": movie["vote_average"],
                "popularity": movie["popularity"],
                "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
            })


    return movies
