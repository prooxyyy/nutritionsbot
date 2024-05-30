from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from enums.enums import MenuAction, AIReceptMenuAction
from factory.client_factories import MenuCallbackFactory, AIMenuCallbackFactory


def main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(
        text="😋 Згенерувати список продуктів",
        callback_data=MenuCallbackFactory(action=MenuAction.GEN_MENU).pack())
    )

    builder.add(InlineKeyboardButton(
        text="✨ AI Рецепт",
        callback_data=MenuCallbackFactory(action=MenuAction.AI_RECEPT_MENU).pack())
    )

    builder.row(InlineKeyboardButton(
        text="📈 Моя статистика",
        callback_data=MenuCallbackFactory(action=MenuAction.STATS).pack())
    )

    builder.row(InlineKeyboardButton(
        text="❤️ Корисні поради",
        callback_data=MenuCallbackFactory(action=MenuAction.HEALTH_TIPS).pack())
    )

    return builder.as_markup()

def back_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(
        text="⤴️ Назад",
        callback_data=MenuCallbackFactory(action=MenuAction.OPEN).pack())
    )

    return builder.as_markup()

def ai_recept_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(
        text="📸 По фото",
        callback_data=AIMenuCallbackFactory(action=AIReceptMenuAction.PHOTO).pack())
    )

    builder.add(InlineKeyboardButton(
        text="📝 Текстом",
        callback_data=AIMenuCallbackFactory(action=AIReceptMenuAction.TEXT).pack())
    )

    builder.row(InlineKeyboardButton(
        text="⤴️ Назад",
        callback_data=MenuCallbackFactory(action=MenuAction.OPEN).pack())
    )

    return builder.as_markup()