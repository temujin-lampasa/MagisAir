CREATE DATABASE airline;
\c airline;

CREATE TABLE airport(
  airport_ID serial PRIMARY KEY,
  airport_name varchar(255) NOT NULL,
  airport_city varchar(255) NOT NULL,
  airport_country varchar(255) NOT NULL
);

CREATE TABLE scheduled_flight(
  flight_ID serial PRIMARY KEY,
  flight_code varchar(255) NOT NULL,
  flight_dep_date date NOT NULL,
  flight_dep_time time NOT NULL,
  flight_arrival_date date NOT NULL,
  flight_arrival_time time NOT NULL,
  flight_cost FLOAT(2) NOT NULL,
  origin_airport_ID integer NOT NULL,
  destination_airport_ID integer NOT NULL,
  CONSTRAINT fk_origin
  FOREIGN KEY (origin_airport_ID) REFERENCES airport(airport_ID),
  FOREIGN KEY (destination_airport_ID) REFERENCES airport(airport_ID),
  CONSTRAINT check_date CHECK (flight_arrival_date >= flight_dep_date)
);

CREATE TABLE crew(
  crew_ID serial PRIMARY KEY,
  crew_fname varchar(255) NOT NULL,
  crew_lname varchar(255) NOT NULL,
  crew_role varchar(255) NOT NULL
  CHECK (crew_role in ('Captain', 'First Officer', 'Second Officer',
    'Third Officer', 'Relief Crew', 'Flight Engineer', 'Purser', 'Loadmaster',
    'Airborne Sensor Operator', 'Flight Attendant', 'Flight Medic'))
);

CREATE TABLE crew_assignment(
  crew_ID integer NOT NULL,
  flight_ID INTEGER NOT NULL,
  CONSTRAINT fk_crew
  FOREIGN KEY (crew_ID) REFERENCES crew(crew_ID),
  CONSTRAINT fk_flight FOREIGN KEY (flight_ID)
  REFERENCES scheduled_flight(flight_ID)
);

CREATE TABLE passenger(
  pass_ID serial PRIMARY KEY,
  pass_fname varchar(255) NOT NULL,
  pass_lname varchar(255) NOT NULL,
  pass_mi varchar(1),
  pass_bday date NOT NULL DEFAULT '1900-01-01',
  pass_gender varchar(255)
);

CREATE TABLE booking(
  booking_ID serial PRIMARY KEY,
  booking_date date NOT NULL
  CHECK (booking_date >= current_date),
  pass_ID integer NOT NULL,
  CONSTRAINT fk_pass
  FOREIGN KEY (pass_ID) REFERENCES passenger(pass_ID)
);

CREATE TABLE addon(
  addon_ID serial PRIMARY KEY,
  addon_description varchar(255) NOT NULL,
  addon_cost FLOAT(2) NOT NULL DEFAULT 0
);

CREATE TABLE booking_addon_map(
  booking_ID integer NOT NULL,
  addon_ID integer NOT NULL,
  quantity integer NOT NULL DEFAULT 01,
  CONSTRAINT fk_booking
  FOREIGN KEY (booking_ID) REFERENCES booking(booking_ID),
  CONSTRAINT fk_addon
  FOREIGN KEY (addon_ID) REFERENCES addon(addon_ID)
);

CREATE TABLE itinerary(
  booking_ID integer NOT NULL,
  flight_ID integer NOT NULL,
  CONSTRAINT fk_booking
  FOREIGN KEY (booking_ID) REFERENCES booking(booking_ID),
  CONSTRAINT fk_flight FOREIGN KEY (flight_ID)
  REFERENCES scheduled_flight(flight_ID)
);
