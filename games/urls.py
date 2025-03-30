from django.urls import path

from .import views

app_name = 'games'

urlpatterns = [
    path('', views.index, name='index'),
    path('games/<int:game_id>/', views.game_page, name='game'),
    path('games/cart_add/<int:game_id>/', views.game_add, name='game_add'),
    path('games/cart_delete/<int:game_id>/', views.game_delete, name='game_delete'),
    path('cart/', views.cart_show, name='cart'),
    path('purchase/', views.purchase, name='purchase'),
]