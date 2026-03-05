from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from db import get_connection

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/test")
def test():
    return jsonify({"message": "Auth blueprint working"})


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    conn = get_connection()
    cur = conn.cursor()

    # Check if user already exists
    cur.execute("SELECT id FROM users WHERE username = %s;", (username,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({"error": "Username already exists"}), 409

    cur.execute("""
        INSERT INTO users (username, password)
        VALUES (%s, %s)
        RETURNING id;
    """, (username, password))  # Hash passwords in production!

    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "User registered successfully", "user_id": user_id}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE username = %s AND password = %s;", (username, password))
    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user[0]))
    return jsonify({"access_token": access_token})
