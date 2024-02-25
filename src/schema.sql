CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    sender_id INT,
    receiver_id INT,
    message TEXT,
    -- other message-related columns
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id)
);

CREATE TABLE profile (
    id SERIAL PRIMARY KEY,
    firstname TEXT,
    lastname TEXT,
    user_id INT,
    message TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE contact (
    id SERIAL PRIMARY KEY,
    user_id INT,
    contact_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (contact_id) REFERENCES users(id)
);

CREATE TABLE photos (
    id SERIAL PRIMARY KEY,
    file_name TEXT, 
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);