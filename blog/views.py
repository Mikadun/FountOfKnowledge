from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import FilterForm

def home(request):
	author_name = ''
	if request.method == 'POST':
		filter_form = FilterForm(request.POST)
		if filter_form.is_valid():
			author_name = filter_form.cleaned_data.get('author')
			author = User.objects.filter(username__contains=author_name).first()
			posts = Post.objects.filter(author__exact=author)
	else:
		filter_form = FilterForm()
		posts = Post.objects.all()
		author = None
	if author_name.strip() == '':
		filter_form = FilterForm()
		posts = Post.objects.all()
		author = None
	return render(request, 'blog/home.html', {'posts': posts, 'filter': {'form': filter_form, 'author': author}})

class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date']

class PostDetailView(DetailView):
	model = Post

def about(request):
	return render(request, 'blog/about.html', {'title': 'About'})

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']
	template_name = 'blog/post_update.html'

	def form_valid(self, form):
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author or not self.request.user.profile.access == 'standart':
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author or not self.request.user.profile.access == 'standart':
			return True
		return False
