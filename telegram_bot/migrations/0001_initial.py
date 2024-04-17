# Generated by Django 5.0.4 on 2024-04-17 14:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "telegram_id",
                    models.PositiveBigIntegerField(
                        unique=True, verbose_name="Внешний ID пользователя"
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, verbose_name="ФИО пользователя"),
                ),
                (
                    "phonenumber",
                    models.CharField(
                        max_length=20, unique=True, verbose_name="Телефон пользователя"
                    ),
                ),
            ],
            options={
                "verbose_name": "Клиент",
                "verbose_name_plural": "Клиенты",
                "ordering": ["telegram_id"],
            },
        ),
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=200, verbose_name="Название ингредиента"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True, upload_to="", verbose_name="Изображение"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "dish",
                    models.CharField(max_length=100, verbose_name="Название блюда"),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True, upload_to="", verbose_name="Изображение"
                    ),
                ),
                ("description", models.TextField(verbose_name="Описание блюда")),
                (
                    "cooking_time",
                    models.IntegerField(verbose_name="Время приготовления(мин)"),
                ),
                (
                    "price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="Стоимость блюда",
                    ),
                ),
                (
                    "instruction",
                    models.TextField(verbose_name="Инструкция приготовления"),
                ),
            ],
            options={
                "verbose_name": "Рецепт",
                "verbose_name_plural": "Рецепты",
                "ordering": ["dish"],
            },
        ),
        migrations.CreateModel(
            name="RecipeIngredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quantity",
                    models.IntegerField(
                        verbose_name="Количество ингредиента в рецепте"
                    ),
                ),
                (
                    "measurement_unit",
                    models.CharField(
                        default="грамм", max_length=20, verbose_name="Единица измерения"
                    ),
                ),
                (
                    "ingredient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="telegram_bot.ingredient",
                        verbose_name="Ингредиент рецепта",
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="telegram_bot.recipe",
                        verbose_name="Рецепт",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ингредиент рецепта",
                "verbose_name_plural": "Ингредиенты рецепта",
            },
        ),
        migrations.AddField(
            model_name="recipe",
            name="ingredients",
            field=models.ManyToManyField(
                related_name="recipes",
                through="telegram_bot.RecipeIngredient",
                to="telegram_bot.ingredient",
                verbose_name="Ингредиенты",
            ),
        ),
    ]
