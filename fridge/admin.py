from django.contrib import admin
from .models import IngredientItem, Recipe, Ingredient, RecipeStep

# Register your models here.

admin.site.register(IngredientItem)
admin.site.register(Recipe)
admin.site.register(RecipeStep)
admin.site.register(Ingredient)
