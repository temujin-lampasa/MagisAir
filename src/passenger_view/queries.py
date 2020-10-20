from django.db import connection


class QueryList:
    """Queries for the database."""

    def flight_dep_date_query(self, dep_date):
        flight_dep_date = dep_date
        q = f"""SELECT
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
            WHERE f.flight_dep_date = '{flight_dep_date}') a
          JOIN
            airport b
          ON (a.airport_origin = b.airport_id)) a
        JOIN
          airport b
        ON (a.airport_destination=b.airport_id);
            """

        cursor = connection.cursor()
        cursor.execute(q)
        flights = cursor.fetchall()
        cursor.close()
        processed_flights = [process_flight_data(f) for f in flights]
        return processed_flights


# Helpers ---
def process_flight_data(self, data):
    """Make a dictionary for flight data."""
    fields = [
        'flight_code',
        'airport_origin',
        'airport_destination',
        'flight_dep_date',
        'flight_arrival_date',
        'flight_duration',
        'flight_cost'
        ]
    flight_data = {}
    if len(fields) == len(data):
        for i in range(len(data)):
            flight_data[fields[i]] = data[i]
    else:
        raise Exception('Invalid flight data.')
