-- CITY GRAPH
SELECT
  a.airport_name || ', ' || a.airport_city as "Origin" ,
  b.airport_name || ', ' || b.airport_city as "Destination"
FROM
( -- origin
  SELECT a.flight_ID, b.airport_city, b.airport_name
  FROM scheduled_flight a
  JOIN airport b
  ON (a.origin_airport_ID=b.airport_ID)
) a
JOIN
( -- destination
  SELECT a.flight_ID, b.airport_city, b.airport_name
  FROM scheduled_flight a
  JOIN airport b
  ON (a.destination_airport_ID=b.airport_ID)
) b
ON (a.flight_ID=b.flight_ID);


-- FLIGHT / PASSENGER
SELECT
a.flight_code as "Flight",
a.flight_dep_date as "Departure Date",
b.pass_lname || ', ' || b.pass_fname AS "Passenger"
FROM
  (SELECT * FROM
    (SELECT a.flight_code, a.flight_dep_date, b.booking_ID
    FROM scheduled_flight a LEFT JOIN itinerary b
    ON (a.flight_ID=b.flight_ID)) a
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
  a.crew_lname || ', ' || a.crew_fname AS "Crew",
  a.crew_role as "Role",
  a.flight_code as "Flight",
  b.airport_city as "Destination",
  a.flight_dep_date || ', ' || a.flight_dep_time AS "Departure",
  a.flight_arrival_date || ', ' || a.flight_arrival_time AS "Arrival"
FROM
  (SELECT * FROM
    (SELECT
      a.crew_ID, a.crew_fname, a.crew_lname, a.crew_role, b.flight_ID
       FROM crew a
    LEFT JOIN crew_assignment b
    ON (a.crew_ID = b.crew_ID)) a
  LEFT JOIN scheduled_flight b
    ON (a.flight_ID=b.flight_ID)) a
LEFT JOIN airport b
ON (a.destination_airport_ID=b.airport_ID);
