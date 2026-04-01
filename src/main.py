from typing import Annotated
from fastapi import FastAPI, Depends
from src.services.weather import WeatherService
from src.models.weather import Weather

app = FastAPI(title="Weather API Proxy")


def get_weather_service():
    return WeatherService()


@app.get("/weather/{city}", response_model=Weather)
async def get_weather(
    city: str, service: Annotated[WeatherService, Depends(get_weather_service)]
):
    return await service.get_weather(city)
