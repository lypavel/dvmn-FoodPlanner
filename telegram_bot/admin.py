from django.contrib import admin

from telegram_bot.models import Ingredient, Recipe, Client, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 5


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
    inlines = (RecipeIngredientInline,)
