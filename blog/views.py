from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import FilterForm, CommentForm
from users.models import Profile

def home(request):
	post_title = ''
	if request.method == 'POST':
		filter_form = FilterForm(request.POST)
		if filter_form.is_valid():
			post_title = filter_form.cleaned_data.get('author')
			posts = Post.objects.filter(title__contains=post_title)
	else:
		filter_form = FilterForm()
		posts = Post.objects.all()
		author = None
	if post_title.strip() == '':
		filter_form = FilterForm()
		posts = Post.objects.all()
		author = None
	return render(request, 'blog/home.html', {'posts': posts, 'filter': {'form': filter_form}})

class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date']

def view_posts(request, pk):
	author = Profile.objects.get(pk__exact=pk).user
	return render(request, 'blog/home.html', {'objects': author.post_set.all()})

def post_detail(request, pk=None):
	post = Post.objects.get(id__exact=pk)
	if request.method == 'POST':
		if not request.user.is_authenticated:
			return redirect('login')
		form = CommentForm(request.POST)
		if form.is_valid():
			form.save(request.user, post)
			return redirect('post-detail', pk)
	else:
		form = CommentForm()
	return render(request, 'blog/post_detail.html', {
		'object': post, 'form': form, 'comments': post.comment_set.all()
	})

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

