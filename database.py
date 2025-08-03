from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib
import os

# Variables de entorno o configuralas directamente (recomendado usar .env)
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
SERVER = os.getenv("DB_SERVER")
DATABASE = os.getenv("DB_NAME")

# Armado de la cadena de conexión
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER=tcp:{SERVER},1433;"
    f"DATABASE={DATABASE};"
    f"UID={USER};"
    f"PWD={PASSWORD};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Connection Timeout=30;"
)

# Crear engine y sesión
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

SEARCH_TABLE = "searches"
SEARCH_CLASS = "Search"

USER_TABLE = "users"
USER_CLASS = "User"

SEARCH_PARTICIPANT_TABLE = "search_participants"
SEARCH_PARTICIPANT_CLASS = "SearchParticipant"

SEARCH_DEPARTMENT_TABLE = "search_departments"
SEARCH_DEPARTMENT_CLASS = "SearchDepartment"

DEPARTMENT_TABLE = "departments"
DEPARTMENT_CLASS = "Department"

PARTICIPANT_REACTION_TABLE = "participant_reactions"
PARTICIPANT_REACTION_CLASS = "ParticipantReaction"

PARTICIPANT_COMMENT_TABLE = "participant_comments"
PARTICIPANT_COMMENT_CLASS = "ParticipantComment"


