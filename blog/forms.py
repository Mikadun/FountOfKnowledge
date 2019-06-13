from django import forms
from .models import Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout


class FilterForm(forms.Form):
    author = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите текст'}), label='', max_length=100,
                             required=False)

    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-filterForm'
        self.helper.form_class = 'form-inline'

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['content']

	def form_valid(self, form, post):
		form.instance.author = self.request.user
		form.instance.post = post
		return super().form_valid(form)

	def save(self, author, post):
		comment = super(CommentForm, self).save(commit=False)
		comment.author = author
		comment.post = post
		comment.save()
		return comment