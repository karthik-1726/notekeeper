from flask import Flask, jsonify, request, render_template
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Database connection function
def get_db_connection():
    return psycopg2.connect(
        dbname="notekeeper_7c09",
        user="notekeeper_7c09_user",
        password="CFRNeEjIsRroI747Crtim2eKnDh7TjWm",
        host="dpg-ct475t3tq21c7391ierg-a",
        port="5432"
    )

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/notes", methods=["GET"])
def get_notes():
    try:
        page = int(request.args.get("page", 1))
        per_page = 6

        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Fetch pinned notes
        cursor.execute("SELECT * FROM notes WHERE pinned = TRUE ORDER BY id DESC")
        pinned_notes = cursor.fetchall()

        # Fetch unpinned notes with pagination
        offset = (page - 1) * per_page
        cursor.execute("SELECT * FROM notes WHERE pinned = FALSE ORDER BY id DESC LIMIT %s OFFSET %s", (per_page, offset))
        unpinned_notes = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({"pinned": pinned_notes, "unpinned": unpinned_notes})
    except Exception as e:
        print(f"Error fetching notes: {e}")  # Log error for debugging
        return jsonify({"error": "Error fetching notes!"}), 500

@app.route("/api/notes", methods=["POST"])
def create_note():
    data = request.json
    title = data.get("title")
    tagline = data.get("tagline")
    body = data.get("body")
    pinned = data.get("pinned", False)

    if not title or not body:
        return jsonify({"error": "Title and body are required!"}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("INSERT INTO notes (title, tagline, body, pinned) VALUES (%s, %s, %s, %s)", 
                       (title, tagline, body, pinned))
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Note created successfully!"}), 201
    except Exception as e:
        print(f"Error creating note: {e}")  # Log error for debugging
        return jsonify({"error": "Error creating note!"}), 500

@app.route("/api/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    data = request.json
    title = data.get("title")
    tagline = data.get("tagline")
    body = data.get("body")
    pinned = data.get("pinned", False)

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE notes
            SET title = %s, tagline = %s, body = %s, pinned = %s
            WHERE id = %s
        """, (title, tagline, body, pinned, note_id))
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Note updated successfully!"})
    except Exception as e:
        print(f"Error updating note: {e}")  # Log error for debugging
        return jsonify({"error": "Error updating note!"}), 500

@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM notes WHERE id = %s", (note_id,))
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Note deleted successfully!"})
    except Exception as e:
        print(f"Error deleting note: {e}")  # Log error for debugging
        return jsonify({"error": "Error deleting note!"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
