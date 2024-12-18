from aiohttp import ClientSession


class Users:

    @classmethod
    async def registration(
            cls,
            id_tg: int
    ):
        async with ClientSession() as session:
            async with session.post(
                    'https://api.my-street-tomsk.ru/v1/users/add',
                    json={
                        'id_tg': id_tg
                    }
            ):
                pass

    @classmethod
    async def profile_customer(
            cls,
            id_tg: int
    ):
        async with ClientSession() as session:
            async with session.get(
                    f'https://api.my-street-tomsk.ru/v1/users/my_profile_costumer/{id_tg}'
            ) as response:
                return await response.json()

    @classmethod
    async def profile_executor(
            cls,
            id_tg: int
    ):
        async with ClientSession() as session:
            async with session.get(
                    f'https://api.my-street-tomsk.ru/v1/users/my_profile_executor/{id_tg}'
            ) as response:
                return await response.json()

    @classmethod
    async def update_activity(
            cls,
            id_tg: int
    ):
        async with ClientSession() as session:
            async with session.put(
                    f'https://api.my-street-tomsk.ru/v1/users/update/{id_tg}'
            ):
                pass

    @classmethod
    async def update_area(
            cls,
            id_tg: int,
            id_area: int
    ):
        async with ClientSession() as session:
            async with session.put(
                    f'https://api.my-street-tomsk.ru/v1/users/update/area/{id_tg}/{id_area}'
            ):
                pass

    @classmethod
    async def get_id_area_user(cls, id_tg: int):
        async with ClientSession() as session:
            async with session.get(
                    f'https://api.my-street-tomsk.ru/v1/users/area_user/{id_tg}'
            ) as response:
                return await response.json()

    @classmethod
    async def get_title_area_user(cls, id_tg: int):
        async with ClientSession() as session:
            async with session.get(
                    f'https://api.my-street-tomsk.ru/v1/users/area_user/title/{id_tg}'
            ) as response:
                return await response.json()

    @classmethod
    async def get_all_areas(cls):
        async with ClientSession() as session:
            async with session.get(
                    f'https://api.my-street-tomsk.ru/v1/users/all_areas'
            ) as response:
                return await response.json()
