from django.db import connection


class QueryList:

    def assigned_flights_query(crew_ID):
        """Get the assigned flights of a crew member.
        Format: (flight code, destination, departure, arrival)"""
        q = """
        SELECT
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
        ON (a.destination_airport_ID=b.airport_ID)
        WHERE a.crew_id = %s;"""

        cursor = connection.cursor()
        cursor.execute(q, (crew_ID,))
        assigned_flights = cursor.fetchall()
        return assigned_flights

    def assigned_crew_query(flight_ID):
        """Get the assigned crew for a flight.
        Format: (fname, lname, role)"""
        q = """
        SELECT
        b.crew_fname,
        b.crew_lname,
        b.crew_role
        FROM
          (
            SELECT *
            FROM scheduled_flight a
            JOIN crew_assignment b
            ON (a.flight_ID = b.flight_ID)
            WHERE a.flight_ID=%s
          ) a
        JOIN crew b
        ON (a.crew_ID=b.crew_ID);
        """

        cursor = connection.cursor()
        cursor.execute(q, (flight_ID,))
        assigned_crew = cursor.fetchall()
        return assigned_crew

    def passenger_list_query(flight_ID):
        """Return a list of passengers for a specific flight."""
        q = """
        SELECT
        b.pass_lname || ', ' || b.pass_fname AS "Passenger"
        FROM
          (SELECT * FROM
            (SELECT a.flight_ID, a.flight_code, a.flight_dep_date, b.booking_ID
            FROM scheduled_flight a LEFT JOIN itinerary b
            ON (a.flight_ID=b.flight_ID)) a
          LEFT JOIN booking b
          ON (a.booking_ID=b.booking_ID)) a
        LEFT JOIN passenger b
        ON (a.pass_ID = b.pass_ID)
        WHERE a.flight_ID=%s;"""
        cursor = connection.cursor()
        cursor.execute(q, (flight_ID,))
        passenger_list = cursor.fetchall()
        return passenger_list
