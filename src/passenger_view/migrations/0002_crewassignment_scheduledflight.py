# Generated by Django 2.1.5 on 2020-10-25 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passenger_view', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrewAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'crew_assignment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ScheduledFlight',
            fields=[
                ('flight_id', models.AutoField(primary_key=True, serialize=False)),
                ('flight_code', models.CharField(max_length=255)),
                ('flight_dep_date', models.DateField()),
                ('flight_dep_time', models.TimeField()),
                ('flight_arrival_date', models.DateField()),
                ('flight_arrival_time', models.TimeField()),
                ('flight_cost', models.FloatField()),
            ],
            options={
                'db_table': 'scheduled_flight',
                'managed': False,
            },
        ),
    ]
