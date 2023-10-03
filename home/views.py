from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.views import (
    LoginView, PasswordResetDoneView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib import messages
from django.views.generic.base import View
from .forms import RegisterUserForm, LoginUserForm
from django.urls import reverse_lazy
from owner import OwnwerCreateView
from django.shortcuts import render, redirect


class HomeView(View):
    template_name = 'home/main.html'

    def get(self, request):
        print(request.get_host())
        host = request.get_host()
        islocal = host.find('localhost') >= 0 or host.find('127.0.0.1') >= 0
        context = {
            'installed': settings.INSTALLED_APPS,
            'islocal': islocal,
            'settings': settings,
        }
        return render(request, self.template_name, context)


class RegisterUser(OwnwerCreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('/')

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(self.request, user, 'django.contrib.auth.backends.ModelBackend')
            messages.success(self.request, 'Регистрация Прошла успешно.')
            return redirect('words:all')
        else:
            messages.error(self.request, "Невалидная информация")
            form = RegisterUserForm()
            ctx = {'form': form}
            return render(request, self.template_name, ctx)


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'registration/login_social.html'


def logout_user(request):
    logout(request)
    return redirect('home:login')
