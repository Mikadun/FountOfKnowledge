from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.views.generic import DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Profile


def sign_up(request):
    if request.method == 'POST':
        uform = UserRegisterForm(request.POST)
        pform = ProfileUpdateForm(request.POST, request.FILES)
        if uform.is_valid() and pform.is_valid():
            uform.save()
            username = uform.cleaned_data.get('username')
            pform.save()
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        uform = UserRegisterForm()
        pform = ProfileUpdateForm()
    return render(request, 'users/signup.html', {'uform': uform, 'pform': pform})


@login_required
def profile(request):
    if request.method == 'POST':
        uform = UserUpdateForm(request.POST, instance=request.user)
        pform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, f'Account has been updated')
            return redirect('profile')
    else:
        uform = UserUpdateForm(instance=request.user)
        pform = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'uform': uform, 'pform': pform})


@login_required
def admin_panel(request):
    if request.user.profile.access == 'admin':
        return render(request, 'users/admin_panel.html',
                      {'access': request.user.profile.access, 'users': User.objects.all()})
    else:
        return HttpResponseForbidden()


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = '/'
    success_message = 'User was deleted Successfully'

    def test_func(self):
        user = self.get_object()
        if self.request.user == user or self.request.user.profile.access == 'admin':
            return True
        return False

    def get_success_message(self, cleaned_data):
        return success_message


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'users/profile_detail.html'
