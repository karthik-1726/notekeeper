let currentPage = 1;

function fetchNotes() {
    fetch(`/api/notes?page=${currentPage}`)
        .then(response => response.json())
        .then(data => renderNotes(data))
        .catch(error => showError("Error fetching notes!"));
}

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
            <div class="actions">
                <button class="edit" onclick="editNote(${note.id})">Edit</button>
                <button class="delete" onclick="deleteNote(${note.id})">Delete</button>
            </div>
        `;
        notesGrid.appendChild(noteDiv);
    });
}

function addNote() {
    const title = document.getElementById("note-title").value;
    const tagline = document.getElementById("note-tagline").value;
    const body = document.getElementById("note-body").value;
    const pinned = document.getElementById("note-pinned").checked ? 1 : 0;

    fetch("/api/notes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, tagline, body, pinned })
    })
        .then(response => {
            if (!response.ok) 
                    throw new Error("Failed to add note!");
            return response.json();
        })
        .then((data) => {
            showToast(data.message);
            fetchNotes();
            clearForm();
        })
        .catch(error => showError("Error adding note!"));
}

function editNote(id) {
    const newTitle = prompt("Enter new title:");
    const newTagline = prompt("Enter new tagline:");
    const newBody = prompt("Enter new body:");
    if (!newTitle || !newBody || !newTagline) return;

    fetch(`/api/notes/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: newTitle, tagline: newTagline, body: newBody, pinned: 0 })
    })
        .then(response => {
            if (!response.ok) throw new Error("Failed to update note!");
            showToast("Note updated successfully!");
            fetchNotes();
        })
        .catch(error => showError("Error updating note!"));
}

function deleteNote(id) {
    if (!confirm("Are you sure you want to delete this note?")) return;

    fetch(`/api/notes/${id}`, { method: "DELETE" })
        .then(response => {
            if (!response.ok) throw new Error("Failed to delete note!");
            showToast("Note deleted successfully!");
            fetchNotes();
        })
        .catch(error => showError("Error deleting note!"));
}

function showToast(message, type = "success") {
    const toast = document.getElementById("toast");
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    
    setTimeout(() => {
        toast.className = "toast";
    }, 3000); // Toast disappears after 3 seconds
}

function showError(message) {
    showToast(message, "error");
}


function clearForm() {
    document.getElementById("note-title").value = "";
    document.getElementById("note-tagline").value = "";
    document.getElementById("note-body").value = "";
    document.getElementById("note-pinned").checked = false;
}

function showError(message) {
    alert(message);
}

function nextPage() {
    currentPage++;
    fetchNotes();
}

function prevPage() {
    if (currentPage > 1) {
        currentPage--;
        fetchNotes();
    }
}

document.addEventListener("DOMContentLoaded", fetchNotes);
