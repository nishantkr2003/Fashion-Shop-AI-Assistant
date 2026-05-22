import ssl
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.utils.config import settings

ssl_context = ssl.create_default_context()

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=True,
    connect_args={"ssl": ssl_context}
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


async def get_db():

    async with AsyncSessionLocal() as db:
        yield db