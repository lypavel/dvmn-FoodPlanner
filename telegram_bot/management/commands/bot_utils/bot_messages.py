from telegram_bot.models import Recipe, RecipeIngredient


WELCOME = (
    'Добро пожаловать в наш бот по подбору рецептов.\n\n'
    'С помощью него вы всегда сможете подобрать подходящий для вас рецепт '
    'на каждый день.'
    )

PD_AGREEMENT = (
    'Для продолжения работы с ботом необходимо ваше согласие '
    'на обработку персональных данных.'
)

PD_RESTRICT = (
    'К сожалению, без согласия на обработку персональных данных '
    'вы не сможете воспользоваться нашим сервисом.'
)

FOR_REGULAR_CUSTOMERS = (
    'Давайте посмотрим, какие блюда вы можете приготовить сегодня.'
)

AUTH_SUCCESSFUL = (
    'Вы успешно зарегистрированы.'
)

NO_RECIPES = 'Не найдено ни одного рецепта. Попробуйте зайти позднее.'

GET_CLIENT_NAME = 'Отлично. Скажите, как мы можем к Вам обращаться?'
GET_CLIENT_PHONE = 'Теперь введите ваш номер телефона.'
GET_CLIENT_VALID_PHONE = (
    'Вероятно в номере телефона допущена ошибка. Попробуйте снова.'
)
GET_EXISTING_PHONE = (
    'Этот номер телефона уже используется. Попробуйте ввести другой номер.'
)


def generate_user_greeting(name: str) -> str:
    return f'Приятно познакомиться, {name}.'


def generate_recipe_main_info(recipe: Recipe) -> str:
    return (
        f'**{recipe.dish}**\n\n{recipe.description}\n\n'
        f'Время приготовления: {recipe.cooking_time} минут\n\n'
        f'Стоимость блюда: {recipe.price} у.е.'
    )


def generate_recipe_instructions(recipe: Recipe) -> str:
    ingredients = ''

    recipe_ingredients = RecipeIngredient.objects\
        .filter(recipe=recipe)\
        .select_related('ingredient')
    for ingredient in recipe_ingredients:
        ingredients = (f'{ingredients}\n'
                       f'{ingredient.ingredient.title} - '
                       f'{ingredient.quantity} '
                       f'{ingredient.measurement_unit}')

    return (f'**Продукты**:\n{ingredients}\n\n'
            f'**Способ приготовления:**\n\n{recipe.instruction}')
