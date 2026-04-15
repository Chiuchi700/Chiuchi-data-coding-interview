from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def get_engine() -> Engine:
    user = "postgres"
    password = "1234"
    host = "localhost"
    port = "5432"
    database = "dw_flights"

    connection_string = (
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    )

    return create_engine(connection_string)