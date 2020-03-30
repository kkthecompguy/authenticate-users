from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegisterForm
from .decorators import unauthenticated_user


@login_required
def home_view(request):
  return render(request, 'index.html', {})


@unauthenticated_user
def user_login_view(request):
  next = request.GET.get('next')
  form = UserLoginForm(request.POST or None)

  if form.is_valid():
    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password')

    user = authenticate(request, username=username, password=password)
    login(request, user)

    if next:
      return redirect('next')
    return redirect('/')

  context = {
    'form': form
  }
  return render(request, 'users/login.html', context)


@unauthenticated_user
def user_register_view(request):
  next = request.GET.get('next')
  form = UserRegisterForm(request.POST or None)
  if form.is_valid():
    password = form.cleaned_data.get('password1')
    user = form.save(commit=False)
    user.set_password(password)
    user.save()
    if next:
      return redirect(next)
    return redirect('users:login')
  
  context = {
    'form': form
  }
  return render(request, 'users/register.html', context)

def user_logout_view(request):
  logout(request)
  return redirect('users:login')