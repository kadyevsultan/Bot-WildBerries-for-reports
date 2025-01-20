from app.database.models import async_session
from app.database.models import Shop, User
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def add_shop(tg_id, api_key, shop_name):
    async with async_session() as session:
        session.add(Shop(tg_id=tg_id, api_key=api_key, shop_name=shop_name))
        await session.commit()
        
        
async def get_shops(tg_id):
    async with async_session() as session:
        result = await session.execute(select(Shop).where(Shop.tg_id == tg_id))
        return result.scalars().all()
        
        
async def del_shop(tg_id, shop_name):
    async with async_session() as session:
        await session.execute(delete(Shop).where(Shop.tg_id == tg_id).where(Shop.shop_name == shop_name))
        await session.commit()
        
async def get_api_by_shop_name(session: AsyncSession, tg_id, shop_name):
    # Используем асинхронный запрос
    async with session() as s:
        result = await s.execute(
            select(Shop).filter(Shop.tg_id == tg_id, Shop.shop_name == shop_name)
        )
        shop = result.scalars().first()  # Получаем первый результат

        if shop:
            return shop.api_key
        return None