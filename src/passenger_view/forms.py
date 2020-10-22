from django import forms
import datetime
from .queries import QueryList
import passenger_view.models as models


class FlightSearchForm(forms.Form):
    city_country = QueryList.city_country_select()
    city_choices = [(c[0], f"{c[0]} ({c[1]})") for c in city_country]

    from_city = forms.ChoiceField(choices=city_choices)
    to_city = forms.ChoiceField(choices=city_choices)
    date = forms.DateField(widget=forms.SelectDateWidget(),
                           input_formats=['%Y-%m-%d'],
                           initial=datetime.date.today())

    def clean(self):
        cleaned_data = super().clean()
        # print(cleaned_data)
        print("CLEANED: ")
        print(cleaned_data)

        to_city_val = cleaned_data.get('to_city')
        from_city_val = cleaned_data.get('from_city')
        date_val = cleaned_data.get('date')

        # Check if cities are the same
        if from_city_val == to_city_val:
            raise forms.ValidationError('Cities cannot be the same.')

        # Check if date is from the past
        if date_val is not None and datetime.date.today() > date_val:
            raise forms.ValidationError('Date must not be in the past.')


class PassengerInfoForm(forms.ModelForm):

    pass_bday = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1890, 2021)),
        input_formats=['%Y-%m-%d'],
        initial=f"{datetime.date.today().year}-01-01",
        label='Birthdate'
    )

    class Meta:
        model = models.Passenger
        fields = ['pass_fname', 'pass_lname',
                  'pass_mi', 'pass_bday', 'pass_gender']
        labels = {
            'pass_fname': 'First Name',
            'pass_lname': 'Last Name',
            'pass_mi': 'Middle Initial',
            'pass_bday': 'Birthdate',
            'pass_fname': 'First Name',
            'pass_gender': 'Gender'
        }
