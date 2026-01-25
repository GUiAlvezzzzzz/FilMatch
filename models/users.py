import json
import os

USERS_FILE = "data/users.json"


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    os.makedirs("data", exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def create_or_update_user(user_id, profile):
    users = load_users()
    users[user_id] = profile
    save_users(users)
    return users[user_id]


def get_user(user_id):
    users = load_users()
    return users.get(user_id)
