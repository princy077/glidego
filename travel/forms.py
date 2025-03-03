from django import forms
from .models import ActivityBooking, Activity, Review

class ActivityBookingForm(forms.ModelForm):
    activity = forms.ModelChoiceField(
        queryset=Activity.objects.all(),  # Ensure this fetches all activities
        empty_label="Select an activity",  # Display a placeholder
        required=True
    )

    class Meta:
        model = ActivityBooking
        fields = ['activity', 'date', 'time', 'number_of_people']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['destination', 'activity', 'rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
        }