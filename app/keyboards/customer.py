from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.query.customer import Customer
from app.query.users import Users

customer = Customer()
users = Users()
hand_data = []


class KeyboardsCustomer:
    @staticmethod
    async def my_active_orders(
            id_tg: int,
            message: types.Message
    ):
        global hand_data
        hand_data.clear()
        id_area = await users.get_id_area_user(
            id_tg=id_tg
        )
        orders = await Customer.get_orders_is_active(
            id_tg=id_tg,
            id_area=id_area[0]['id_area']
        )
        for order in orders:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="👌 Закончить заказ",
                            callback_data=f"order_complete_{order['id']}",
                        ),
                        InlineKeyboardButton(
                            text="❌ Закрыть запись",
                            callback_data=f"close_record",
                        )
                    ]
                ]
            )
            hand_data.append(f"order_complete_{order['id']}")
            await message.answer(
                f"<b><i>Ваш адрес: {order['address']}\n\nДетали:\n{order['description']}</i></b>",
                reply_markup=keyboard,
                parse_mode="HTML"
            )
