from django import forms
from django.db import connection
import datetime


class FlightSearchForm(forms.Form):

    cursor = connection.cursor()
    cursor.execute("SELECT airport_city, airport_country FROM airport GROUP BY airport_city, airport_country")
    cities = cursor.fetchall()
    cities = [(c[0], f"{c[0]} ({c[1]})") for c in cities]
    cursor.close()

    from_city = forms.MultipleChoiceField(choices=cities)
    to_city = forms.MultipleChoiceField(choices=cities)
    date = forms.DateField(input_formats=['%Y-%m-%d'],
                           initial='YYYY-MM-DD')

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)

        to_city_val = cleaned_data.get('to_city')
        from_city_val = cleaned_data.get('from_city')
        date_val = cleaned_data.get('date')
        # Check if cities are the same
        if from_city_val == to_city_val:
            raise forms.ValidationError('Cities cannot be the same.')

        # Check if date is from the past
        if datetime.date.today() > date_val:
            raise forms.ValidationError('Date must not be in the past.')