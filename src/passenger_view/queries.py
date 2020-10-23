from django.db import connection
from .helpers import FlightRow


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
        """Return list of FlightRows."""
        flight_dep_date = dep_date
        q = """SELECT
          a.flight_code AS "Flight",
          a.airport_city || ' (' || a.airport_country || ')' AS "Origin",
          b.airport_city || ' (' || b.airport_country || ')' AS "Destination",
          a.flight_dep_date || ', ' || a.flight_dep_time AS "Departure",
          a.flight_arrival_date || ', ' || a.flight_arrival_time AS "Arrival",
          a.flight_arrival_time - a.flight_dep_time AS "Duration",
          a.flight_cost AS "Cost"
        FROM
          (SELECT * FROM  -- airport with origin
            (SELECT *
            FROM flight f
            JOIN flight_route fr
            ON (f.route_id=fr.route_id)
            WHERE f.flight_dep_date = %s) a
          JOIN
            airport b
          ON (a.airport_origin = b.airport_id)) a
        JOIN
          airport b
        ON (a.airport_destination=b.airport_id)
        WHERE a.airport_city = %s AND b.airport_city=%s;
            """

        vars = [flight_dep_date, origin, destination]

        cursor = connection.cursor()
        cursor.execute(q, vars)
        flights = cursor.fetchall()
        cursor.close()
        flight_rows = [FlightRow(f) for f in flights]
        return flight_rows

    def passenger_insert_query(
        pass_fname, pass_lname, pass_mi, pass_bday, pass_gender
    ):
        """Insert a row to the passenger table."""
        vars = [pass_fname, pass_lname, pass_mi, pass_bday, pass_gender]
        q = """
        INSERT INTO
            passenger(pass_fname, pass_lname, pass_mi, pass_bday, pass_gender)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor = connection.cursor()
        cursor.execute(q, vars)
        cursor.close()
