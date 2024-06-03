-- Create the table
CREATE TABLE articles (
    id TEXT PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    published_at TIMESTAMP,
    author_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP with time zone
);

