-- Create the 'notekeeper' database if it does not already exist
-- In PostgreSQL, the database is created and managed separately.
-- If you have already created your database, you can skip this part.

-- CREATE DATABASE notekeeper;

-- Connect to the 'notekeeper' database
-- \c notekeeper;  -- This is a command you would use in psql to connect to the database

-- Create the 'notes' table
CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,           -- 'SERIAL' for auto-increment in PostgreSQL
    title VARCHAR(255) NOT NULL,      -- Title of the note (cannot be null)
    tagline VARCHAR(255),             -- Optional tagline
    body TEXT NOT NULL,               -- The main content of the note (cannot be null)
    pinned BOOLEAN DEFAULT FALSE,     -- Use 'BOOLEAN' for true/false values
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Automatically set timestamp on creation
);

-- Add any additional indexes or constraints as necessary
-- Example: Adding an index on the title for quicker searches (optional)
-- CREATE INDEX idx_notes_title ON notes (title);
