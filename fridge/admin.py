from django.contrib import admin
from .models import IngredientItem, Recipe, Ingredient

# Register your models here.

admin.site.register(IngredientItem)
admin.site.register(Recipe)
admin.site.register(Ingredient)
