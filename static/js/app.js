let currentPage = 1;

// Set BASE_URL to your deployed backend URL
const BASE_URL = window.location.origin.includes("localhost")
    ? "" // For local testing
    : window.location.origin; // Use Render domain when deployed

// Fetch notes with pagination
function fetchNotes() {
    fetch(`${BASE_URL}/api/notes?page=${currentPage}`)
        .then(response => {
            if (!response.ok) throw new Error("Error fetching notes!");
            return response.json();
        })
        .then(data => {
            // Render notes only if containers exist
            const pinnedContainer = document.getElementById("pinned-notes");
            const unpinnedContainer = document.getElementById("unpinned-notes");

            if (!pinnedContainer || !unpinnedContainer) {
                throw new Error('Required DOM elements for notes not found!');
            }

            renderNotes(data);  // Call render if containers exist
        })
        .catch(error => showError(error.message));
}

// Render pinned and unpinned notes
function renderNotes({ pinned, unpinned }) {
    const pinnedContainer = document.getElementById("pinned-notes");
    const unpinnedContainer = document.getElementById("unpinned-notes");

    // Clear containers before rendering
    pinnedContainer.innerHTML = "";
    unpinnedContainer.innerHTML = "";

    // Render pinned notes
    pinned.forEach(note => {
        pinnedContainer.appendChild(createNoteElement(note));
    });

    // Render unpinned notes
    unpinned.forEach(note => {
        unpinnedContainer.appendChild(createNoteElement(note));
    });
}

// Create a single note element
function createNoteElement(note) {
    const noteDiv = document.createElement("div");
    noteDiv.className = "note";
    noteDiv.innerHTML = `
        <h3>${note.title}</h3>
        <p>${note.tagline}</p>
        <p>${note.body}</p>
        <div class="actions">
            <button class="edit" onclick="editNote(${note.id})">Edit</button>
            <button class="delete" onclick="deleteNote(${note.id})">Delete</button>
        </div>
    `;
    return noteDiv;
}

// Add a new note
function addNote() {
    const title = document.getElementById("note-title").value;
    const tagline = document.getElementById("note-tagline").value;
    const body = document.getElementById("note-body").value;
    const pinned = document.getElementById("note-pinned").checked; // Boolean value

    fetch(`${BASE_URL}/api/notes`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, tagline, body, pinned })
    })
        .then(response => {
            if (!response.ok) throw new Error("Failed to add note!");
            return response.json();
        })
        .then(data => {
            showToast(data.message);
            // After note added, fetch and render the updated list of notes
            fetchNotes();
            clearForm();
        })
        .catch(error => showError(error.message));
}

// Edit an existing note
function editNote(id) {
    const newTitle = prompt("Enter new title:");
    const newTagline = prompt("Enter new tagline:");
    const newBody = prompt("Enter new body:");
    const isPinned = confirm("Is this note pinned?"); // Boolean value

    if (!newTitle || !newBody || !newTagline) return;

    fetch(`${BASE_URL}/api/notes/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: newTitle, tagline: newTagline, body: newBody, pinned: isPinned })
    })
        .then(response => {
            if (!response.ok) throw new Error("Failed to update note!");
            return response.json();
        })
        .then(() => {
            showToast("Note updated successfully!");
            fetchNotes();
        })
        .catch(error => showError(error.message));
}

// Delete a note
function deleteNote(id) {
    if (!confirm("Are you sure you want to delete this note?")) return;

    fetch(`${BASE_URL}/api/notes/${id}`, { method: "DELETE" })
        .then(response => {
            if (!response.ok) throw new Error("Failed to delete note!");
            return response.json();
        })
        .then(() => {
            showToast("Note deleted successfully!");
            fetchNotes();
        })
        .catch(error => showError(error.message));
}

// Show a toast message
function showToast(message, type = "success") {
    const toast = document.getElementById("toast");
    if (toast) {
        toast.textContent = message;
        toast.className = `toast show ${type}`;
        
        setTimeout(() => {
            toast.className = "toast";
        }, 3000); // Toast disappears after 3 seconds
    }
}

// Clear the form after adding a note
function clearForm() {
    document.getElementById("note-title").value = "";
    document.getElementById("note-tagline").value = "";
    document.getElementById("note-body").value = "";
    document.getElementById("note-pinned").checked = false;
}

// Error handling function
function showError(message) {
    showToast(message, "error");
}

// Handle pagination: Next Page
function nextPage() {
    currentPage++;
    fetchNotes();
}

// Handle pagination: Previous Page
function prevPage() {
    if (currentPage > 1) {
        currentPage--;
        fetchNotes();
    }
}

// Load notes when the page is ready
document.addEventListener("DOMContentLoaded", fetchNotes);
