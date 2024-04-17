from django.contrib import admin

from telegram_bot.models import Ingredient, Recipe, Client, RecipeIngredient


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = ('telegram_id', 'phonenumber',)
    list_display = ('telegram_id', 'name', 'phonenumber',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    search_fields = ('dish',)
    list_display = ('dish', 'cooking_time', 'price',)
    raw_id_fields = ('ingredients',)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient', 'recipe', 'quantity', 'measurement_unit',)
    raw_id_fields = ('recipe', 'ingredient',)
