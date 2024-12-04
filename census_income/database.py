from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Database connection URL (read from environment variables for security)
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/Census Data"
)

# Create the SQLAlchemy engine
# pool_pre_ping ensures the connection is valid before using it
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# SessionLocal factory for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

# Example usage (remove this in production)
if __name__ == "__main__":
    try:
        # Attempt to connect to the database
        with engine.connect() as connection:
            print("Database connected successfully.")
    except Exception as e:
        print(f"Error connecting to the database: {e}")
