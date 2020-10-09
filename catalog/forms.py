from django import forms
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        #check if the date is not in the past
        if data < datetime.date.today():
            raise ValidationError(_('Invalid renewal date - It is in the past'))
        #check if the date is not far away than 4weeks in the future
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid renewal date - More than 4 weeks in the Future'))
        
        return data
