import httpx
from src.core.config import settings

class WeatherService:
    def __init__(self):
        import redis.asyncio as redis

        self.redis = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True
        )
        self.api_key = settings.WEATHER_API_KEY
        self.base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
    
    async def fetch_from_api(self, city: str):
        params = {
            "key": self.api_key,
            "unitGroup": "metric",
            "contentType": "json",
        }
        url = f"{self.base_url}/{city}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()

            except httpx.HTTPStatusError as e:
                print(f"Error response {e.response.status_code} while fetching weather for {city}")
                raise e
            except Exception as e:
                print(f"An unexpected error occured: {e}")
                raise e