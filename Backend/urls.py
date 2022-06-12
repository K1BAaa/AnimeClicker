from django.urls import path
from backend import views

boosts_list = views.BoostViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

boost_details = views.BoostViewSet.as_view({
    'get': 'retrieve', # получить данные об одной
    'put': 'partial_update', # обновить все поля
    'patch': 'partial_update', # обновить несколько полей
    'delete': 'destroy' # ремувнуть, уничтожить, удалить, разрушить, зарезать
})

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('update_coins/', views.update_coins, name='update_coins'),
    path('core/', views.get_core, name='core'),
    path('boosts/', boosts_list, name='boosts'),
    path('boosts/<int:pk>/', boost_details, name='boosts'),
]
