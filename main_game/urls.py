from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterPageView.as_view(), name="register"),
    path('login/', views.LoginPageView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),

    path('', views.GameView.as_view(), name="game"),
]