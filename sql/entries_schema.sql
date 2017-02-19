DROP TABLE IF EXISTS entries;
DROP SEQUENCE IF EXISTS entries_id_seq;
CREATE SEQUENCE entries_id_seq;
CREATE TABLE entries (
  id integer PRIMARY KEY DEFAULT nextval('entries_id_seq'),
  username varchar(80) UNIQUE,
  password varchar(100),
  email varchar(25) UNIQUE,
  first_name varchar(25),
  last_name varchar(25)
);
ALTER SEQUENCE entries_id_seq OWNED BY entries.id;
