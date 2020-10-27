from django.db import connection
from .helpers import FlightRow
import datetime


class QueryList:
    """Queries for the database."""

    def city_country_select():
        """Return list of 2-tuples (city, country)."""
        q = """
        SELECT airport_city, airport_country
        FROM airport
        GROUP BY airport_city, airport_country"""
        cursor = connection.cursor()
        cursor.execute(q)
        city_country = cursor.fetchall()
        cursor.close()
        return city_country

    def flight_select_query(dep_date, origin, destination):
        """Return list of flights as FlightRows."""
        flight_dep_date = dep_date
        q = """SELECT
          a.flight_ID,
          a.flight_code AS "Flight Code",
          a.airport_city || ' (' || a.airport_country || ')' AS "Origin",
          b.airport_city || ' (' || b.airport_country || ')' AS "Destination",
          a.flight_dep_date || ', ' || a.flight_dep_time AS "Departure",
          a.flight_arrival_date || ', ' || a.flight_arrival_time AS "Arrival",
          a.flight_arrival_time - a.flight_dep_time AS "Duration",
          a.flight_cost AS "Cost"
        FROM
        (  -- flight/origin
          SELECT *
          FROM scheduled_flight a
          JOIN airport b
          ON (a.origin_airport_ID=b.airport_ID)
        ) a
        JOIN
        (  -- flight/destination
          SELECT *
          FROM scheduled_flight a
          JOIN airport b
          ON (a.destination_airport_ID=b.airport_ID)
        ) b
        ON (a.flight_ID = b.flight_ID)
        WHERE a.flight_dep_date=%s AND a.airport_city = %s AND b.airport_city=%s;
            """

        cursor = connection.cursor()
        cursor.execute(q, (flight_dep_date, origin, destination))
        flights = cursor.fetchall()
        cursor.close()
        flight_rows = [FlightRow(f) for f in flights]
        # Fix negative values, when arrival is the next day:
        for flight_row in flight_rows:
            if flight_row.flight_duration.total_seconds() < 0:
                d = flight_row.flight_duration + datetime.timedelta(hours=24)
                flight_row.flight_duration = d

        return flight_rows

    def passenger_insert_query(
        pass_fname, pass_lname, pass_mi, pass_bday, pass_gender
    ):
        """Insert a row to the passenger table and return its ID."""
        q = """
        INSERT INTO
            passenger(pass_fname, pass_lname, pass_mi, pass_bday, pass_gender)
        VALUES (%s, %s, %s, %s, %s);

        SELECT currval(pg_get_serial_sequence('passenger','pass_id'));
        """
        cursor = connection.cursor()
        cursor.execute(
            q,
            (pass_fname, pass_lname, pass_mi, pass_bday, pass_gender)
        )
        pass_id = cursor.fetchone()[0]
        cursor.close()
        return pass_id

    def booking_insert_query(booking_date, pass_id):
        """Insert a booking for a passenger,
           return the booking_id."""
        q = """
        INSERT INTO booking(booking_date, pass_id)
        VALUES (%s, %s);

        SELECT currval(pg_get_serial_sequence('booking','booking_id'));
        """
        cursor = connection.cursor()
        cursor.execute(q, (booking_date, pass_id))
        booking_id = cursor.fetchone()
        cursor.close()
        return booking_id

    def booking_addon_map_query(booking_id, addon_ids, addon_quantities):
        """Insert into booking_addon_map for a given booking and
           a list of addon ids and quantities."""
        if len(addon_ids) != len(addon_quantities):
            raise Exception("Invalid addon value.")

        q = """ INSERT INTO booking_addon_map(booking_ID, addon_ID, quantity)
        VALUES (%s, %s, %s);
        """
        cursor = connection.cursor()
        for addon_id, quantity in zip(addon_ids, addon_quantities):
            cursor.execute(q, (booking_id, addon_id, quantity))
        cursor.close()
        return

    def itinerary_insert_query(booking_id, flight_ids):
        """Insert into itinerary for a given booking and a list of
        flight codes and departure dates."""
        q = """
        INSERT INTO itinerary(booking_ID, flight_ID)
        VALUES (%s, %s);
        """
        cursor = connection.cursor()
        for flight_id in flight_ids:
            cursor.execute(q, (booking_id, flight_id))
        cursor.close()
        return
