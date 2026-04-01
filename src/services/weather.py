import httpx
from src.models.weather import Weather
from src.core.config import settings


class WeatherService:
    def __init__(self):
        import redis.asyncio as redis

        self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.api_key = settings.WEATHER_API_KEY
        self.base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

    async def _fetch_from_api(self, city: str):
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
                raw_data = response.json()

                # Transform raw_data into clean format
                return Weather(
                    city=city,
                    temp=raw_data.get("currentConditions", {}).get("temp"),
                    desc=raw_data.get("currentConditions", {}).get("conditions"),
                )

            except httpx.HTTPStatusError as e:
                print(
                    f"Error response {e.response.status_code} while fetching weather for {city}"
                )
                raise e
            except Exception as e:
                print(f"An unexpected error occured: {e}")
                raise e

    async def get_weather(self, city: str):
        key = f"weather:{city.lower().strip()}"

        try:
            cached_data = await self.redis.get(key)
            if cached_data:
                weather = Weather.model_validate_json(cached_data)
                weather.cache_hit = True
                return weather
        except Exception as e:
            print(f"⚠️ Redis Error: {e}. Falling back to API.")

        # Fetch from API (this returns a Weather object)
        weather = await self._fetch_from_api(city)

        try:
            # Save the JSON string version to Redis
            await self.redis.set(key, weather.model_dump_json(), ex=3600)
        except Exception as e:
            print(f"⚠️ Could not save to Redis: {e}")

        return weather
