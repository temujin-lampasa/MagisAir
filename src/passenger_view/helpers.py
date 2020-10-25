# Helpers ---
class FlightRow:
    """A single flight row in the flight_select_view table."""

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
