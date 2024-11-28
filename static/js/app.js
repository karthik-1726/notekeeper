// Fetch notes from the server and render them
function fetchNotes() {
    fetch("/api/notes?page=1")
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to fetch notes!");
            }
            return response.json();
        })
        .then(data => {
            renderNotes(data);
        })
        .catch(error => {
            console.error("Error fetching notes:", error);
            showError("Error fetching notes!");
        });
}

// Add a new note
function addNote() {
    const title = document.getElementById("note-title").value;
    const tagline = document.getElementById("note-tagline").value;
    const body = document.getElementById("note-body").value;
    const pinned = document.getElementById("note-pinned").checked;

    if (!title || !body) {
        showError("Title and body are required!");
        return;
    }

    fetch("/api/notes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, tagline, body, pinned })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to add note!");
            }
            return response.json();
        })
        .then(data => {
            showToast("Note added successfully!");
            fetchNotes();
        })
        .catch(error => {
            console.error("Error adding note:", error);
            showError("Error adding note!");
        });
}

// Display error messages
function showError(message) {
    alert(message); // Replace this with a custom error toast if needed
}

// Render notes on the page
function renderNotes({ pinned, unpinned }) {
    const notesGrid = document.getElementById("notes-grid");
    notesGrid.innerHTML = "";

    [...pinned, ...unpinned].forEach(note => {
        const noteDiv = document.createElement("div");
        noteDiv.className = "note";
        noteDiv.innerHTML = `
            <h3>${note.title}</h3>
            <p>${note.tagline}</p>
            <p>${note.body}</p>
        `;
        notesGrid.appendChild(noteDiv);
    });
}

document.addEventListener("DOMContentLoaded", fetchNotes);
