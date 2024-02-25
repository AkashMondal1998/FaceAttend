CREATE TABLE persons(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    emp_id TEXT NOT NULL,
    face_encoding BLOB UNIQUE NOT NULL
);

CREATE TABLE attendance(
    id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    person_id INTEGER NOT NULL,
    FOREIGN KEY (person_id) REFERENCES persons(id)
)