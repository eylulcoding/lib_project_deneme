from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('<int:pk>/', views.room_detail, name='room_detail'),
    path('<int:pk>/reserve/', views.reserve_room, name='reserve_room'),
    path('reservation/<int:pk>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    path('<int:pk>/rate/', views.rate_room, name='rate_room'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
] 