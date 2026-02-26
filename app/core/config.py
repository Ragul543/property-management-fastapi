from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "FastAPI App"
    debug: bool = True
    version: str = "0.1.0"
    database_url: str = "postgresql+psycopg2://postgres:Solution%40456@143.1.1.107:5432/fastapi_co"


settings = Settings()
