from aiogram.exceptions import TelegramBadRequest
from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.keyboards.users import KeyboardsUsers
from app.query.users import Users

router = Router()

users = KeyboardsUsers()
users_query = Users()


class BackButtons:

    @staticmethod
    async def back_main_menu(callback: types.CallbackQuery):
        id_tg: int = callback.from_user.id
        area = await users_query.get_title_area_user(
            id_tg=id_tg
        )
        builder = InlineKeyboardBuilder()
        buttons = [
            types.InlineKeyboardButton(text='👨‍💻 Я заказчик', callback_data='customer'),
            types.InlineKeyboardButton(text='🏃 Я исполнитель', callback_data='executor'),
            types.InlineKeyboardButton(text='🏘 Поменять район', callback_data='new_area'),
            types.InlineKeyboardButton(text='🔔 Поддержка', callback_data='support'),
            types.InlineKeyboardButton(text='❗️ Инструкция', callback_data='information'),
            types.InlineKeyboardButton(text='️ 📕 Правила', callback_data='rules'),
        ]
        builder.add(*buttons)
        builder.adjust(1)

        try:
            await callback.edit_text(
                f"<b><i>Ваш район: {area[0]['title']}</i></b>",
                reply_markup=builder.as_markup(),
                parse_mode='HTML'

            )
        except TelegramBadRequest:
            await callback.answer(
                f"<b><i>Ваш район: {area[0]['title']}</i></b>",
                reply_markup=builder.as_markup(),
                parse_mode='HTML'
            )
        except AttributeError:
            await callback.message.edit_text(
                f"<b><i>Ваш район: {area[0]['title']}</i></b>",
                reply_markup=builder.as_markup(),
                parse_mode='HTML'
            )
