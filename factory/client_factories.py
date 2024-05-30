from aiogram.filters.callback_data import CallbackData

from enums.enums import Gender, ActivityLevel, MenuAction, AIReceptMenuAction


class RegisterStepGenderCallbackFactory(CallbackData, prefix="register_gender"):
    gender: Gender


class RegisterStepActivityLevelCallbackFactory(CallbackData, prefix="reg_activity"):
    activity_level: ActivityLevel

class MenuCallbackFactory(CallbackData, prefix="menu"):
    action: MenuAction

class AIMenuCallbackFactory(CallbackData, prefix="ai_menu"):
    action: AIReceptMenuAction
