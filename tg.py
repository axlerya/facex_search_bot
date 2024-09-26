import aiohttp
from PIL import Image
import io
from config import settings

class TGApi:
    def __init__(self) -> None:
        self._session = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session and not self._session.closed:
            await self._session.close()
        self._session = None

    async def generate_photo_url(self, file_id: str) -> str:
        _tg_api = f"https://api.telegram.org/bot{settings.telegram.token}/getFile?file_id={file_id}"
        async with self._session.get(_tg_api) as resp:
            data = await resp.json()
        path = data.get("result").get("file_path")
        return f"https://api.telegram.org/file/bot{settings.telegram.token}/{path}"
        
    async def get_image_from_file_id(self, file_id: str) -> Image.Image:
        photo_url = await self.generate_photo_url(file_id)
        async with self._session.get(photo_url) as resp:
            file_data = await resp.read()
        image = Image.open(io.BytesIO(file_data))
        return image
        
    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()
        self._session = None