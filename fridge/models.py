from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# 사용자가 등록한 식재료 (냉장고 아이템)
class IngredientItem(models.Model):
    name = models.CharField(max_length=50)  # 예: 양파
    category = models.CharField(max_length=50)  # 예: 채소, 고기 등
    exp_date = models.DateField()  # 유통기한
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User와 연결 (1:N 관계)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"
        
# DB 내 저장되어 있는 기본 식재료
class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
        
# 레시피
class Recipe(models.Model):
    title = models.CharField(max_length=50)
    instructions = models.TextField()
    ingredients = models.ManyToManyField(Ingredient)  # 어떤 재료로 만드는지

    def __str__(self):
        return self.title
