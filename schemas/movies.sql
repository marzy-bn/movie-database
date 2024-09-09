CREATE TABLE IF NOT EXISTS movies (
    movieId INTEGER PRIMARY KEY, -- Primary Key will assign a unique ID (1, 2, 3, etc) automatically
    name TEXT,
    rating REAL,
    genre TEXT
);