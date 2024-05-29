from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from enums.enums import Gender, ActivityLevel
from factory.client_factories import RegisterStepGenderCallbackFactory, RegisterStepActivityLevelCallbackFactory


def register_gender_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(
        text="🚹 Я хлопець",
        callback_data=RegisterStepGenderCallbackFactory(gender=Gender.MALE).pack())
    )

    builder.add(InlineKeyboardButton(
        text="🚺 Я дівчина",
        callback_data=RegisterStepGenderCallbackFactory(gender=Gender.FEMALE).pack())
    )

    return builder.as_markup()

def register_activity_level_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(
        text="🦦 Малорухливий",
        callback_data=RegisterStepActivityLevelCallbackFactory(activity_level=ActivityLevel.SEDENTARY).pack())
    )

    builder.row(InlineKeyboardButton(
        text="🦥 Легка активність",
        callback_data=RegisterStepActivityLevelCallbackFactory(activity_level=ActivityLevel.LIGHTLY_ACTIVE).pack())
    )

    builder.row(InlineKeyboardButton(
        text="🦍 Помірна активність",
        callback_data=RegisterStepActivityLevelCallbackFactory(activity_level=ActivityLevel.MODERATELY_ACTIVE).pack())
    )

    builder.row(InlineKeyboardButton(
        text="🐆 Висока активність",
        callback_data=RegisterStepActivityLevelCallbackFactory(activity_level=ActivityLevel.VERY_ACTIVE).pack())
    )

    return builder.as_markup()