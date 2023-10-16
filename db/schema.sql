CREATE TABLE IF NOT EXISTS schedules (
  id BINARY(16) PRIMARY KEY,
  email VARCHAR(255) NOT NULL,
  url VARCHAR(1024) NOT NULL,
  token VARCHAR(28),
  verified BOOLEAN NOT NULL DEFAULT 0,
  every_secs INTEGER NOT NULL,
  last_failure_timestamp TIMESTAMP
);