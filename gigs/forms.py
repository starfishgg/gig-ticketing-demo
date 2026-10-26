
from django import forms




class TicketBookingForm(forms.Form):
    """Collect the customer's details and ticket quantity."""

    customer_name = forms.CharField(
        label="Your name",
        max_length=150,
    )
    customer_email = forms.EmailField(
        label="Email address",
    )
    quantity = forms.IntegerField(
        label="Number of tickets",
        min_value=1,
        max_value=10,
        initial=1,
    )
