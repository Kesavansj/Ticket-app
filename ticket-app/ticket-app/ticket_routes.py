from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_connection
from ticket_model import (  # Fixed: import directly, not from models.ticket_model
    create_ticket,
    get_tickets_by_user,
    update_ticket,
    delete_ticket
)

ticket_bp = Blueprint("ticket_bp", __name__, url_prefix="/tickets")


# =========================
# CREATE
# =========================
@ticket_bp.route("/", methods=["POST"])
@jwt_required()
def create():
    user_id = get_jwt_identity()
    data = request.json

    if not all(k in data for k in ("name", "task", "description")):
        return jsonify({"error": "name, task, and description are required"}), 400

    ticket_id = create_ticket(
        data["name"],
        data["task"],
        data["description"],
        user_id
    )

    return jsonify({
        "message": "Ticket created successfully",
        "ticket_id": ticket_id
    }), 201


# =========================
# READ
# =========================
@ticket_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_one(id):
    user_id = get_jwt_identity()
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, task, description
        FROM tickets
        WHERE id = %s AND user_id = %s;
    """, (id, user_id))

    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify({"error": "Ticket not found"}), 404

    return jsonify({
        "id": row[0],
        "name": row[1],
        "task": row[2],
        "description": row[3]
    })


# =========================
# UPDATE
# =========================
@ticket_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update(id):
    user_id = get_jwt_identity()
    data = request.json

    if not all(k in data for k in ("name", "task", "description")):
        return jsonify({"error": "name, task, and description are required"}), 400

    updated = update_ticket(
        id,
        data["name"],
        data["task"],
        data["description"],
        user_id
    )

    if updated == 0:
        return jsonify({"error": "Ticket not found"}), 404

    return jsonify({"message": "Ticket updated successfully"})


# =========================
# DELETE
# =========================
@ticket_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    user_id = get_jwt_identity()

    deleted = delete_ticket(id, user_id)

    if deleted == 0:
        return jsonify({"error": "Ticket not found"}), 404

    return jsonify({"message": "Ticket deleted successfully"})
