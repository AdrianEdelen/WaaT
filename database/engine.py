from sqlalchemy import create_engine
from utils.env_manager import EnvManager
from utils.check_sql_directory import ensure_directory_for_sqlite



db_url = EnvManager().DATABASE_URL
ensure_directory_for_sqlite(db_url=db_url)
engine = create_engine(db_url)