from . import views
from .views import (
    HomeView, RegisterUser, LoginUser
)
from django.urls import include, path, re_path


app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view()),
    # auth
    path('register/', RegisterUser.as_view(), name='register'),
    # verify
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
]