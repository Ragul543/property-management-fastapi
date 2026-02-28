from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "FastAPI App"
    debug: bool = True
    version: str = "0.1.0"
    database_url: str = "mysql+pymysql://fastapi_user:Solution%40456@localhost:3306/fastapi_co"

    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = "ragulleo8778074691@gmail.com"
    smtp_password: str = "yzyb bczt aiwc rdbx"
    admin_email: str = "ragulleo8778074691@gmail.com"


settings = Settings()
