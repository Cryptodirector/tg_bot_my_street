import asyncio

from aiogram import Router

from aiogram import Bot, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.keyboards.customer import KeyboardsCustomer
from app.query.customer import Customer
from app.keyboards.back_buttons import BackButtons
from app.keyboards.users import KeyboardsUsers
from app.query.users import Users

users = Users()
customer = Customer()
keyboards_costumer = KeyboardsCustomer()
keyboards_users = KeyboardsUsers()


router = Router()
bot = Bot(token="7656161088:AAGHJoxI4ZHu64eZY0slSwO0r7r_h9ThmnQ")


class UserMSG(StatesGroup):
    address = State()
    description = State()


@router.callback_query(F.data == "add_order")
async def checkout(callback: types.CallbackQuery, state: FSMContext):
    id_tg: int = callback.from_user.id
    await users.update_activity(id_tg=id_tg)
    await callback.message.delete()
    await state.set_state(UserMSG.address)

    # Отправляем сообщение и сохраняем его ID в состояние
    delete_msg = await callback.message.answer(
        "🏠 <b><i>Введите ваш адрес:\n Пример: Трудовая 18</i></b>",
        parse_mode='HTML'
    )
    await state.update_data(
        delete_msg_id=delete_msg.message_id
    )


@router.message(UserMSG.address)
async def set_address(message: types.Message, state: FSMContext):
    # Получаем ID сообщения, которое нужно удалить
    user_data = await state.get_data()
    delete_msg_id = user_data.get("delete_msg_id")

    # Обновляем состояние
    await state.update_data(
        address=message.text
    )
    await message.delete()

    # Удаляем предыдущее сообщение
    if delete_msg_id:
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=delete_msg_id
        )

    # Отправляем следующее сообщение
    dlt = await message.answer(
        f"<b><i>Ваш адрес: {message.text}\n"
        "👌 Принято! Укажите детали заказа:\n\n"
        "Пример:\n"
        "Откуда: Магазин Ярче\n"
        "Купить: молоко, хлеб\n"
        "Стоимость заказа: 100р</i></b>",
        parse_mode="HTML"
    )
    await state.set_state(UserMSG.description)

    # Сохраняем ID нового сообщения для удаления на следующем этапе
    await state.update_data(
        delete_msg_id=dlt.message_id
    )


@router.message(UserMSG.description)
async def set_description(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❌ Закрыть запись",
                    callback_data=f"close_record",
                )
            ]
        ]
    )

    user_data = await state.get_data()
    id_area = await users.get_id_area_user(
        id_tg=message.from_user.id
    )

    await customer.add_order(
        id_tg=message.from_user.id,
        id_area=id_area[0]['id_area'],
        address=user_data["address"],
        description=message.text
    )
    await message.delete()

    delete_msg_id = user_data.get("delete_msg_id")
    if delete_msg_id:
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=delete_msg_id
        )

    await bot.send_message(
        text=(
            "<b><i>👌 Заказ принят! Скоро с вами свяжется исполнитель.\n\n"
            f"Детали:\n{user_data.get('address')}\n{message.text}\n\n"
            "Посмотреть ваш заказ можно во вкладке\n"
            '"Мои активные заказы"</i></b>'
        ),
        chat_id=message.chat.id,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await state.clear()
    await asyncio.sleep(5)
    await BackButtons.back_main_menu(
        message
    )


@router.callback_query(F.data.startswith("order_complete_"))
async def order_completed(callback: types.CallbackQuery):
    id_tg: int = callback.from_user.id
    id_order = int(callback.data.split("_")[-1])
    await users.update_activity(
        id_tg=id_tg
    )
    await customer.order_is_completed(
        id_order=id_order
    )
    await callback.message.delete()
    await callback.answer("👌 Заказ завершён!")


@router.callback_query(F.data == 'back_main_menu')
async def back_main_menu(callback: types.CallbackQuery):
    id_tg: int = callback.from_user.id
    await users.update_activity(
        id_tg=id_tg
    )
    return await BackButtons.back_main_menu(
        callback)


@router.callback_query(F.data == 'close_record')
async def back_main_menu(callback: types.CallbackQuery):
    id_tg: int = callback.from_user.id
    await users.update_activity(
        id_tg=id_tg
    )
    await callback.message.delete()
