from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection URL for Heroku PostgreSQL
DATABASE_URL = "postgresql+psycopg2://u6qhu6arohg419:p74b3e103ae841ccf6665754710cff650a4f3d50c41701a34e716a9971084e8f0@c5p86clmevrg5s.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d2hsf54fj86798"

# Create the SQLAlchemy engine
# pool_pre_ping ensures the connection is valid before using it
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# SessionLocal factory for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

# Example usage to verify the connection
if __name__ == "__main__":
    try:
        # Attempt to connect to the database
        with engine.connect() as connection:
            print("Database connected successfully.")
    except Exception as e:
        print(f"Error connecting to the database: {e}")
