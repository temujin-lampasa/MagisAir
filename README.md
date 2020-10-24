# MagisAir

<b>Requirements</b>
<ul>
<li> Django==3.1.2 </li>
<li> psql (PostgreSQL) 12.4 </li>
<li> Python 3.xx </li>
</ul>

<b>How to use:</b>
1. Go to src/db_files and run:

`> psql -U postgres`

`> \i setup.sql`

If that doesn't work, run:

`> psql -U postgres`

`> \i create_airline_db.sql`

`> \i insert_values.sql`

`> \i generate/flight_insert.sql`

2. Go to src/MagisAir and open `settings.py`.

  Enter your secret key:

  ```
  SECRET_KEY = '<SECRET KEY HERE>'
  ```
  
  Enter your postgres password:
  ```
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'airline',
        'USER': 'postgres',
        'PASSWORD': '<INSERT PASSWORD HERE>',
    }
  }
  ```

3. Go to src/ and run:

`> python manage.py makemigrations`

`> python manage.py migrate`

`> python manage.py runserver`

3. Open browser and go to http://localhost:8000/passenger_view/


<b> Notes: </b>

-- Flights were only generated for 1 day. (today)
 You can adjust that by going to `src/db_files/generate/generate_values.py`
 
<b> Issues: </b>

-- Missing sample data (passengers, etc)

-- Missing foreign_key constraints (ON DELETE/UPDATE stuff)

-- It doesn't know what to do when there's direct flight from A to B.
  ( it should suggest a connecting flight).
