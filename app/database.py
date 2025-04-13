from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# EN: Database URL for SQLite
# BR: URL do banco de dados para SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./focused.db"

# EN: Create an engine for SQLite
# BR: Crie um mecanismo para SQLite
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# EN: Create a session local to interact with the database
# BR: Crie uma sessão local para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# EN: Define the base class for the ORM models
# BR: Defina a classe base para os modelos ORM
Base = declarative_base()

# EN: Dependency for getting a database session
# BR: Dependência para obter uma sessão de banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
