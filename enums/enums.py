from enum import Enum

class ActivityLevel(float, Enum):
    SEDENTARY = 1.2
    LIGHTLY_ACTIVE = 1.375
    MODERATELY_ACTIVE = 1.55
    VERY_ACTIVE = 1.725

activity_level_names = {
    ActivityLevel.SEDENTARY: "Малорухливий",
    ActivityLevel.LIGHTLY_ACTIVE: "Слабо активний",
    ActivityLevel.MODERATELY_ACTIVE: "Помірно активний",
    ActivityLevel.VERY_ACTIVE: "Дуже активний"
}

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class MenuAction(str, Enum):
    GEN_MENU = "gen_menu"
    STATS = "my_stats"
    OPEN = "open"
    HEALTH_TIPS = "health_tips"
    AI_RECEPT_MENU = "ai_recept"

class AIReceptMenuAction(str, Enum):
    PHOTO = "photo"
    TEXT = "text"