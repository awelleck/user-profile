DROP TABLE IF EXISTS chat;
CREATE SEQUENCE chat_id_seq;
CREATE TABLE chat (
  id integer PRIMARY KEY DEFAULT nextval('chat_id_seq'),
  messages varchar(500),
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER SEQUENCE chat_id_seq OWNED BY entries.id;
