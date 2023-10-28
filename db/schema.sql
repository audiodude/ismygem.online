CREATE TABLE IF NOT EXISTS schedules (
  id BINARY(16) PRIMARY KEY,
  email VARCHAR(255) NOT NULL,
  url VARCHAR(1024) NOT NULL,
  every_secs INTEGER NOT NULL,
  scheduler_key VARCHAR(1024),
  first_failure_timestamp TIMESTAMP
);