import datetime
import random

class ValueGenerator:
    def generate_flights(num_routes):
        """Generate 48 flights for each route (2 per hour),
           for the next 5 days.
        Assumptions:
        > airport IDs are from 1 to num_airports inclusive.
        > All flights are 30 min long.
        > Departure and Arrival are all on same day.
        """
        q = """
        INSERT INTO flight(flight_code, flight_dep_date, flight_dep_time,
                           flight_arrival_date, flight_arrival_time, flight_cost,
                           route_ID)
        VALUES
        """

        flight_dep_date = datetime.date.today()
        one_day = datetime.timedelta(days=1)
        for _ in range(5):
            flight_code = 0  # Conv. to string and pad with 0s later

            # IDs of the routes
            # Assumed [1, num_routes]
            route_ids = range(1, num_routes+1)
            flight_dep_time = datetime.timedelta(0)
            thirty_min = datetime.timedelta(minutes=30)

            for route_id in route_ids:
                # Make 2 flights per hour
                for half_hour in range(0, 48):
                    value_string = ""
                    flight_arrival_time = flight_dep_time + thirty_min
                    # Convert arrival_time to '24:00:00' since duration
                    # is calculated as arrival - departure.
                    # Changing to 00:00:00 will result in negative value.
                    if flight_arrival_time == datetime.timedelta(hours=24):
                        flight_arrival_time = '24:00:00'
                    flight_code_str = "MA " + str(flight_code).zfill(3)
                    flight_cost = random.randint(1000, 10_000)
                    # flight_dep_time_str = flight_dep_time.str
                    value_string = f"""
                    ('{flight_code_str}', '{flight_dep_date}', '{flight_dep_time}', '{flight_dep_date}', '{flight_arrival_time}', {flight_cost}, {route_id}),
"""
                    # Add 1 to flight code and 30 min flight_dep_time
                    flight_code += 1
                    flight_dep_time += thirty_min
                    # Reset when it reaches 1 day
                    # because i don't know how to format timedelta
                    if flight_dep_time == datetime.timedelta(hours=24):
                        flight_dep_time = datetime.timedelta(0)
                    q += value_string
            flight_dep_date = flight_dep_date + one_day
        # Remove last comma and newline
        # Add semicolon
        q = q[:-2] + ";"

        with open("flight_insert.sql", 'w') as f:
            f.write(q)


if __name__ == "__main__":
    ValueGenerator.generate_flights(12)
