from flask import Flask, request, jsonify, render_template
from models.recommender import recommend_movies
from database.db import create_tables, get_connection

app = Flask(__name__)
create_tables()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/users", methods=["POST"])
def create_user():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (name, action, drama, comedy, scifi)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["name"],
        data["action"],
        data["drama"],
        data["comedy"],
        data["scifi"]
    ))

    conn.commit()
    user_id = cursor.lastrowid
    conn.close()

    return jsonify({"user_id": user_id})


@app.route("/recommend/<int:user_id>")
def recommend(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT action, drama, comedy, scifi
        FROM users WHERE id = ?
    """, (user_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Usuário não encontrado"}), 404

    user_profile = {
        "action": row[0],
        "drama": row[1],
        "comedy": row[2],
        "scifi": row[3]
    }

    recommendations = recommend_movies(user_profile)
    return jsonify(recommendations)


if __name__ == "__main__":
    app.run(debug=True)
