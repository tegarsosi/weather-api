# Weather API Proxy

A FastAPI proxy that fetches weather data from Visual Crossing and caches results in Redis.

A project from [roadmap.sh](https://roadmap.sh/projects/weather-api-wrapper-service)

## Prerequisites
- [uv](https://github.com/astral-sh/uv) installed
- Visual Crossing API Key
- Redis URL (Upstash or local)

## Setup
1. **Clone and install**:
   ```bash
   git clone <your-repo-url>
   cd weather-api
   uv sync
   ```
2. **Configure Environment**:
   Create a `.env` file in the root:
   ```bash
   WEATHER_API_KEY=your-api-key
   REDIS_URL=rediss://default:password@host:port
   ```

## Development
**Run the API**
```bash
uv run uvicorn src.main:app --reload
```

**Access Documentation**:
- Swagger UI:http://127.0.0.1:8000/docs

## API Endpoints
- `GET /weather/{city}`: Returns current temperature and conditions. Includes a cache_hit boolean.

### Example Response:
```json
{
    "city": "berlin",
    "temp": 11.0,
    "desc": "Clear",
    "cache_hit": true
}
```

## Project Structure
- `src/main.py`: FastAPI routes and entry point.
- `src/services/weather.py`: Logic for API fetching and Redis caching.
- `src/models/weather.py`: Pydantic models for data validation.
- `src/core/config.py`: Environment variable management.