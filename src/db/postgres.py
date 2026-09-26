from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.config import get_config

Base = declarative_base()


class Database:
    def __init__(self):
        self.engine = None
        self.session_maker = None

    def init(self):
        config = get_config()
        db_config = config.database.postgres

        # Construct async database URL
        # Assumes asyncpg driver
        user, password = <YOUR_PASSWORD>"user"], db_config["password"]
        host, port, database = (
            db_config["host"],
            db_config["port"],
            db_config["database"],
        )
        url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"

        self.engine = create_async_engine(
            url, echo=False, pool_size=20, max_overflow=10
        )

        self.session_maker = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def get_session(self) -> AsyncSession:
        if self.session_maker is None:
            self.init()
        async with self.session_maker() as session:
            yield session

    async def close(self):
        if self.engine:
            await self.engine.dispose()


db = Database()


async def get_db():
    async for session in db.get_session():
        yield session
