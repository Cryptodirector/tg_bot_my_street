from aiohttp import ClientSession


class Customer:

    @classmethod
    async def add_order(
            cls,
            id_tg: int,
            id_area: int,
            address: str,
            description: str
    ):
        async with ClientSession() as session:
            async with session.post(
                    'https://api.my-street-tomsk.ru/v1/costumer/orders/add',
                    json={
                        'customer': id_tg,
                        'address': address,
                        'description': description,
                        'id_area': id_area
                    }
            ):
                pass

    @classmethod
    async def get_orders_is_active(
            cls,
            id_tg: int,
            id_area: int
    ):
        async with ClientSession() as session:
            async with session.get(
                    f'https://api.my-street-tomsk.ru/v1/costumer/orders/my_active_orders/{id_tg}/{id_area}',
            ) as response:
                return await response.json()

    @classmethod
    async def order_is_completed(
            cls,
            id_order: int
    ):
        async with ClientSession() as session:
            async with session.post(
                    f'https://api.my-street-tomsk.ru/v1/costumer/orders/is_completed?id_order={id_order}',
            ):
                pass
