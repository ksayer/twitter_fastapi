from src.db.session import session


async def get_session():
    async with session() as sess:
        yield sess
