from django import forms
from .models import Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout


class FilterForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Название'}), label='', max_length=100, required=False)
    author = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Автор'}), label='', max_length=100, required=False)
    organization = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Организация'}), label='', max_length=100, required=False)
    journal = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Журнал'}), label='', max_length=100, required=False)

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
