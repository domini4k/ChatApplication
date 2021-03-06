from django.shortcuts import render, redirect, reverse
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import (
    authenticate,
    login,
    logout
)


def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/chat')

    context = {
        'form': form,
    }
    return render(request, 'users/login.html', context)


def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/chat')

    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('/login')


def start_page(request):
    return redirect('/login')