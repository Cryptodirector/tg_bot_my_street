from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.query.executor import Executor
from app.query.users import Users


users = Users()
executor = Executor()
hand_id_order = []


class KeyboardsExecutor:
    @staticmethod
    async def menu_orders(callback: types.CallbackQuery):
        global hand_id_order
        hand_id_order.clear()
        id_tg = callback.from_user.id
        id_area = await users.get_id_area_user(
            id_tg=id_tg
        )
        orders = await Executor.get_all_orders(
            id_tg=id_tg,
            id_area=id_area[0]['id_area']
        )
        for order in orders:

            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="👌 Взять заказ",
                            callback_data=f"take_order_{order['id']}",
                        ),
                        InlineKeyboardButton(
                            text="❌ Закрыть запись",
                            callback_data=f"close_record",
                        )
                    ]
                ]
            )
            hand_id_order.append(
                {f"take_order_{order['id']}": order["customer"]}
            )
            await callback.message.answer(
                f"<b><i>Адрес заказчика: {order['address']}\n\nДетали:\n{order['description']}</i></b>",
                reply_markup=keyboard,
                parse_mode="HTML"
            )

    @staticmethod
    async def active_orders(callback: types.CallbackQuery):
        id_tg = callback.from_user.id
        id_area = await users.get_id_area_user(
            id_tg=id_tg
        )
        orders = await Executor.get_active_orders(
            id_tg=id_tg,
            id_area=id_area[0]['id_area']
        )

        for order in orders:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="❌ Закрыть запись",
                        callback_data="close_record",
                    )],
                ]
            )

            await callback.message.answer(
                f"<b><i>Адрес заказчика: {order['address']}\nДетали: {order['description']}</i></b>\n"
                f"<b><i>Заказчик:</i></b> tg://user?id={order['customer']}",
                reply_markup=keyboard,
                parse_mode="HTML"
            )
