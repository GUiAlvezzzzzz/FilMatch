from flask import Flask, request, jsonify, render_template, redirect, session
import sqlite3
import requests
from database.db import create_tables, get_connection
from models.recommender import recommend_movies

TMDB_API_KEY = "b87c198c19ec168812af0faedcfa8129"

app = Flask(__name__)
app.secret_key = "segredo_super_seguro"

create_tables()



# PÁGINA INICIAL (LOGIN)

@app.route("/")
def index():
    return render_template("login.html")



# REGISTRO

@app.route("/register", methods=["POST"])
def register():
    data = request.json

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (name, age, email, password)
            VALUES (?, ?, ?, ?)
        """, (
            data["name"],
            int(data["age"]),
            data["email"],
            data["password"]
        ))

        conn.commit()
        conn.close()

        return jsonify({"success": True})

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email já cadastrado"}), 400



# LOGIN 

@app.route("/login", methods=["POST"])
def login():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM users
        WHERE email = ? AND password = ?
    """, (data["email"], data["password"]))

    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "Credenciais inválidas"}), 401

    session["user_id"] = user[0]

    return jsonify({"success": True})



# RECOMENDADOR (PÁGINA)

@app.route("/recomendador")
def recomendador():
    if "user_id" not in session:
        return redirect("/")

    return render_template("index.html")



# RECOMENDAÇÃO 

@app.route("/recommend", methods=["POST"])
def recommend():


    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Não autenticado"}), 401

    lang = request.args.get("lang", "pt")
    profile = request.json

    tmdb_language = "pt-BR" if lang == "pt" else "en-US"

    movies = recommend_movies(profile, language=tmdb_language)

    return jsonify(movies)



# PLATAFORMAS

@app.route("/providers/<int:movie_id>")
def get_providers(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"

    response = requests.get(url, params={
        "api_key": TMDB_API_KEY
    })

    data = response.json()
    providers = data.get("results", {}).get("BR", {}).get("flatrate", [])

    return jsonify(providers)



# LOGOUT (OPCIONAL)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")



# RUN

if __name__ == "__main__":
    app.run(debug=True)
