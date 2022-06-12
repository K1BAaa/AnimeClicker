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
def get_core(request):
    core = Core.objects.get(user=request.user)
    return Response({
        'core': CoreSerializer(core).data,
    })


@api_view(['POST'])
def update_coins(request):
    coins = request.data['current_coins']
    core = Core.objects.get(user=request.user)
    is_levelup, boost_type = core.update_coins(coins)

    if is_levelup:
        Boost.objects.create(
                core=core, price=core.coins, power=core.level*5, type=boost_type,
        )
    core.save()
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

    def partial_update(self, request, pk):
        coins = request.data['coins']
        boost = self.queryset.get(pk=pk)
        is_levelup = boost.levelup(coins)
        if not is_levelup:
            return Response({'error': 'Not enough money'})
        old_boost_values, new_boost_values = is_levelup
        return Response({
            'old_boost_values': self.serializer_class(old_boost_values).data,
            'new_boost_values': self.serializer_class(new_boost_values).data,
        })


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
