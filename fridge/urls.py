from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.fridge_view, name='home'),  # 홈 화면에서 냉장고 식재료 보기
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('add/', views.ingredient_search, name='ingredient_search'),
    path('add/<int:ingredient_id>/', views.add_ingredient, name='add_ingredient'),
    path('recipes/', views.recommend_recipes, name='recommend_recipes'),
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
]
