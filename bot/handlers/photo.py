import aiohttp
from aiogram import F, Router
from aiogram.types import Message, ContentType
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from facenet import FaceNet
from tg import TGApi
from io import BytesIO
from database.crud import create_search_with_photos
from database.engine_db import AsyncSessionLocal


router = Router(name="photo")

# URL для отправки фото на анализ
SEARCH_API_URL = "http://search_api-parser:8010/upload-photo/"

@router.message(F.content_type == ContentType.PHOTO)
async def command_start_handler(message: Message):
    """
    Основная обработка фото: отправка на анализ, запись в БД и получение ссылки на фото через UUID поиска.
    """
    await message.reply("Processing...")

    # Получаем file_id фото из сообщения
    file_id = message.photo[-1].file_id

    # Извлекаем изображение через Telegram API
    async with TGApi() as api:
        facenet = FaceNet()
        image = await api.get_image_from_file_id(file_id)
    

        items = facenet.detect_faces(image)
        
        if len(items) == 0:
            return await message.reply("нет лиц на фото")

        if len(items) > 1:
            return await message.reply("на фото более 1 лица")
        
    # Отправляем фото на search_api-parser для поиска похожих фото
    photo_list_url = await send_photo_to_search_api(image)

    if not photo_list_url:
        return await message.reply("Нет похожих фото")

    # Сохраняем поиск, фотографии и ссылки на фото в БД
    urls_to_send = [url.get('fullImageUrl') for url in photo_list_url if url.get('fullImageUrl')]

    async with AsyncSessionLocal() as session:
        search_uuid = await create_search_with_photos(message.from_user.id, [file_id], urls_to_send, session)

    # Отправляем пользователю ссылку на страницу с фотографиями, используя UUID поиска
    await message.reply(f"Here is your search result: http://localhost:8012/search/{search_uuid}")


async def send_photo_to_search_api(image):
    """
    Отправка фотографии на search_api-parser для анализа и получения похожих фото.
    """
    async with aiohttp.ClientSession() as session:
        image_bytes = BytesIO()
        image.save(image_bytes, format='JPEG')
        image_bytes.seek(0)  

        form_data = aiohttp.FormData()
        form_data.add_field('file', image_bytes, filename='image.jpg', content_type='image/jpeg')

        headers = {
            "d020f9980d9b": "931f3318123b4cba"
        }

        async with session.post(SEARCH_API_URL, headers=headers, data=form_data) as response:
            if response.status == 200:
                return await response.json()  # Возвращаем список URL-ов фото
            else:
                print(f"Error from search API: {response.status}")
                return None
