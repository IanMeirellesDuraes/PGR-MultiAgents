import aiohttp
from src.config import AppConfig


class DynadokService:
    def __init__(self):
        self.base_url = AppConfig.get_env("DYNADOK_API_BASE_URL")
        self.auth_key = AppConfig.get_env("DYNADOK_INTERNAL_AUTH_KEY")

    async def _patch(self, path, payload):
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "x-api-key": self.auth_key,
        }

        async with aiohttp.ClientSession() as session:
            async with session.patch(
                self.base_url + path, headers=headers, json=payload
            ) as response:
                return await response.json()

    async def update_computed_fields(self, document_id, data):
        return await self._patch(
            f"/v1/internals/participant-documents/{document_id}", data
        )
