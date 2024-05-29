import random

from common import FOOD_LIST
from enums.enums import Gender, ActivityLevel


def calculate_daily_calories(gender: Gender, weight: int, height: int, age: int, activity_level: ActivityLevel):
    if gender == Gender.MALE:
        # Формула Харриса-Бенедикта для мужчин
        bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
    else:
        # Формула Харриса-Бенедикта для женщин
        bmr = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)

    # Умножаем BMR на коэффициент активности
    daily_calories = bmr * activity_level.value
    return int(daily_calories)


def generate_food_list(calories):
    suitable_foods = [food for food in FOOD_LIST if food["cal"] <= calories]
    random.shuffle(suitable_foods)
    selected_foods = []
    total_calories = 0

    for food in suitable_foods:
        if total_calories + food["cal"] <= calories and len(selected_foods) < 7:
            selected_foods.append(food)
            total_calories += food["cal"]

        if len(selected_foods) >= 5:
            break

    return selected_foods
