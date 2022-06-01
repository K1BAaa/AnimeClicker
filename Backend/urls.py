from django.urls import path
from backend import views

boosts_list = views.BoostViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

boost_details = views.BoostViewSet.as_view({
    'get': 'retrieve', # получить данные об одной заметке
    'put': 'update', # обновить все поля заметки
    'patch': 'partial_update', # обновить несколько полей заметки
    'delete': 'destroy' # ремувнуть, уничтожить, удалить, разрушить, зарезать заметку
})

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('call_click/', views.call_click, name='call_click'),
    path('boosts/', boosts_list, name='boosts'),
    path('boosts/<int:pk>/', boost_details, name='boost_details')
]
