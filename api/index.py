from flask import Flask, request, jsonify, render_template, redirect, session
import sqlite3
import requests
from database.db import create_tables, get_connection
from models.recommender import recommend_movies
import os

app = Flask(__name__)
app.secret_key = "segredo"

TMDB_API_KEY = os.environ.get("TMDB_API_KEY")

create_tables()

@app.route("/")
def index():
    return render_template("login.html")

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

@app.route("/login", methods=["POST"])
def login():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE email=? AND password=?",
        (data["email"], data["password"])
    )

    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "Credenciais inválidas"}), 401

    session["user_id"] = user[0]
    return jsonify({"success": True, "user_id": user[0]})

@app.route("/recomendador")
def recomendador():
    if "user_id" not in session:
        return redirect("/")
    return render_template("index.html")

@app.route("/recommend/<int:user_id>", methods=["POST"])
def recommend(user_id):
    lang = request.args.get("lang", "pt")
    profile = request.json

    tmdb_language = "pt-BR" if lang == "pt" else "en-US"
    movies = recommend_movies(profile, language=tmdb_language)

    return jsonify(movies)

@app.route("/providers/<int:movie_id>")
def get_providers(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"

    response = requests.get(url, params={
        "api_key": TMDB_API_KEY
    })

    data = response.json()
    providers = data.get("results", {}).get("BR", {}).get("flatrate", [])

    return jsonify(providers)
