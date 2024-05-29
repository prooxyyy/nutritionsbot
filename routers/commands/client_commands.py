from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from factory.client_factories import RegisterStepGenderCallbackFactory, RegisterStepActivityLevelCallbackFactory
from fsm.client_register_fsm import RegisterFSM
from keyboards.client_keyboards import main_menu_kb
from keyboards.register_keyboards import register_gender_kb, register_activity_level_kb

router = Router(name="client_commands")


@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext, session: AsyncSession):
    if await state.get_state() is not None:
        await state.clear()

    user = await session.get(User, message.from_user.id)

    if user is None:
        await state.set_state(RegisterFSM.gender)

        return await message.answer("Привіт! Цей бот допоможе тобі почати правильно харчуватися ☺️\n\n"
                                    "Перед початком, мені потрібно знати о тобі трошки більше. Ти хлопець чи дівчина?",
                                    reply_markup=register_gender_kb())
    else:
        return await message.answer("👋 Ласкаво просимо до головного меню управління!\n\n"
                                    "🥙 Тут ти можеш знайти різні корисні функції для відстеження та планування свого харчування.\n"
                                    "⤵️ Обери один із пунктів меню, щоб продовжити:", reply_markup=main_menu_kb())


@router.callback_query(RegisterStepGenderCallbackFactory.filter(), RegisterFSM.gender)
async def register_step1(call: types.CallbackQuery, state: FSMContext,
                         callback_data: RegisterStepGenderCallbackFactory):
    message = call.message

    await state.set_data({"gender": callback_data.gender})
    await state.set_state(RegisterFSM.age)

    await message.edit_text("☺️ <b>Чудово!</b> Вкажіть свій вік:")


@router.message(RegisterFSM.age)
async def register_step2(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.reply("Вкажіть ваш реальний вік!")

    age = int(message.text)

    if age < 1 or age > 100:
        return await message.reply("Вкажіть ваш реальний вік!")

    state_data = await state.get_data()
    await state.update_data(state_data, age=age)
    await state.set_state(RegisterFSM.height)

    await message.reply("Вкажіть ваш зріст (у сантиметрах):")


@router.message(RegisterFSM.height)
async def register_step3(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.reply("Вкажіть ваш реальний зріст!")

    height = int(message.text)

    if height < 120 or height > 300:
        return await message.reply("Вкажіть ваш реальний зріст!")

    state_data = await state.get_data()
    await state.update_data(state_data, height=height)
    await state.set_state(RegisterFSM.weight)

    await message.reply("Вкажіть вашу вагу (у кілограмах):")


@router.message(RegisterFSM.weight)
async def register_step4(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.reply("Вкажіть вашу реальну вагу!")

    weight = int(message.text)

    if weight < 25 or weight > 250:
        return await message.reply("Вкажіть вашу реальну вагу!")

    state_data = await state.get_data()
    await state.update_data(state_data, weight=weight)
    await state.set_state(RegisterFSM.activity_level)

    await message.reply("💪 Оберіть вашу фізичну активність:", reply_markup=register_activity_level_kb())


@router.callback_query(RegisterStepActivityLevelCallbackFactory.filter())
async def register_step5(call: types.CallbackQuery, state: FSMContext,
                         callback_data: RegisterStepActivityLevelCallbackFactory, session: AsyncSession):
    message = call.message

    user = await session.get(User, call.from_user.id)

    state_data = await state.get_data()

    print(state_data)

    if user is None:
        try:
            user = User(user_id=call.from_user.id)

            user.gender = state_data['gender']
            user.age = state_data['age']
            user.height = state_data['height']
            user.weight = state_data['weight']
            user.activity_level = callback_data.activity_level

            await session.merge(user)

            await session.commit()

            await state.clear()

            await message.edit_text("👋 Ласкаво просимо до головного меню управління!\n\n"
                                    "🥙 Тут ти можеш знайти різні корисні функції для відстеження та планування свого харчування.\n"
                                    "⤵️ Обери один із пунктів меню, щоб продовжити:", reply_markup=main_menu_kb())
        except Exception as e:
            print(e)
    else:
        await message.edit_text("Не вдалось виконати операцію.")
