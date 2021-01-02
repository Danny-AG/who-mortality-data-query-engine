CREATE DATABASE who;

\connect who

CREATE TABLE mortality_rates
(
    country text,
    year smallint,
    cause text,
    sex char(1),
    deaths int,
    PRIMARY KEY(country, year, cause, sex)
);