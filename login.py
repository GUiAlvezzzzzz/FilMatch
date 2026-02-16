@app.route("/register", methods=["POST"])
def register():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (name, age, email, password, action, drama, comedy, scifi)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["name"],
        data["age"],
        data["email"],
        data["password"], 
        data["action"],
        data["drama"],
        data["comedy"],
        data["scifi"]
    ))

    conn.commit()
    user_id = cursor.lastrowid
    conn.close()

    return jsonify({"user_id": user_id})
