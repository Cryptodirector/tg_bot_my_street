from datetime import datetime

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest
from app.query.users import Users

users = Users()
areas_list = []


class KeyboardsUsers:
    builder = None

    @classmethod
    async def menu_customer(
            cls,
            message: types.Message,

    ):
        builder = InlineKeyboardBuilder()
        buttons = [
            types.InlineKeyboardButton(text='📌 Создать заказ', callback_data='add_order'),
            types.InlineKeyboardButton(text='‍💻 Мои активные заказы', callback_data='my_active_orders'),
            types.InlineKeyboardButton(text='🙋‍♂️ Профиль', callback_data='profile_customer'),
            types.InlineKeyboardButton(text='⬅  Назад', callback_data='back_main_menu')

        ]
        builder.add(*buttons)
        builder.adjust(1)
        await message.edit_text(
            '<b><i>Выберите категорию!</i></b>',
            reply_markup=builder.as_markup(),
            parse_mode='HTML'
        )
        return builder

    @classmethod
    async def menu_executor(
            cls,
            message: types.Message,

    ):
        builder = InlineKeyboardBuilder()
        buttons = [
            types.InlineKeyboardButton(text='🧐 Посмотреть все заказы', callback_data='orders_menu'),
            types.InlineKeyboardButton(text='🏃 Мои активные заказы', callback_data='orders_active_executor'),
            types.InlineKeyboardButton(text='🙋‍♂️ Профиль', callback_data='profile_executor'),
            types.InlineKeyboardButton(text='⬅  Назад', callback_data='back_main_menu')

        ]
        builder.add(*buttons)
        builder.adjust(1)
        await message.edit_text(
            '<b><i>Выберите категорию!</i></b>',
            reply_markup=builder.as_markup(),
            parse_mode='HTML'
        )
        return builder

    @classmethod
    async def profile_customer(
            cls,
            message: types.Message,
            id_tg: int

    ):
        profile = await users.profile_customer(id_tg=id_tg)
        created_at = datetime.strptime(profile[0]["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
        formatted_date = created_at.strftime("%d.%m.%Y")
        formatted_time = created_at.strftime("%H:%M")
        builder = InlineKeyboardBuilder()
        buttons = [
            types.InlineKeyboardButton(text='⬅  Назад', callback_data='back_main_menu')
        ]
        builder.add(*buttons)
        builder.adjust(2, 1)
        await message.edit_text(
            f"<b><i>Ваш ID - {profile[0]['id_tg']}\n"
            f"Дата создания аккаунта - {formatted_date}, {formatted_time}\n"
            f"Активные заказы - {profile[0]['active_orders_count']}\n"
            f"Выполненные заказы - {profile[0]['completed_orders']}</i></b>",
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )
        return builder

    @classmethod
    async def profile_executor(
            cls,
            message: types.Message,
            id_tg: int

    ):
        profile = await users.profile_executor(id_tg=id_tg)
        created_at = datetime.strptime(profile[0]["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
        formatted_date = created_at.strftime("%d.%m.%Y")
        formatted_time = created_at.strftime("%H:%M")
        builder = InlineKeyboardBuilder()
        buttons = [
            types.InlineKeyboardButton(text='⬅  Назад', callback_data='back_main_menu')
        ]
        builder.add(*buttons)
        builder.adjust(2, 1)
        await message.edit_text(
            f"<b><i>Ваш ID - {profile[0]['id_tg']}\n"
            f"Дата создания аккаунта - {formatted_date}, {formatted_time}\n"
            f"Активные заказы - {profile[0]['active_orders_count']}\n"
            f"Выполненные заказы - {profile[0]['completed_orders']}</i></b>",
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )
        return builder

    @classmethod
    async def all_areas(cls, message: types.Message):
        global areas_list
        areas = await users.get_all_areas()
        builder = InlineKeyboardBuilder()

        for area in areas:
            areas_list.append(area["id"])
            buttons = [
                types.InlineKeyboardButton(
                    text=f'{area["title"]}',
                    callback_data=f'area_{area["id"]}'
                )
            ]
            builder.add(*buttons)

        builder.adjust(2)
        try:
            await message.edit_text(
                '<b><i>Выберите нужный район:</i></b>',
                reply_markup=builder.as_markup(),
                parse_mode='HTML'
            )
            return builder

        except TelegramBadRequest:
            await message.answer(
                '<b><i>Выберите нужный район:</i></b>',
                reply_markup=builder.as_markup(),
                parse_mode='HTML'
            )
            return builder

    @classmethod
    async def get_information(cls, callback: types.CallbackQuery):
        builder = InlineKeyboardBuilder()
        buttons = [
            types.InlineKeyboardButton(text='⬅  Назад', callback_data='back_main_menu')
        ]
        builder.add(*buttons)
        builder.adjust(1)

        await callback.message.edit_text(
            '<b><i>Инструкция по использованию бота:</i></b>\n\n'
            '<b><i>Выбор района:</i></b>\n'
            '   <i>После запуска бота первым шагом выберите ваш район из предложенного списка.</i>\n\n'
            '<b><i>Главное меню:</i></b>\n'
            '   <i>После выбора района откроется меню с тремя разделами:</i>\n'
            '   <i>Профиль заказчика</i>\n'
            '   <i>Профиль исполнителя</i>\n'
            '   <i>Поменять район</i>\n\n'
            '<b><i>Профиль заказчика:</i></b>\n'
            '   <b><i>Выставить заказ</i></b>: <i>Создайте новый заказ.</i>\n'
            '   <b><i>Мои активные заказы:</i></b> <i>Просмотрите список своих заказов.</i>\n'
            '   <b><i>Профиль:</i></b> <i>Узнайте статистику вашего профиля в качестве заказчика.</i>\n\n'
            '<b><i>Профиль исполнителя:</i></b>\n'
            '   <b><i>Просмотр всех заказов:</i></b> <i>Ознакомьтесь с доступными заказами в выбранном районе.</i>\n'
            '   <b><i>Взять заказ:</i></b> <i>Выберите и примите заказ для выполнения.</i>\n'
            '   <b><i>Мои активные заказы:</i></b> <i>Проверьте список заказов, которые вы выполняете.</i>\n'
            '   <b><i>Профиль:</i></b> <i>Узнайте статистику вашего профиля в качестве исполнителя.</i>\n\n'
            '<b><i>Поменять район:</i></b>\n'
            '   <i>Здесь вы можете поменять район.</i>\n\n\n'
            '<b><i>Не забывайте заканчивать заказы.</i></b>',

            reply_markup=builder.as_markup(),
            parse_mode='HTML'

        )

    @classmethod
    async def get_support(cls, callback: types.CallbackQuery):
        builder = InlineKeyboardBuilder()
        buttons = [
            types.InlineKeyboardButton(text='⬅  Назад', callback_data='back_main_menu')
        ]
        builder.add(*buttons)
        builder.adjust(1)

        await callback.message.edit_text(
            '<b><i>По всем вопросам и предложениям писать:</i></b> @sls212',

            reply_markup=builder.as_markup(),
            parse_mode='HTML'

        )

    @classmethod
    async def get_rules(
            cls,
            callback: types.CallbackQuery
    ):
        builder = InlineKeyboardBuilder()
        buttons = [
            types.InlineKeyboardButton(text='⬅  Назад', callback_data='back_main_menu')
        ]
        builder.add(*buttons)
        builder.adjust(1)

        await callback.message.edit_text(
            '<b>Бот создан для удобства участников.</b>\n'
            '<i>Администрация бота не отвечает за содержание объявлений и результаты выполнения заданий.'
            ' Вы действуете на свой страх и риск.</i>\n\n'
            '<b>ПРАВИЛА ДЛЯ ЗАКАЗЧИКОВ</b>\n'
            '<b>Обязательно укажите:</b>\n'
            '- Ограничение по возрасту (например, 18+);\n'
            '- Место выполнения задания (начальная и конечная точки);\n'
            '- Размер вознаграждения;\n'
            '- Конкретное описание задачи.\n\n'
            '<b>Запреты:</b>\n'
            '- Нельзя размещать задания, связанные с:\n'
            '  - <i>наркотиками или запрещёнными веществами;</i>\n'
            '  - <i>действиями, нарушающими законы РФ.</i>\n\n'
            '<b>Доставка алкоголя и табака:</b>\n'
            '- Разрешено только участникам старше 18 лет.\n'
            '- Исполнители должны удостовериться в совершеннолетии заказчика (рекомендуется запросить документ).\n'
            '- Участникам младше 18 лет выполнение подобных задач строго запрещено.\n'
            '- Все действия должны соответствовать законам РФ.\n'
            '<i>Администрация бота не несёт ответственности за'
            ' возможные нарушения законодательства участниками.</i>\n\n'
            '<b>ПРАВИЛА ДЛЯ ИСПОЛНИТЕЛЕЙ</b>\n'
            '- Участие несовершеннолетних возможно только с разрешения родителей.\n'
            '- Доставка алкоголя и табака строго с 18 лет.\n'
            '- Выполнение заданий, связанных с незаконной деятельностью, запрещено!',
            reply_markup=builder.as_markup(),
            parse_mode='HTML'
        )
