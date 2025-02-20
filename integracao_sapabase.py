from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("postgres")
PASSWORD = os.getenv("1993")
HOST = os.getenv("localhost")
PORT = os.getenv("5432")
DBNAME = os.getenv("ads_database_ser")

# Construct the SQLAlchemy connection string
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)
# Disable SQLAlchemy client-side pooling by using NullPool
"https://docs.sqlalchemy.org/en/20/core/pooling.html#switching-pool-implementations"
engine = create_engine(DATABASE_URL, poolclass=NullPool)

# Test the connection
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")