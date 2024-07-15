from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from ..core.config import settings

# Define the database URL based on the settings configuration.
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create an asynchronous database engine with the specified database URL.
# `echo=True` enables SQL logging for debugging purposes.
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create an asynchronous session maker bound to the engine.
# This session maker is used to generate new database sessions.
# `autocommit=False` ensures that transactions are managed manually.
# `autoflush=False` disables automatic flushing of the session.
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
