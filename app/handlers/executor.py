import asyncio

from aiogram import Router, Bot
from aiogram import F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.keyboards.executor import KeyboardsExecutor
from app.query.executor import Executor
from app.query.users import Users

users = Users()
keyboards_executor = KeyboardsExecutor()
executor = Executor()
router = Router()
bot = Bot(token="7656161088:AAGHJoxI4ZHu64eZY0slSwO0r7r_h9ThmnQ")


@router.callback_query(F.data == "orders_menu")
async def show_orders(callback: types.CallbackQuery):
    id_tg: int = callback.from_user.id
    await users.update_activity(id_tg=id_tg)
    await keyboards_executor.menu_orders(callback)


@router.callback_query(F.data.startswith("take_order_"))
async def take_order(callback: types.CallbackQuery):
    id_tg: int = callback.from_user.id

    area = await users.get_title_area_user(id_tg=id_tg)
    await users.update_activity(id_tg=id_tg)
    await callback.message.delete()
    id_order = int(callback.data.split("_")[-1])
    result = await executor.take_an_order(
        id_order=id_order,
        id_tg=callback.from_user.id
    )
    id_area = await users.get_id_area_user(id_tg=id_tg)
    order = await executor.get_order(
        id_order=id_order,
        id_area=id_area[0]['id_area']
    )
    if result == {'detail': 'Заказ недоступен'}:
        builder = InlineKeyboardBuilder()
        buttons = [
            types.InlineKeyboardButton(text='‍💻 Я заказчик', callback_data='customer'),
            types.InlineKeyboardButton(text='🏃 Я исполнитель', callback_data='executor'),
            types.InlineKeyboardButton(text='🏘 Поменять район', callback_data='new_area'),
            types.InlineKeyboardButton(text='🔔 Поддержка', callback_data='support'),
            types.InlineKeyboardButton(text='❗️ Инструкция', callback_data='information'),
            types.InlineKeyboardButton(text='️ 📕 Правила', callback_data='rules'),
        ]
        builder.add(*buttons)
        builder.adjust(1)

        dlt = await bot.send_message(
            text='😥 Упс, заказ уже взяли',
            chat_id=callback.from_user.id
        )
        await asyncio.sleep(3)
        await bot.delete_message(
            chat_id=callback.from_user.id,
            message_id=dlt.message_id
        )
        await callback.message.answer(
            f"<b><i>Ваш район: {area[0]['title']}</i></b>",
            reply_markup=builder.as_markup(),
            parse_mode='HTML'
        )

    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text="➡ Перейти к клиенту",
                    url=f"tg://user?id={order[0]['customer']}",
                )],
                [InlineKeyboardButton(
                    text="❌ Закрыть запись",
                    callback_data="close_record",
                )],
            ]
        )

        await callback.message.answer(
            "👌 Заказ принят!",
            reply_markup=keyboard
        )


@router.callback_query(F.data == "orders_active_executor")
async def get_my_active_orders(callback: types.CallbackQuery):
    id_tg: int = callback.from_user.id
    await users.update_activity(id_tg=id_tg)
    await keyboards_executor.active_orders(callback)
