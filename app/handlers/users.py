from aiogram import Router
from aiogram import F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.keyboards.users import KeyboardsUsers
from app.keyboards.customer import KeyboardsCustomer
from app.query.users import Users

users = Users()
router = Router()
keyboards_user = KeyboardsUsers()
keyboards_customer = KeyboardsCustomer()


class MenuHandler:

    @staticmethod
    @router.callback_query(lambda call: call.data.startswith('area_'))
    async def all_areas_call(callback: types.CallbackQuery):
        area_id = callback.data.split('_')[1]
        id_tg: int = callback.from_user.id
        try:
            await users.update_area(id_tg=id_tg, id_area=area_id)
            area = await users.get_title_area_user(id_tg=id_tg)

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
            await callback.message.edit_text(
                f"<b><i>Ваш район: {area[0]['title']}</i></b>",
                reply_markup=builder.as_markup(resize_keyboard=True),
                parse_mode='HTML'
            )
        except IndexError:
            pass

    @staticmethod
    @router.callback_query(F.data == "new_area")
    async def new_area(callback: types.CallbackQuery):
        await keyboards_user.all_areas(callback.message)

    @staticmethod
    @router.callback_query(F.data == "customer")
    async def customer_page(callback: types.CallbackQuery):
        id_tg: int = callback.from_user.id
        await users.update_activity(id_tg=id_tg)
        await keyboards_user.menu_customer(message=callback.message)

    @staticmethod
    @router.callback_query(F.data == "executor")
    async def customer_page(callback: types.CallbackQuery):
        id_tg: int = callback.from_user.id
        await users.update_activity(
            id_tg=id_tg
        )
        await keyboards_user.menu_executor(
            message=callback.message
        )

    @staticmethod
    @router.callback_query(F.data == "profile_customer")
    async def customer_profile(callback: types.CallbackQuery):
        id_tg: int = callback.from_user.id
        await users.update_activity(
            id_tg=id_tg
        )
        await keyboards_user.profile_customer(
            message=callback.message,
            id_tg=id_tg
        )

    @staticmethod
    @router.callback_query(F.data == "profile_executor")
    async def customer_profile(callback: types.CallbackQuery):
        id_tg: int = callback.from_user.id
        await users.update_activity(
            id_tg=id_tg
        )
        await keyboards_user.profile_executor(
            message=callback.message,
            id_tg=id_tg
        )

    @staticmethod
    @router.callback_query(F.data == "my_active_orders")
    async def customer_active_orders(callback: types.CallbackQuery):
        id_tg: int = callback.from_user.id
        await users.update_activity(
            id_tg=id_tg
        )
        await keyboards_customer.my_active_orders(
            message=callback.message,
            id_tg=id_tg
        )

    @staticmethod
    @router.callback_query(F.data == 'information')
    async def information(callback: types.CallbackQuery):
        id_tg: int = callback.from_user.id
        await users.update_activity(
            id_tg=id_tg
        )
        await keyboards_user.get_information(
            callback=callback
        )

    @staticmethod
    @router.callback_query(F.data == 'support')
    async def information(callback: types.CallbackQuery):
        id_tg: int = callback.from_user.id
        await users.update_activity(
            id_tg=id_tg
        )
        await keyboards_user.get_support(
            callback=callback
        )

    @staticmethod
    @router.callback_query(F.data == 'rules')
    async def rules(callback: types.CallbackQuery):
        id_tg: int = callback.from_user.id
        await users.update_activity(
            id_tg=id_tg
        )
        await keyboards_user.get_rules(
            callback=callback
        )
