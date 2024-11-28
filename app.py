from flask import Flask, jsonify, request, render_template
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Replace with your MySQL root password
        database="notekeeper"
    )

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/notes", methods=["GET"])
def get_notes():
    page = int(request.args.get("page", 1))
    per_page = 6

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Get all pinned notes first
    cursor.execute("SELECT * FROM notes WHERE pinned = 1 ORDER BY id DESC")
    pinned_notes = cursor.fetchall()

    # Get non-pinned notes with pagination
    offset = (page - 1) * per_page
    cursor.execute("SELECT * FROM notes WHERE pinned = 0 ORDER BY id DESC LIMIT %s OFFSET %s", (per_page, offset))
    unpinned_notes = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify({"pinned": pinned_notes, "unpinned": unpinned_notes})

@app.route("/api/notes", methods=["POST"])
def create_note():
    data = request.json
    title = data.get("title")
    tagline = data.get("tagline")
    body = data.get("body")
    pinned = data.get("pinned", 0)

    if not title or not body:
        return jsonify({"error": "Title and body are required!"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("INSERT INTO notes (title, tagline, body, pinned) VALUES (%s, %s, %s, %s)", 
                   (title, tagline, body, pinned))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Note created successfully!"}), 201

@app.route("/api/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    data = request.json
    title = data.get("title")
    tagline = data.get("tagline")
    body = data.get("body")
    pinned = data.get("pinned", 0)

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

@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM notes WHERE id = %s", (note_id,))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Note deleted successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
