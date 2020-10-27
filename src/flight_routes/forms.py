from django import forms
from string import digits
from passenger_view.models import ScheduledFlight, Airport


class AirportForm(forms.ModelForm):
    """Form for creating new airports"""
    class Meta:
        model = Airport
        fields = [
            'airport_name',
            'airport_city',
            'airport_country'
        ]

    def clean_airport_country(self, *args, **kwargs):
        airport_country = self.cleaned_data.get('airport_country')
        if len(airport_country) == 2 and airport_country.isupper():
            return airport_country
        else:
            raise forms.ValidationError("Country code is invalid")


class ScheduledFlightForm(forms.ModelForm):
    class Meta:
        model = ScheduledFlight
        fields = [
            'flight_code',
            'flight_dep_date',
            'flight_dep_time',
            'flight_arrival_date',
            'flight_arrival_time',
            'flight_cost',
            'origin_airport',
            'destination_airport'
        ]

    def clean_flight_code(self, *args, **kwargs):
        flight_code = self.cleaned_data.get('flight_code')
        starts_with_MA_space = flight_code.startswith('MA ')
        ends_with_three_digits = False not in [character in digits for character in flight_code][-3:]
        is_six_characters = len(flight_code) == 6
        if starts_with_MA_space and ends_with_three_digits and is_six_characters:
            return flight_code
        else:
            raise forms.ValidationError("Flight code must start with 'MA ' and end with three digits")

    def clean_flight_cost(self, *args, **kwargs):
        flight_cost = self.cleaned_data.get('flight_cost')
        if flight_cost >= 0:
            return flight_cost
        else:
            raise forms.ValidationError("Flight cost must be at least 0.00")

    def clean_origin_airport(self, *args, **kwargs):
        origin_airport = self.cleaned_data.get('origin_airport')
        destination_airport = self.cleaned_data.get('destination_airport')
        if origin_airport != destination_airport:
            return origin_airport
        else:
            raise forms.ValidationError("Origin and destination airports must be different")

    def clean_destination_airport(self, *args, **kwargs):
        destination_airport = self.cleaned_data.get('destination_airport')
        origin_airport = self.cleaned_data.get('origin_airport')
        if destination_airport != origin_airport:
            return destination_airport
        else:
            raise forms.ValidationError("Origin and destination airports must be different")
