from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Recipe
from django.db.models import Q

def home(request):
    recipes = Recipe.objects.order_by('-created_at')[:6]
    return render(request, 'home.html', {'recipes': recipes})

def recipe_list(request):
    q = request.GET.get('q', '')
    recipes = list(Recipe.objects.all())
    if q:
        q_lower = q.lower()
        recipes = [
            r for r in recipes
            if q_lower in r.title.lower()
            or q_lower in r.description.lower()
            or q_lower in r.ingredients.lower()
        ]
    return render(request, 'recipe_list.html', {'recipes': recipes, 'q': q})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipe_detail.html', {'recipe': recipe})

@login_required
def recipe_add(request):
    if request.method == 'POST':
        Recipe.objects.create(
            author=request.user,
            title=request.POST['title'],
            description=request.POST['description'],
            ingredients=request.POST['ingredients'],
            steps=request.POST['steps'],
        )
        return redirect('recipe_list')
    return render(request, 'recipe_form.html')

@login_required
def toggle_favorite(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user in recipe.favorites.all():
        recipe.favorites.remove(request.user)
    else:
        recipe.favorites.add(request.user)
    # вернуться туда, откуда пришёл (профиль или карточка)
    return redirect(request.META.get('HTTP_REFERER', 'recipe_detail'))

@login_required
def profile(request):
    my_recipes = Recipe.objects.filter(author=request.user)
    favorites = request.user.favorite_recipes.all()
    return render(request, 'profile.html', {'my_recipes': my_recipes, 'favorites': favorites})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})