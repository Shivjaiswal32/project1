from django import forms
from .models import Attendance

from .models import Attendance, Employee
from django.contrib.auth.models import User

class AttendanceForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), required=False, label='Employee (for admin)')

    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'status']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if not (user and user.is_superuser):
            self.fields['employee'].widget = forms.HiddenInput()
