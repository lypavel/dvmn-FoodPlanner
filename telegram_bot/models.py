from django.db import models


class Client(models.Model):
    telegram_id = models.PositiveBigIntegerField(
        'Внешний ID пользователя',
        unique=True)
    name = models.CharField('ФИО пользователя', max_length=100)
    phonenumber = models.CharField(
        'Телефон пользователя',
        max_length=20,
        unique=True)

    def __str__(self):
        return f'{self.telegram_id} {self.name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['telegram_id']


class Ingredient(models.Model):
    title = models.CharField('Название ингредиента', max_length=200)
    image = models.ImageField('Изображение', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['title']


class Recipe(models.Model):
    dish = models.CharField('Название блюда', max_length=100)
    image = models.ImageField('Изображение', blank=True)
    description = models.TextField('Описание блюда')

    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name="recipes",
        verbose_name='Ингредиенты')

    cooking_time = models.IntegerField('Время приготовления(мин)')
    price = models.DecimalField(
        'Стоимость блюда',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    instruction = models.TextField('Инструкция приготовления')

    def __str__(self):
        return self.dish

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['dish']


class RecipeIngredient(models.Model):
    quantity = models.IntegerField('Количество ингредиента в рецепте')
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=20,
        default='грамм')

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Рецепт')
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Ингредиент рецепта')

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
