import csv
from django.core.management.base import BaseCommand
from fridge.models import Ingredient
from django.db import transaction

class Command(BaseCommand):
    help = 'CSV에서 식재료 데이터를 읽어 DB에 저장'

    def handle(self, *args, **kwargs):
        file_path = 'ingredients_with_new_images.csv'

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            with transaction.atomic():
                for row in reader:
                    name = row['식재료명'].strip()
                    category = row['식품분류'].strip()
                    image_url = row['new_image_url'].strip() if row['new_image_url'] else None

                    # 중복 방지 - 이미 존재하면 update, 없으면 create
                    ingredient, created = Ingredient.objects.update_or_create(
                        name=name,
                        defaults={
                            'category': category,
                            'image_url': image_url
                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'추가됨: {name}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'업데이트됨: {name}'))
