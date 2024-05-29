from aiogram.filters.callback_data import CallbackData

from enums.enums import Gender, ActivityLevel, MenuAction


class RegisterStepGenderCallbackFactory(CallbackData, prefix="register_gender"):
    gender: Gender


class RegisterStepActivityLevelCallbackFactory(CallbackData, prefix="reg_activity"):
    activity_level: ActivityLevel

class MenuCallbackFactory(CallbackData, prefix="menu"):
    action: MenuAction
