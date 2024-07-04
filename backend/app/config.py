import os

EMAIL_PATTERN = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
SESSION_EXPIRE_TIME = 3600

database_user = os.getenv("POSTGRES_USER", "kuda_user")
database_password = os.getenv("POSTGRES_PASSWORD", "123")
database_name = os.getenv("POSTGRES_DB", 'kuda')
database_host = os.getenv("POSTGRES_HOST", "localhost:5433")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("REDIRECT_URI", 'http://localhost:8000/auth/google/callback')
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY", "")

SQLALCHEMY_URL = f"postgresql+asyncpg://{database_user}:{database_password}@{database_host}/{database_name}"
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')

tags_fixture = ['smoke', 'child', 'parcels', 'with_animals', 'max_two', 'only_verified']

GOOGLE_CLIENT_ID = "941807474970-g27gmr4phcusta47dn6fvg6hvcm3btgp.apps.googleusercontent.com"
