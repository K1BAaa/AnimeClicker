from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from backend.forms import UserForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend import models


@login_required
def index(request):
    core = models.Core.objects.get(user=request.user)
    return render(request, 'backend/index.html', {'core': core})


@api_view(['GET'])
def call_click(request):
    core = models.Core.objects.get(user=request.user)
    core.click()
    return Response({'coins': core.coins})


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            core = models.Core(user=user)
            core.save()
            login(request, user)
            return redirect('index')
        return render(request, 'backend/register.html', {'user_form': user_form})

    user_form = UserForm()
    return render(request, 'backend/register.html', {'user_form': user_form})


def user_login(request):
    user_form = UserForm()
    if request.method == 'POST':
        user = authenticate(
                username=request.POST.get('username'),
                password=request.POST.get('password'),
        )
        if user:
            login(request, user)
            return redirect('index')

        return render(request, 'backend/login.html', {
            'user_form': user_form,
            'invalid': True,
            }
        )
    return render(request, 'backend/login.html', {"user_form": user_form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')
