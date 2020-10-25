# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Addon(models.Model):
    addon_id = models.AutoField(primary_key=True)
    addon_description = models.CharField(max_length=255)
    addon_cost = models.FloatField()

    class Meta:
        managed = False
        db_table = 'addon'


class Airport(models.Model):
    airport_id = models.AutoField(primary_key=True)
    airport_name = models.CharField(max_length=255)
    airport_city = models.CharField(max_length=255)
    airport_country = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'airport'


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    booking_date = models.DateField()
    pass_field = models.ForeignKey('Passenger', models.DO_NOTHING, db_column='pass_id')  # Field renamed because it was a Python reserved word.

    class Meta:
        managed = False
        db_table = 'booking'


class BookingAddonMap(models.Model):
    booking = models.ForeignKey(Booking, models.DO_NOTHING)
    addon = models.ForeignKey(Addon, models.DO_NOTHING)
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'booking_addon_map'


class Crew(models.Model):
    crew_id = models.AutoField(primary_key=True)
    crew_fname = models.CharField(max_length=255)
    crew_lname = models.CharField(max_length=255)
    crew_role = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'crew'


class CrewAssignment(models.Model):
    crew = models.ForeignKey(Crew, models.DO_NOTHING)
    flight = models.ForeignKey('ScheduledFlight', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'crew_assignment'


class Itinerary(models.Model):
    booking = models.ForeignKey(Booking, models.DO_NOTHING)
    flight = models.ForeignKey('ScheduledFlight', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'itinerary'


class Passenger(models.Model):
    pass_id = models.AutoField(primary_key=True)
    pass_fname = models.CharField(max_length=255)
    pass_lname = models.CharField(max_length=255)
    pass_mi = models.CharField(max_length=1, blank=True, null=True)
    pass_bday = models.DateField()
    pass_gender = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'passenger'


class ScheduledFlight(models.Model):
    flight_id = models.AutoField(primary_key=True)
    flight_code = models.CharField(max_length=255)
    flight_dep_date = models.DateField()
    flight_dep_time = models.TimeField()
    flight_arrival_date = models.DateField()
    flight_arrival_time = models.TimeField()
    flight_cost = models.FloatField()
    origin_airport = models.ForeignKey(Airport, models.DO_NOTHING,
                                       related_name='origin_airport')
    destination_airport = models.ForeignKey(Airport, models.DO_NOTHING,
                                            related_name='dest_airport')

    class Meta:
        managed = False
        db_table = 'scheduled_flight'
