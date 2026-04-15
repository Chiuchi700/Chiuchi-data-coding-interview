SELECT current_database(), current_user;

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'airports'
ORDER BY ordinal_position;

SELECT *
FROM airlines
LIMIT 10;

SELECT *
FROM airports
LIMIT 10;

SELECT *
FROM flights
LIMIT 10;

SELECT *
FROM planes
LIMIT 10;

SELECT *
FROM weather
LIMIT 10;