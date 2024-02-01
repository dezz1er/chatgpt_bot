from aiogram import F, Router, flags, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

import kb
import text
import utils
from db.user import User
from states import Gen

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message, session: AsyncSession):
    exists_query = select(User).where(User.user_id == msg.from_user.id)
    user_exists = await session.execute(exists_query)
    user = user_exists.scalars().first()

    if not user:
        # Пользователь не найден, добавляем его в базу данных
        new_user = User(
            user_id=msg.from_user.id,
            username=msg.from_user.username,
            # Задайте другие поля, если необходимо
        )
        session.add(new_user)
        await session.commit()

        await msg.answer(
            text.greet.format(name=msg.from_user.full_name),
            reply_markup=kb.menu
        )
    else:
        # Пользователь уже существует, просто отвечаем на сообщение
        await msg.answer('Мы с тобой уже знакомы', reply_markup=kb.menu)


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)


@router.callback_query(F.data == "generate_text")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.text_prompt)
    await clbck.message.edit_text(text.gen_text)
    await clbck.message.answer(text.gen_exit, reply_markup=kb.exit_kb)


@router.message(Gen.text_prompt)
@flags.chat_action("typing")
async def generate_text(msg: Message, state: FSMContext):
    prompt = msg.text
    user_id = msg.from_user.id
    mesg = await msg.answer(text.gen_wait)
    res = await utils.generate_text(prompt, user_id)
    if not res:
        return await mesg.edit_text(text.gen_error, reply_markup=kb.iexit_kb)
    await mesg.edit_text(res + text.text_watermark,
                         disable_web_page_preview=True)


@router.callback_query(F.data == "generate_image")
async def input_image_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.img_prompt)
    await clbck.message.edit_text(text.gen_image)
    await clbck.message.answer(text.gen_exit, reply_markup=kb.exit_kb)


@router.message(Gen.img_prompt)
@flags.chat_action("upload_photo")
async def generate_image(msg: Message, state: FSMContext):
    prompt = msg.text
    mesg = await msg.answer(text.gen_wait)
    img_res = await utils.generate_image(prompt)
    if len(img_res) == 0:
        return await mesg.edit_text(text.gen_error, reply_markup=kb.iexit_kb)
    await mesg.delete()
    await mesg.answer_photo(photo=img_res[0], caption=text.img_watermark)


# @router.message(Command('clear'))
# async def process_clear_command(message: types.Message):
#     user_id = message.from_user.id
#     conversation_history[user_id] = []
#     await message.reply("История диалога очищена.")
