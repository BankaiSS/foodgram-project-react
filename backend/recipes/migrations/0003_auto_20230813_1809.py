# Generated by Django 3.2.15 on 2023-08-13 15:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredientsinrecipe',
            options={'verbose_name': 'Ингредиент в рецепте', 'verbose_name_plural': 'Ингредиенты в рецептах'},
        ),
        migrations.RemoveConstraint(
            model_name='ingredientsinrecipe',
            name='recipeingredient',
        ),
        migrations.AlterField(
            model_name='ingredientsinrecipe',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Минимальное количество 1!')], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='ingredientsinrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient', verbose_name='Ингредиент'),
        ),
        migrations.AlterField(
            model_name='ingredientsinrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_list', to='recipes.recipes', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='image',
            field=models.ImageField(upload_to='recipes/static/', verbose_name='Image'),
        ),
    ]