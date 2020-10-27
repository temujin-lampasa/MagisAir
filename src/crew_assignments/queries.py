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
