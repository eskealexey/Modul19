from .forms import UserRegister
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Buyer, Game


# Create your views here.
def platform(request):
    context = {
        'title': 'Главная страница',
    }
    return render(request, 'platform.html', context)

def games_list(request):
    title = "Магазин компьютерных игр"
    games = []

    for game in Game.objects.all():
        games.append(game)
    print(games)
    context = {
        'title': title,
        'games': games,
    }
    return render(request, 'games.html', context)


class Cart(TemplateView):
    title = 'Корзина'
    text = 'Извините, Ваша корзина пуста'
    context = {
        'title': title,
        'text': text,
    }
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        return self.context

def check_value(users: list, name: str, pas1: str, pas2: str, age: int) -> bool:
    if (name not in users) and (pas1 == pas2) and age > 18:
        return True


def sign_up_by_django(request):
    title = 'Регистрация django'
    users = []
    bayers = Buyer.objects.all()
    for bayer in bayers:
        users.append(bayer.name)
    info = {'title': title, }
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            if check_value(users, username, password, repeat_password, int(age)):
                Buyer.objects.create(name=username, balance='0.5', age=age)
                info = {'res': f'Приветствуем, {username}!'}
            if username in users:
                info = {'error': 'Пользователь уже существует'}
            elif int(age) < 18:
                info = {'error': 'Вы должны быть старше 18'}
            elif password != repeat_password:
                info = {'error': 'Пароли не совпадают'}
    else:
        form = UserRegister()
        info = {
            'title': title,
            'form': form,
        }

    return render(request, 'registration_page.html', context=info)
