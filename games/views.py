from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from . import models
import math

def index(request):
    items_per_page = 8
    page = int(request.GET.get('page', 1))
    search = request.GET.get('search', '')
    genre_id = int(request.GET.get('genre', 0))
    publisher_id = int(request.GET.get('publisher', 0))

    publishers = models.Publiher.objects.all()
    genres = models.Genre.objects.all()

    if search:
        games = models.Game.objects.filter(name=search).all()[
            (page-1)*items_per_page:page*items_per_page]
        total_pages = math.ceil(models.Game.objects.filter(
            name=search).count()/items_per_page)
    elif genre_id > 0:
        genre = get_object_or_404(models.Genre, pk=genre_id)
        games = models.Game.objects.filter(genres=genre).all()[
            (page-1)*items_per_page:page*items_per_page]
        total_pages = math.ceil(models.Game.objects.filter(
            genres=genre).count()/items_per_page)
    elif publisher_id > 0:
        publisher = get_object_or_404(models.Publiher, pk=publisher_id)
        games = models.Game.objects.filter(publisher_id=publisher.id).all()[
            (page-1)*items_per_page:page*items_per_page]
        total_pages = math.ceil(models.Game.objects.filter(
            publisher_id=publisher.id).count()/items_per_page)
    else:
        games = models.Game.objects.all()[(
            page-1)*items_per_page:page*items_per_page]
        total_pages = math.ceil(models.Game.objects.count()/items_per_page)

    if request.user.is_authenticated:
        cart_items = models.Cart.objects.filter(user=request.user)
        cart_ids = [item.game.id for item in cart_items]
        cart_count = cart_items.count()

        transactions = models.Transaction.objects.filter(user=request.user)
        transactions_ids = [item.game.id for item in transactions]
    else:
        if 'cart' not in request.session:
            request.session['cart'] = []
        cart_ids = request.session['cart']
        cart_count = len(cart_ids)

        transactions_ids = []

    return render(request, 'games/index.html', {
        'games':games,
        'genres':genres,
        'publishers':publishers,
        'publisher_id':publisher_id,
        'genre_id':genre_id,
        'pages': range(1, total_pages+1),
        'total_pages': total_pages,
        'current_page':page,
        'next_page': page+1,
        'prev_page': page-1,
        'cart_count': cart_count,
        'cart': cart_ids,
        'transactions': transactions_ids,
    })

def game_page(request, game_id):
    game = get_object_or_404(models.Game, pk=game_id)
    images = game.images.all()
    genres = game.genres.all()
    min_req = models.MinSystemRequirements.objects.filter(game = game).first()
    rec_req = models.RecommendedSystemRequirements.objects.filter(game = game).first()

    if request.user.is_authenticated:
        cart_items = models.Cart.objects.filter(user=request.user)
        cart_ids = [item.game.id for item in cart_items]
        cart_count = cart_items.count()

        transactions = models.Transaction.objects.filter(user=request.user)
        transactions_ids = [item.game.id for item in transactions] 
    else:
        if 'cart' not in request.session:
            request.session['cart'] = []
        cart_ids = request.session['cart']
        cart_count = len(cart_ids)

        transactions_ids = []

    return render(request, 'games/game.html', {
        'game': game,
        'images': images,
        'genres': genres,
        'min_req':min_req,
        'rec_req':rec_req,
        'cart': cart_ids,
        'cart_count': cart_count,
        'transactions': transactions_ids,
    })

# добавление игры в корзину
def game_add(request, game_id):
    # получаем игру по id
    game = get_object_or_404(models.Game, pk=game_id)

    if request.user.is_authenticated:
        #если пользователь авторизован, добавляем в БД
        models.Cart.objects.get_or_create(user=request.user, game=game)
    else:
        #если пользователь не авторизован, добавляем в сессию
        if 'cart' not in request.session:
            request.session['cart'] = []
        request.session['cart'].append(game_id)
        request.session.modified = True

    #редирект на эту же страницу
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# удаление игры из корзины
def game_delete(request, game_id):

    if request.user.is_authenticated:
        # если плользователь авторизован, удаляем из БД
        try:
            cart_item = models.Cart.objects.get(user=request.user, game_id=game_id)
            cart_item.delete()
        except models.Cart.DoesNotExist:
            pass
    else:
        # если пользователь не авторизован, удаляем из сессии
        if 'cart' in request.session:
            cart = request.session['cart']
            request.session['cart'] = [game for game in cart if game != game_id]
            request.session.modified = True

    # редирект на эту же страницу
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def cart_show(request):
    cart = []
    total_amount = 0

    if request.user.is_authenticated:
        cart_items = models.Cart.objects.filter(user=request.user)
        cart_count = cart_items.count()

        for item in cart_items:
            game = get_object_or_404(models.Game, pk=item.game.pk)
            cart.append(game)
            total_amount += game.price
    else:
        for i in request.session['cart']:
            game = get_object_or_404(models.Game, pk=i)
            cart.append(game)
            total_amount += game.price
        cart_count = len(cart)

    return render(request, 'games/cart.html', {
        'cart': cart,
        'cart_count': cart_count,
        'total_amount': total_amount,
    })


@login_required
def purchase(request):
    user = request.user
    cart_items = models.Cart.objects.filter(user = user)

    if request.method == "POST":
        if cart_items.exists():
            for item in cart_items:
                models.Transaction.objects.create(
                    user = user,
                    game = item.game,
                    price = item.game.price,
                )
            
            cart_items.delete()
            messages.success(request, "Успешная покупка!")
            return redirect('games:index')

    return render(request, 'games/purchase.html')