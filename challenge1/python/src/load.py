import pandas as pd
from sqlalchemy.engine import Engine


def load_to_postgres(df: pd.DataFrame, table_name: str, engine: Engine) -> None:
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
    )