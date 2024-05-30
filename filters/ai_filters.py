from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message

PROCESSING: list[int] = []

class ProccessCooldown(Filter):
    def __init__(self):
        pass

    async def __call__(self, call: CallbackQuery = None, message: Message = None) -> bool:
        if call is not None:
            if call.from_user.id in PROCESSING:
                await call.answer("🔄 Запит обробляється, почекайте...")
                return False
            return True

        if message is not None:
            if message.from_user.id in PROCESSING:
                await message.reply("🔄 Запит обробляється, почекайте...")
                return False
            return True

        return False