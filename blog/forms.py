from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout


class FilterForm(forms.Form):
    author = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Author name'}), label='', max_length=100,
                             required=False)

    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-filterForm'
        self.helper.form_class = 'form-inline'
