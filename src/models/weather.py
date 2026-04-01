from pydantic import BaseModel


class Weather(BaseModel):
    city: str
    temp: float
    desc: str
    cache_hit: bool = False
