CREATE TABLE IF NOT EXISTS users (
user_id INTEGER PRIMARY KEY,
fullname TEXT,
user_class TEXT,
phone INTEGER,
email TEXT,
password TEXT
);

CREATE TABLE IF NOT EXISTS interests (
interest_id INTEGER PRIMARY KEY,
interest TEXT,
description TEXT
);

CREATE TABLE IF NOT EXISTS users_interests (
user_id INTEGER,
interest_id INTEGER,
PRIMARY KEY (user_id, interest_id),
FOREIGN KEY (user_id) REFERENCES users(user_id),
FOREIGN KEY (interest_id) REFERENCES interests(interest_id)
);

CREATE TABLE IF NOT EXISTS events (
event_id INTEGER PRIMARY KEY,
interest_id INTEGER,
title TEXT,
description TEXT,
event_date DATE,
location TEXT,
FOREIGN KEY (interest_id) REFERENCES interests(interest_id)
);

CREATE TABLE IF NOT EXISTS users_events (
user_id INTEGER,
event_id INTEGER,
PRIMARY KEY (user_id, event_id),
FOREIGN KEY (user_id) REFERENCES users(user_id),
FOREIGN KEY (event_id) REFERENCES events(event_id)
);