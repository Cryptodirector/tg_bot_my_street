import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.query.users import Users
from app.handlers.users import router as users_router
from app.handlers.executor import router as router_executor
from app.handlers.customer import router as router_costumer
from app.keyboards.users import KeyboardsUsers

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=""
)
dp = Dispatcher()
users = Users()
keyboards_users = KeyboardsUsers()
CHANNEL_ID = ""


async def is_user_subscribed(
        message: types.Message,
        user_id: int
):

    # Проверяем состояние пользователя в канале
    chat_member = await bot.get_chat_member(
        chat_id=CHANNEL_ID,
        user_id=user_id
    )

    # Если пользователь подписан, он будет в состоянии member/administrator/creator
    if chat_member.status in ['member', 'administrator', 'creator']:
        return True

    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text="📢 Подписаться",
                    url=f"https://t.me/{CHANNEL_ID.strip('@')}"
                )],
            ]
        )
        await message.answer(
            "❌ Вы не подписаны на канал. Пожалуйста,"
            " подпишитесь, чтобы пользоваться ботом.",

            reply_markup=keyboard
        )


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    id_tg = message.from_user.id
    if await is_user_subscribed(
            user_id=id_tg,
            message=message
    ):
        await users.registration(id_tg=id_tg)
        await keyboards_users.all_areas(message)


dp.include_router(users_router)
dp.include_router(router_costumer)
dp.include_router(router_executor)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
