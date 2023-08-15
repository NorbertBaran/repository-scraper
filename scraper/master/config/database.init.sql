CREATE TABLE variables (
    name TEXT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS metadata (
    id SERIAL PRIMARY KEY,
    repository_id Integer,
    url VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS metrics (
    id SERIAL PRIMARY KEY,
    metadata_id Integer REFERENCES metadata(id),
    comment VARCHAR(255)
);