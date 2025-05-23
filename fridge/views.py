from django.shortcuts import render, redirect
from .models import Ingredient, IngredientItem, Recipe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # 로그인 성공 시 홈으로 이동
        else:
            return render(request, 'fridge/login.html', {'error': 'ID 또는 비밀번호가 틀렸습니다.'})
    return render(request, 'fridge/login.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 회원가입 후 자동 로그인
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'fridge/signup.html', {'form': form})

@login_required
def fridge_view(request):
    my_ingredients = IngredientItem.objects.filter(user=request.user)
    return render(request, 'fridge/home.html', {'my_ingredients': my_ingredients})
    
@login_required
def ingredient_search(request):
    query = request.GET.get('q', '')
    ingredients = Ingredient.objects.filter(name__icontains=query) if query else Ingredient.objects.all()

    return render(request, 'fridge/add.html', {
        'ingredients': ingredients,
        'query': query
    })
    
@login_required
def add_ingredient(request, ingredient_id):
    ingredient = Ingredient.objects.get(id=ingredient_id)

    IngredientItem.objects.create(
        name=ingredient.name,
        category=ingredient.category,
        exp_date='2025-12-31',  # 임시값
        user=request.user,
        image_url=ingredient.image_url  # ⭐ 이미지 URL 복사!
    )

    return redirect('home')


@login_required
def recommend_recipes(request):
    # 로그인한 사용자가 등록한 식재료들
    my_ingredients = IngredientItem.objects.filter(user=request.user).values_list('name', flat=True)

    # name이 하나라도 포함된 레시피 추천
    recommended = Recipe.objects.filter(ingredients__name__in=my_ingredients).distinct()

    return render(request, 'fridge/recipes.html', {
        'recommended': recommended
    })


@login_required
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'fridge/recipe_detail.html', {
        'recipe': recipe
    })

