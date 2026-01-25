import random
from services.tmdb import fetch_discover_movies, GENRE_MAP

import random
from services.tmdb import fetch_discover_movies, GENRE_MAP


def score_movie(movie, user_profile):
    score = 0
    movie_genres = movie["genre_ids"]
    matched_genres = 0

    for genre, weight in user_profile.items():
        genre_id = GENRE_MAP[genre]

        if genre_id in movie_genres:
            score += weight * 4
            matched_genres += 1
        else:
            if weight == 0:
                score -= 5  


    if matched_genres == 0:
        return -999

    score += movie["vote_average"] * 0.7
    score += movie["popularity"] * 0.005
    score += random.uniform(-0.3, 0.3)

    return round(score, 2)


def recommend_movies(user_profile, limit=30):
    movies = fetch_discover_movies(pages=6)

    scored = []

    for movie in movies:
        score = score_movie(movie, user_profile)

        if score <= 0:
            continue

        scored.append({
            "title": movie["title"],
            "poster": movie["poster"],
            "vote": movie["vote_average"],
            "score": score
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

    seen = set()
    final = []

    for movie in scored:
        if movie["title"] not in seen:
            seen.add(movie["title"])
            final.append(movie)

        if len(final) == limit:
            break

    return final

