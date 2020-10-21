INSERT INTO airport(airport_name, airport_city, airport_country)
VALUES
('Kennedy International Airport', 'New York', 'US'),
('Heathrow Airport', 'London', 'UK'),
('Narita Airport', 'Narita', 'JP'),
('Ninoy Aquino International Airport', 'Manila', 'PH');


-- complete graph
INSERT INTO flight_route(airport_origin, airport_destination)
VALUES
(1, 2),
(1, 3),
(1, 4),
(2, 1),
(2, 3),
(2, 4),
(3, 1),
(3, 2),
(3, 4),
(4, 1),
(4, 2),
(4, 3);


INSERT INTO flight(flight_code, flight_dep_date, flight_dep_time,
                   flight_arrival_date, flight_arrival_time, flight_cost,
                   route_ID)
VALUES
('MA 800', current_date + interval '5 days', '12:30:00', current_date + interval '5 days', '13:00:00', 2718.28, 1),
('MA 801', current_date + interval '5 days', '01:30:00', current_date + interval '5 days', '02:00:00', 2718.28, 1);


INSERT INTO crew(crew_fname, crew_lname, crew_role)
VALUES
('James', 'Dean', 'captain'),
('Claire', 'Boucher', 'first officer'),
('Debbie', 'Reynolds', 'third officer'),
('Jeremy', 'Lin', 'flight engineer'),
('Daigo', 'Umehara', 'airborne sensor operator'),
('Nana', 'Komatsu', 'flight attendant'),
('Kana', 'Hanazawa', 'flight attendant'),
('Robert', 'Lee', 'captain');


INSERT INTO crew_flight_map(crew_ID, flight_code, flight_dep_date)
VALUES
(1, 'MA 800', current_date + interval '5 days'),
(2, 'MA 800', current_date + interval '5 days'),
(3, 'MA 800', current_date + interval '5 days'),
(4, 'MA 800', current_date + interval '5 days'),
(5, 'MA 800', current_date + interval '5 days'),
(6, 'MA 800', current_date + interval '5 days'),
(7, 'MA 800', current_date + interval '5 days');


INSERT INTO passenger(pass_fname, pass_lname, pass_mi, pass_bday, pass_gender)
VALUES
('Alice', 'Glass', 'M', '1988-08-23', 'Female'),
('Stefan' , 'Burnett', 'C', '1978-05-10', 'Male'),
('Zach' , 'Hill', 'C', '1979-12-28', 'Male'),
('Andy', 'Morin', 'L', '1986-4-20', 'Male'),
('Carlito', 'Francisco', 'P', '1960-01-01', 'Male');


INSERT INTO booking(booking_date, pass_ID)
VALUES
(current_date, 1),
(current_date + interval '1 day', 2),
(current_date + interval '1 day', 3),
(current_date + interval '1 day', 4),
(current_date + interval '1 day', 5);


INSERT INTO addon(addon_description, addon_cost)
VALUES
('Additional baggage allowance (5 kg)', 237),
('Terminal Fees', 273),
('Travel Insurance', 208);


INSERT INTO booking_addon_map(booking_ID, addon_ID, quantity)
VALUES
(1, 1, 1),
(1, 2, 1),
(1, 3, 1),
(2, 1, 3),
(2, 2, 1),
(2, 3, 1),
(5, 1, 2),
(5, 2, 1),
(5, 3, 1);

INSERT INTO itinerary(booking_ID, flight_code, flight_dep_date)
VALUES
(1, 'MA 800', current_date + interval '5 days'),
(2, 'MA 800', current_date + interval '5 days'),
(3, 'MA 800', current_date + interval '5 days'),
(4, 'MA 800', current_date + interval '5 days'),
(5, 'MA 800', current_date + interval '5 days');
