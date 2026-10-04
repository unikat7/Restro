from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('core:home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    profile_obj = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=profile_obj)
    return render(request, 'accounts/profile.html', {'form': form})
