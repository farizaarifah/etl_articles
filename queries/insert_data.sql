-- Insert dummy data
INSERT INTO articles (title, content, published_at, author_id, created_at, updated_at, deleted_at) VALUES
('First Article', 'Content of the first article', '2023-05-01 10:00:00', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Second Article', 'Content of the second article', '2023-05-02 11:00:00', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Third Article', 'Content of the third article', '2023-05-03 12:00:00', 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Fourth Article', 'Content of the fourth article', '2023-05-04 13:00:00', 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL),
('Fifth Article', 'Content of the fifth article', '2023-05-05 14:00:00', 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL);