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
    rcp_seq = models.CharField(max_length=10, unique=True)  # RCP_SEQ
    title = models.CharField(max_length=100)                # RCP_NM
    method = models.CharField(max_length=30, blank=True)    # RCP_WAY2
    type = models.CharField(max_length=30, blank=True)      # RCP_PAT2
    weight = models.CharField(max_length=10, blank=True)    # INFO_WGT
    kcal = models.CharField(max_length=10, blank=True)      # INFO_ENG
    carb = models.CharField(max_length=10, blank=True)      # INFO_CAR
    protein = models.CharField(max_length=10, blank=True)   # INFO_PRO
    fat = models.CharField(max_length=10, blank=True)       # INFO_FAT
    sodium = models.CharField(max_length=10, blank=True)    # INFO_NA
    hash_tag = models.CharField(max_length=100, blank=True) # HASH_TAG
    main_image = models.URLField(blank=True)                # ATT_FILE_NO_MAIN
    detail_image = models.URLField(blank=True)              # ATT_FILE_NO_MK
    ingredients_text = models.TextField(blank=True)         # RCP_PARTS_DTLS
    tip = models.TextField(blank=True)                      # RCP_NA_TIP

    def __str__(self):
        return self.title

# 레시피 설명 및 사진
class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps')
    order = models.PositiveIntegerField()         # MANUAL01 ~ MANUAL20
    description = models.TextField(blank=True)    # MANUAL##
    image_url = models.URLField(blank=True)       # MANUAL_IMG##

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.recipe.title} - Step {self.order}"