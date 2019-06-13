from django import forms
from .models import Comment

class FilterForm(forms.Form):
	author = forms.CharField(label='Author name:', max_length=100, required=False)

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
