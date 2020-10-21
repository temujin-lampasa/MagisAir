-- CITY GRAPH
SELECT
  a.route_ID as "route_ID",
  a.airport_city as "Origin",
  b.airport_city as "Destination"
FROM
  (SELECT -- origin
    a.route_ID, b.airport_city
  FROM flight_route a JOIN airport b ON (a.airport_origin=b.airport_ID)) a
JOIN
  (SELECT -- destination
    a.route_ID, b.airport_city
  FROM flight_route a JOIN airport b ON (a.airport_destination=b.airport_ID)) b
ON (a.route_ID = b.route_ID);


-- FLIGHT / PASSENGER
SELECT
a.flight_code as "Flight",
a.flight_dep_date as "Departure Date",
b.pass_lname || ', ' || b.pass_fname AS "Passenger"
FROM
  (SELECT * FROM
    (SELECT a.flight_code, a.flight_dep_date, b.booking_ID
    FROM flight a LEFT JOIN itinerary b
    ON (a.flight_code=b.flight_code AND a. flight_dep_date=b.flight_dep_date)) a
  LEFT JOIN booking b
  ON (a.booking_ID=b.booking_ID)) a
LEFT JOIN passenger b
ON (a.pass_ID = b.pass_ID);

-- PASSENGER / ADDON
SELECT
  a.pass_ID,
  a.pass_lname || ', ' || a.pass_fname AS "Passenger",
  b.addon_description AS "Addon",
  a.quantity AS "Quantity"
FROM
  (SELECT * FROM
    (SELECT a.pass_ID, a.pass_fname, a.pass_lname, b.booking_ID
      FROM passenger a JOIN booking b ON (a.pass_ID=b.pass_ID)) a
  LEFT JOIN booking_addon_map b
  ON (a.booking_ID = b.booking_ID)) a
LEFT JOIN addon b
ON (a.addon_ID = b.addon_ID)
ORDER BY a.pass_ID;

--- CREW ASSIGNMENTS
SELECT
  b.crew_lname || ', ' || b.crew_fname AS "Crew",
  b.crew_role as "Role",
  b.flight_code as "Flight",
  a.airport_city as "Destination",
  b.flight_dep_date || ', ' || b.flight_dep_time AS "Departure",
  b.flight_arrival_date || ', ' || b.flight_arrival_time AS "Arrival"
FROM -- route / dest. city
(SELECT fr.route_ID, ap.airport_city
 FROM flight_route fr JOIN airport ap
 ON (fr.airport_destination = ap.airport_ID)) a
 RIGHT JOIN
(SELECT
  b.crew_fname, b.crew_lname, b.crew_role, a.flight_code,
  a.flight_dep_date, a.flight_dep_time, a.flight_arrival_date,
  a.flight_arrival_time, a.route_ID
FROM -- crew / flight
flight a
RIGHT JOIN
(SELECT * FROM crew c
LEFT JOIN crew_flight_map cfm
ON (c.crew_ID = cfm.crew_ID)) b
ON (a.flight_code=b.flight_code and a.flight_dep_date=b.flight_dep_date)) b
ON (a.route_ID = b.route_ID);
