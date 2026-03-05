from db import get_connection


def create_ticket(name, task, description, user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tickets (name, task, description, user_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """, (name, task, description, user_id))

    ticket_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    return ticket_id


def get_tickets_by_user(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, task, description
        FROM tickets
        WHERE user_id = %s
        ORDER BY id;
    """, (user_id,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    # Return as list of dicts for clean JSON output
    tickets = [
        {"id": r[0], "name": r[1], "task": r[2], "description": r[3]}
        for r in rows
    ]
    return tickets


def update_ticket(ticket_id, name, task, description, user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE tickets
        SET name=%s, task=%s, description=%s
        WHERE id=%s AND user_id=%s;
    """, (name, task, description, ticket_id, user_id))

    rows_affected = cur.rowcount
    conn.commit()

    cur.close()
    conn.close()

    return rows_affected  # Returns 0 if ticket not found or doesn't belong to user


def delete_ticket(ticket_id, user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM tickets
        WHERE id=%s AND user_id=%s;
    """, (ticket_id, user_id))

    rows_affected = cur.rowcount
    conn.commit()

    cur.close()
    conn.close()

    return rows_affected  # Returns 0 if ticket not found or doesn't belong to user
