import random
from services.tmdb import fetch_discover_movies, GENRE_MAP


def score_movie(movie, user_profile):
    score = 0
    movie_genres = movie.get("genre_ids", [])
    matched_genres = 0

    for genre, weight in user_profile.items():
        genre_id = GENRE_MAP.get(genre)

        if not genre_id:
            continue

        
        if weight == 0 and genre_id in movie_genres:
            return -999

        if genre_id in movie_genres:
            score += weight * 5
            matched_genres += 1
        else:
            score -= weight * 1.5 

    if matched_genres == 0:
        return -999

   
    score += movie.get("vote_average", 0) * 0.5
    score += random.uniform(-1.2, 1.2)  

    return round(score, 2)



def recommend_movies(user_profile, limit=60, language="pt-BR"):
    movies = fetch_discover_movies(pages=25, language=language)

    if not movies:
        return []

    scored = []

    for movie in movies:
        score = score_movie(movie, user_profile)

        if score <= 0:
            continue

        scored.append({
            "id": movie.get("id"),
            "title": movie.get("title"),
            "overview": movie.get("overview"),
            "release_date": movie.get("release_date"),
            "poster": movie.get("poster"),
            "vote": movie.get("vote_average"),
            "score": score
        })

   
    scored.sort(key=lambda x: x["score"], reverse=True)

   
    top_pool = scored[:120]

    
    final = random.sample(top_pool, min(limit, len(top_pool)))

    return final

