from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from enums.enums import MenuAction
from factory.client_factories import MenuCallbackFactory


def main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(
        text="😋 Згенерувати список продуктів",
        callback_data=MenuCallbackFactory(action=MenuAction.GEN_MENU).pack())
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