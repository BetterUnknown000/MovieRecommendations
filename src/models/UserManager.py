

import json
import os
import hashlib

class UserManager:
    def __init__(self, path="../data/users.json"):
        self.path = path
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump({}, f)

        with open(self.path, "r") as f:
            return json.load(f)

    def save_users(self):
        with open(self.path, "w") as f:
            json.dump(self.users, f, indent=4)

    def generate_user_id(self):
        if not self.users:
            return 1
        else:
            existing_ids = [int(uid) for uid in self.users.keys()]
            return max(existing_ids) + 1

    def add_user(self, username, password, liked_genres, liked_tags):
        user_id = self.generate_user_id()
        hashed_password = self.hash_password(password)
        self.users[user_id] = {
            "username": username,
            "password": hashed_password,
            "liked_genres": liked_genres,
            "liked_tags": liked_tags,
            "watched_movies": []
        }
        self.save_users()
        return user_id

    def authenticate_user(self, user_id, password):
        hashed_password = self.hash_password(password)
        user = self.users.get(str(user_id), None)
        if user and user["password"] == hashed_password:
            return user
        return None

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()