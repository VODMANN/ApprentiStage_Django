from django.forms.widgets import TextInput

class DatePickerInput(TextInput):
    template_name = 'widgets/datepicker.html'

class TimePickerInput(TextInput):
    template_name = 'widgets/timepicker.html'
