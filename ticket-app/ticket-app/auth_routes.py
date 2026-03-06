from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from db import get_connection

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/test")
def test():
    return jsonify({"message": "Auth blueprint working"})


# =========================
# REGISTER
# =========================
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE username = %s;", (username,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({"error": "Username already exists"}), 409

    cur.execute("""
        INSERT INTO users (username, password)
        VALUES (%s, %s)
        RETURNING id;
    """, (username, password))

    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "User registered successfully", "user_id": user_id}), 201


# =========================
# LOGIN
# =========================
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


# =========================
# GET ALL USERS
# =========================
@auth_bp.route("/users", methods=["GET"])
def get_all_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, username FROM users ORDER BY id;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    users = [{"id": r[0], "username": r[1]} for r in rows]
    return jsonify(users)


# =========================
# GET PARTICULAR USER
# =========================
@auth_bp.route("/user/<int:id>", methods=["GET"])
def get_user(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, username FROM users WHERE id = %s;", (id,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": row[0],
        "username": row[1]
    })
