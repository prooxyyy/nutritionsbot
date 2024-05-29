import random

from aiogram import Router, F, types
from sqlalchemy.ext.asyncio import AsyncSession

from common import HEALTH_TIPS
from db.models import User
from factory.client_factories import MenuCallbackFactory
from enums.enums import MenuAction, activity_level_names
from keyboards.client_keyboards import back_kb, main_menu_kb
from utils.utils import generate_food_list, calculate_daily_calories

router = Router(name="client_menu_callbacks")

@router.callback_query(MenuCallbackFactory.filter(F.action == MenuAction.OPEN))
async def open_menu(call: types.CallbackQuery):
    message = call.message

    await message.edit_text("👋 Ласкаво просимо до головного меню управління!\n\n"
                            "🥙 Тут ти можеш знайти різні корисні функції для відстеження та планування свого харчування.\n"
                            "⤵️ Обери один із пунктів меню, щоб продовжити:", reply_markup=main_menu_kb())

@router.callback_query(MenuCallbackFactory.filter(F.action == MenuAction.GEN_MENU))
async def generate_menu(call: types.CallbackQuery, session: AsyncSession):
    message = call.message

    user = await session.get(User, call.from_user.id)

    if user is None:
        return await message.reply("Помилка при обробці запросу")

    daily_calories = calculate_daily_calories(gender=user.gender, weight=user.weight, height=user.height, age=user.age,
                                              activity_level=user.activity_level)
    print(daily_calories)
    food_list = generate_food_list(calories=daily_calories)
    print(food_list)

    msg_text = "😎 Ось що мені вдалось згенерувати для тебе:\n\n"

    for idx, food in enumerate(food_list, 1):
        msg_text += f"{idx}. <b>{food['name']}</b> - <b>{food['cal']} ккал</b>\n"

    msg_text += "\n\nКалорійність продуктів вказана за 100 грамів"

    return await message.edit_text(msg_text, reply_markup=back_kb())

@router.callback_query(MenuCallbackFactory.filter(F.action == MenuAction.STATS))
async def statistics(call: types.CallbackQuery, session: AsyncSession):
    message = call.message

    user = await session.get(User, call.from_user.id)

    if user is None:
        return await message.reply("Помилка при обробці запросу")

    daily_calories = calculate_daily_calories(gender=user.gender, weight=user.weight, height=user.height, age=user.age,
                                              activity_level=user.activity_level)

    return await message.edit_text("📈 Ваша статистика:\n\n"
                                   f"Денна норма калорій: <b>{daily_calories} ккал</b>\n"
                                   f"Вага: <b>{user.weight} кг</b>\n"
                                   f"Зріст: <b>{user.height} см</b>\n"
                                   f"Рівень активності: <b>{activity_level_names[user.activity_level]}</b>", reply_markup=back_kb())

@router.callback_query(MenuCallbackFactory.filter(F.action == MenuAction.HEALTH_TIPS))
async def health_tips(call: types.CallbackQuery, session: AsyncSession):
    message = call.message

    user = await session.get(User, call.from_user.id)

    if user is None:
        return await message.reply("Помилка при обробці запросу")

    tip = random.choice(HEALTH_TIPS)

    return await message.edit_text("🤓 Порада на сьогодні:\n\n"
                                   f"{tip}", reply_markup=back_kb())