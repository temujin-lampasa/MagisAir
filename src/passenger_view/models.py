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

    def __str__(self):
        return self.airport_city

    def same_city(self, other_airport):
        return self.airport_city == other_airport.airport_city


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


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


class CrewFlightMap(models.Model):
    crew = models.ForeignKey(Crew, models.DO_NOTHING)
    flight_code = models.ForeignKey('Flight', models.DO_NOTHING, db_column='flight_code')
    flight_dep_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'crew_flight_map'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Flight(models.Model):
    flight_code = models.CharField(primary_key=True, max_length=255)
    flight_dep_date = models.DateField()
    flight_dep_time = models.TimeField()
    flight_arrival_date = models.DateField()
    flight_arrival_time = models.TimeField()
    flight_cost = models.FloatField()
    route = models.ForeignKey('FlightRoute', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'flight'
        unique_together = (('flight_code', 'flight_dep_date'),)


class FlightRoute(models.Model):
    route_id = models.AutoField(primary_key=True)
    airport_origin = models.ForeignKey(
        Airport, models.DO_NOTHING,
        related_name='airport_origin',
        db_column='airport_origin'
        )
    airport_destination = models.ForeignKey(
        Airport, models.DO_NOTHING,
        related_name='airport_destination',
        db_column='airport_destination')

    class Meta:
        managed = False
        db_table = 'flight_route'


class Itinerary(models.Model):
    booking = models.ForeignKey(Booking, models.DO_NOTHING)
    flight_code = models.ForeignKey(Flight, models.DO_NOTHING, db_column='flight_code')
    flight_dep_date = models.DateField()

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
