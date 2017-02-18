DROP TABLE IF EXISTS chat;
DROP SEQUENCE IF EXISTS chat_id_seq;
CREATE SEQUENCE chat_id_seq;
CREATE TABLE chat (
  id integer PRIMARY KEY DEFAULT nextval('chat_id_seq'),
  username varchar(80),
  messages varchar(500),
  msg_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER SEQUENCE chat_id_seq OWNED BY entries.id;
