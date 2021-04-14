from django.forms import DateInput, Select


class DatePickerInput(DateInput):
    template_name = 'widgets/datepicker.html'


class SelectLiveSearchInput(Select):
    template_name = 'widgets/selectpicker.html'
