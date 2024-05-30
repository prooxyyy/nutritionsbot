from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from cfg import cfg
from common import bot, ai_manager
from db.models import User
from enums.enums import MenuAction, AIReceptMenuAction
from factory.client_factories import MenuCallbackFactory, AIMenuCallbackFactory
from filters.ai_filters import ProccessCooldown
from fsm.ai_fsm import AIGenerateReceiptFSM
from keyboards.client_keyboards import ai_recept_menu_kb

router = Router(name="client_ai_menu")

@router.callback_query(MenuCallbackFactory.filter(F.action == MenuAction.AI_RECEPT_MENU))
async def ai_recept_menu(call: types.CallbackQuery, session: AsyncSession):
    message = call.message

    user = await session.get(User, call.from_user.id)

    if user is None:
        return await message.reply("Помилка при обробці запросу")

    await message.edit_text("✨ Будь ласка, оберіть тип генерації рецепту страви:", reply_markup=ai_recept_menu_kb())

@router.callback_query(AIMenuCallbackFactory.filter(F.action == AIReceptMenuAction.TEXT), ProccessCooldown())
async def ai_recept_text(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    message = call.message

    user = await session.get(User, call.from_user.id)

    if user is None:
        return await message.reply("Помилка при обробці запросу")

    await state.set_state(AIGenerateReceiptFSM.text)

    await message.edit_text("✨ Введіть список продуктів з яких ви хочете зробити страву:")

@router.callback_query(AIMenuCallbackFactory.filter(F.action == AIReceptMenuAction.PHOTO), ProccessCooldown())
async def ai_recept_photo(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    message = call.message

    user = await session.get(User, call.from_user.id)

    if user is None:
        return await message.reply("Помилка при обробці запросу")

    await state.set_state(AIGenerateReceiptFSM.photo)

    await message.edit_text("✨ Надішли мені фотографію з продуктами і я згенерую рецепт страви:")

@router.message(ProccessCooldown(), AIGenerateReceiptFSM.text)
async def ai_recept_text_process(message: types.Message, session: AsyncSession, state: FSMContext):
    user = await session.get(User, message.from_user.id)

    if user is None:
        return await message.reply("Помилка при обробці запросу")

    await state.clear()

    first_message = await message.reply(f"🔎 Думаю...")
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")

    response = await ai_manager.gpt(request=message.text, message=message)

    await first_message.edit_text(text=response, parse_mode=ParseMode.MARKDOWN)

@router.message(ProccessCooldown(), AIGenerateReceiptFSM.photo, F.content_type.in_({'photo'}))
async def ai_recept_photo_process(message: types.Message, session: AsyncSession, state: FSMContext):
    user = await session.get(User, message.from_user.id)

    if user is None:
        return await message.reply("Помилка при обробці запросу")

    await state.clear()

    # Получаем картинку
    photo = message.photo[-1]
    photo_as_file = await bot.get_file(file_id=photo.file_id)
    link = ""

    if photo_as_file:
        link = "https://api.telegram.org/file/bot" + cfg['token'] + "/" + photo_as_file.file_path

    print(link)

    first_message = await message.reply(f"🔎 Думаю...")
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")

    response = await ai_manager.vision(photo_link=link, message=message)

    await first_message.edit_text(text=response, parse_mode=ParseMode.MARKDOWN)