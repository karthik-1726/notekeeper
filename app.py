from flask import Flask, jsonify, request, render_template
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Database connection function
def get_db_connection():
    try:
        connection = psycopg2.connect(
            dbname="notekeeper_7c09",
            user="notekeeper_7c09_user",
            password="CFRNeEjIsRroI747Crtim2eKnDh7TjWm",
            host="dpg-ct475t3tq21c7391ierg-a",  # External host
            port="5432"
        )
        return connection
    except Exception as e:
        app.logger.error(f"Database connection failed: {e}")
        raise  # Raise the error to ensure the app fails correctly if the connection fails

# Health check
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/notes", methods=["GET"])
def get_notes():
    page = int(request.args.get("page", 1))
    per_page = 6

    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Fetch pinned notes
        cursor.execute("SELECT * FROM notes WHERE pinned = TRUE ORDER BY id DESC")
        pinned_notes = cursor.fetchall()

        # Fetch unpinned notes with pagination
        offset = (page - 1) * per_page
        cursor.execute(
            "SELECT * FROM notes WHERE pinned = FALSE ORDER BY id DESC LIMIT %s OFFSET %s",
            (per_page, offset),
        )
        unpinned_notes = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({"pinned": pinned_notes, "unpinned": unpinned_notes})
    except Exception as e:
        app.logger.error(f"Error fetching notes: {e}")
        return jsonify({"error": "Failed to fetch notes"}), 500

@app.route("/api/notes", methods=["POST"])
def create_note():
    data = request.json
    title = data.get("title")
    tagline = data.get("tagline")
    body = data.get("body")
    pinned = bool(data.get("pinned", False))

    if not title or not body:
        return jsonify({"error": "Title and body are required!"}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO notes (title, tagline, body, pinned) VALUES (%s, %s, %s, %s)",
            (title, tagline, body, pinned),
        )
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Note added successfully!"}), 201
    except Exception as e:
        app.logger.error(f"Error creating note: {e}")
        return jsonify({"error": "Failed to add note"}), 500

@app.route("/api/notes/<int:id>", methods=["PUT"])
def update_note(id):
    data = request.json
    title = data.get("title")
    tagline = data.get("tagline")
    body = data.get("body")
    pinned = bool(data.get("pinned", False))

    if not title or not body:
        return jsonify({"error": "Title and body are required!"}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE notes SET title = %s, tagline = %s, body = %s, pinned = %s WHERE id = %s",
            (title, tagline, body, pinned, id),
        )
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Note updated successfully!"})
    except Exception as e:
        app.logger.error(f"Error updating note: {e}")
        return jsonify({"error": "Failed to update note"}), 500

@app.route("/api/notes/<int:id>", methods=["DELETE"])
def delete_note(id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM notes WHERE id = %s", (id,))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Note deleted successfully!"})
    except Exception as e:
        app.logger.error(f"Error deleting note: {e}")
        return jsonify({"error": "Failed to delete note"}), 500

if __name__ == "__main__":
    app.run(debug=True)
