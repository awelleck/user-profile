--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.1
-- Dumped by pg_dump version 9.6.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: practice; Type: TABLE; Schema: public; Owner: 
--

CREATE TABLE practice (
    username character varying(80),
    password character varying(100),
    email character varying(25),
    first_name character varying(25),
    last_name character varying(25)
);


ALTER TABLE practice OWNER TO ;

--
-- Data for Name: practice; Type: TABLE DATA; Schema: public; Owner: 
--

COPY practice (username, password, email, first_name, last_name) FROM stdin;
\.


--
-- Name: practice practice_email_key; Type: CONSTRAINT; Schema: public; Owner: 
--

ALTER TABLE ONLY practice
    ADD CONSTRAINT practice_email_key UNIQUE (email);


--
-- Name: practice practice_username_key; Type: CONSTRAINT; Schema: public; Owner: 
--

ALTER TABLE ONLY practice
    ADD CONSTRAINT practice_username_key UNIQUE (username);


--
-- Name: practice; Type: ACL; Schema: public; Owner: 
--

GRANT ALL ON TABLE practice TO user_goes_here;


--
-- PostgreSQL database dump complete
--

