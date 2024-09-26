from uuid import uuid4, UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User, Search, Photo, PhotoLinks


async def create_search_with_photos(tg_id: int, file_ids: list[str], photo_urls: list[str], session: AsyncSession):
    # Находим пользователя или создаем нового
    user = await session.execute(select(User).where(User.tg_id == tg_id))
    user = user.scalar_one_or_none()

    if not user:
        user = User(tg_id=tg_id)
        session.add(user)
        await session.flush()  # Чтобы получить UUID пользователя

    # Создаем новый поиск
    search = Search(user_uuid=user.uuid)
    session.add(search)
    await session.flush()  # Чтобы получить search_id

    # Добавляем фотографии
    for file_id in file_ids:
        photo = Photo(file_id=file_id, search_id=search.id)
        session.add(photo)

    # Добавляем ссылки на фотографии
    photo_links = PhotoLinks(search_id=search.id, photo_urls=photo_urls)
    session.add(photo_links)

    await session.commit()
    return search.uuid


async def get_photo_urls_by_search_uuid(search_uuid: UUID, session: AsyncSession):
    search = await session.execute(select(Search).where(Search.uuid == search_uuid))
    search = search.scalar_one_or_none()

    # Получаем ссылки на фото
    photo_links = await session.execute(select(PhotoLinks).where(PhotoLinks.search_id == search.id))
    photo_links = photo_links.scalars().all()

    return [link.photo_urls for link in photo_links]
