# config.py (CORRECTED VERSION)
class Config:
    SECRET_KEY = "Saltriver@123"
    
    # URL-encode the @ in password as %40
    POSTGRES_USER = "postgres"
    POSTGRES_PASSWORD = "test%40123"  # @ encoded as %40
    POSTGRES_HOST = "localhost"
    POSTGRES_PORT = "5432"
    POSTGRES_DB = "postgres"
    
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
