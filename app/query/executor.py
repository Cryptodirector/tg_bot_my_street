from aiohttp import ClientSession


class Executor:

    @classmethod
    async def take_an_order(
            cls,
            id_order: int,
            id_tg: int
    ):
        async with ClientSession() as session:

            async with session.post(
                f'https://api.my-street-tomsk.ru/v1/executor/orders/take_an_order?id_order={id_order}',
                json={'executor': id_tg},
            ) as response:
                return await response.json()

    @classmethod
    async def get_all_orders(
            cls,
            id_tg: int,
            id_area: int
    ):
        async with ClientSession() as session:
            async with session.get(
                f'https://api.my-street-tomsk.ru/v1/executor/orders/all/{id_tg}/{id_area}'
            ) as response:
                return await response.json()

    @classmethod
    async def get_active_orders(
            cls,
            id_tg: int,
            id_area: int
    ):
        async with ClientSession() as session:
            async with session.get(
                f'https://api.my-street-tomsk.ru/v1/executor/orders/active_orders/{id_tg}/{id_area}'
            ) as response:
                return await response.json()

    @classmethod
    async def get_order(
            cls,
            id_order: int,
            id_area: int
    ):
        async with ClientSession() as session:
            async with session.get(
                f'https://api.my-street-tomsk.ru/v1/executor/orders/{id_order}/{id_area}'
            ) as response:
                return await response.json()