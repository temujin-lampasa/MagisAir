from django.db import connection


class QueryList:
    """Queries for the database."""

    def flight_select_query(dep_date, origin, destination):
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
        ON (a.airport_destination=b.airport_id)
        WHERE a.airport_city = '{origin}' AND b.airport_city='{destination}';
            """

        cursor = connection.cursor()
        cursor.execute(q)
        flights = cursor.fetchall()
        cursor.close()
        flight_rows = [FlightRow(f) for f in flights]
        return flight_rows


# Helpers ---
class FlightRow:
    """A single flight row in flight_select_view."""

    def __init__(self, data):
        if len(data) != 7:
            raise Exception("Invalid flight data.")
        self.flight_code = data[0]
        self.airport_origin = data[1]
        self.airport_destination = data[2]
        self.flight_dep_date = data[3]
        self.flight_arrival_date = data[4]
        self.flight_duration = data[5]
        self.flight_cost = data[6]

    # def get_absolute_url(self):
    #     return
