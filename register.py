@app.route("/login", methods=["POST"])
def login():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, age FROM users
        WHERE email = ? AND password = ?
    """, (data["email"], data["password"]))

    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "Credenciais inválidas"}), 401

    return jsonify({
        "user_id": user[0],
        "age": user[1]
    })
