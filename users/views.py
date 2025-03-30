from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import NewUserForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from games.models import Transaction, Game



def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect("games:index")
    else:
        form = NewUserForm()
    context = {"form": form}
    return render(request, "users/register.html", context)

class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        messages.success(self.request, "Вы успешно вошли в систему!")
        return super().form_valid(form)

class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Вы успешно вышли из системы.")
        return super().dispatch(request, *args, **kwargs)
    
@login_required
def profile(request):
    # Получаем текущего пользователя
    user = request.user
    
    # Получаем все транзакции пользователя
    transactions = Transaction.objects.filter(user=user)
    
    # Извлекаем все игры, которые пользователь приобрел
    purchased_games = [transaction.game for transaction in transactions]
    count_games = len(purchased_games)
    
    # Передаем список приобретенных игр в шаблон
    context = {
        'games': purchased_games,
        'count_games': count_games,
        'transactions': transactions,
    }
    
    return render(request, "users/profile.html",context)