from django import forms

from django.db import connection


class FlightSearchForm(forms.Form):

    cursor = connection.cursor()
    cursor.execute("SELECT airport_city FROM airport GROUP BY airport_city")
    cities = cursor.fetchall()
    cities = [(c[0], c[0]) for c in cities]
    cursor.close()

    from_city = forms.MultipleChoiceField(choices=cities)
    to_city = forms.MultipleChoiceField(choices=cities)
    date = forms.DateField(input_formats=['%Y-%m-%d'],
                           initial='YYYY-MM-DD')

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        if cleaned_data.get('from_city') == cleaned_data.get('to_city'):
            raise forms.ValidationError('Cities cannot be the same.')
