from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Ingredient, IngredientItem, Recipe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime, date, timedelta
from django.views.decorators.csrf import csrf_exempt

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
    today = date.today()
    items = IngredientItem.objects.filter(user=request.user)

    imminent_items = []
    expired_items = []

    for item in items:
        if item.exp_date < today:
            expired_items.append(item)
        elif today <= item.exp_date <= today + timedelta(days=3):
            imminent_items.append(item)

    return render(request, 'fridge/home.html', {
        'my_ingredients': items,
        'expired_items': expired_items,
        'imminent_items': imminent_items
    })

    
@login_required
def ingredient_search(request):
    query = request.GET.get('q', '')
    ingredients = Ingredient.objects.filter(name__icontains=query) if query else Ingredient.objects.all()

    return render(request, 'fridge/add.html', {
        'ingredients': ingredients,
        'query': query
    })
    
@csrf_exempt
@login_required
def add_ingredient(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)

    if request.method == "POST":
        exp_date_str = request.POST.get('exp_date')
        try:
            exp_date = datetime.strptime(exp_date_str, '%Y-%m-%d').date()
        except:
            exp_date = date.today()  # 파싱 실패 시 오늘 날짜

        print("exp_date_str:", exp_date_str)
        print("parsed exp_date:", exp_date)

        
        IngredientItem.objects.create(
            name=ingredient.name,
            category=ingredient.category,
            exp_date=exp_date,
            user=request.user,
            image_url=ingredient.image_url
        )
        return redirect('home')
    
    return redirect('ingredient_search')


@login_required
def recipe_select(request):
    selected_ingredients = []
    selected_type = request.GET.get("type")

    if request.method == "POST":
        # 사용자가 식재료 선택 후 '레시피 추천' 버튼을 눌렀을 때
        selected_ingredients = request.POST.getlist("ingredients")

        # 선택한 재료와 관련된 레시피 찾기
        q = Q()
        for ing in selected_ingredients:
            q |= Q(ingredients_text__icontains=ing)

        # 추천된 레시피를 QuerySet으로 저장
        recipes = Recipe.objects.filter(q).distinct()

        # 세션에 저장 (GET 요청에서도 사용 가능하도록)
        request.session['recommended_ids'] = [r.id for r in recipes]
        request.session['selected_ingredients'] = selected_ingredients

    else:
        # GET 요청 (예: type 버튼 클릭 시)
        recommended_ids = request.session.get('recommended_ids', [])
        selected_ingredients = request.session.get('selected_ingredients', [])
        recipes = Recipe.objects.filter(id__in=recommended_ids)

    # type 필터가 선택되었으면 적용
    if selected_type:
        recipes = recipes.filter(type=selected_type)
        
     # 추천된 레시피가 있을 때만 type 필터 제공
    if recipes.exists():
        recipe_types = recipes.values_list("type", flat=True).distinct()
    else:
        recipe_types = []

    items = IngredientItem.objects.filter(user=request.user)
    ingredients = [item for item in items]
    recipe_types = Recipe.objects.values_list("type", flat=True).distinct()

    return render(request, "fridge/recipes.html", {
        "ingredients": ingredients,
        "selected_ingredients": selected_ingredients,
        "recommended": recipes,
        "recipe_types": recipe_types,
        "selected_type": selected_type,
    })


@login_required
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'fridge/recipe_detail.html', {
        'recipe': recipe
    })

@login_required
def alerts_view(request):
    today = date.today()
    items = IngredientItem.objects.filter(user=request.user)

    imminent_items = []
    expired_items = []

    for item in items:
        if item.exp_date < today:
            expired_items.append(item)
        elif today <= item.exp_date <= today + timedelta(days=3):
            imminent_items.append(item)

    return render(request, 'fridge/alerts.html', {
        'expired_items': expired_items,
        'imminent_items': imminent_items
    })

@login_required
@csrf_exempt
def delete_ingredient(request, item_id):
    item = get_object_or_404(IngredientItem, id=item_id, user=request.user)
    
    if request.method == "POST":
        item.delete()
        return redirect('home')
    
    return redirect('home')
