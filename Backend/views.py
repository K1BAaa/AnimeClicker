from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Core, Boost
from .serializers import CoreSerializer, BoostSerializer


@login_required
def index(request):
    core = Core.objects.get(user=request.user)
    boosts = Boost.objects.filter(core=core)
    return render(request, 'backend/index.html', {'core': core, 'boosts': boosts})


@api_view(['GET'])
def call_click(request):
    core = Core.objects.get(user=request.user)
    is_levelup = core.click()
    if is_levelup:
        Boost.objects.create(core=core, price=core.coins, power=core.level*20)
    return Response({
            'core': CoreSerializer(core).data,
            'is_levelup': is_levelup,
    })


class BoostViewSet(viewsets.ModelViewSet):
    queryset = Boost.objects.all()
    serializer_class = BoostSerializer

    def get_queryset(self):
        core = Core.objects.get(user=self.request.user)
        boosts = self.queryset.filter(core=core)
        return boosts


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            core = Core(user=user)
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
