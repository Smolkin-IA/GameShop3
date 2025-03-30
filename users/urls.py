from django.urls import path
from .views import UserLoginView, UserLogoutView

from .import views

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),
]