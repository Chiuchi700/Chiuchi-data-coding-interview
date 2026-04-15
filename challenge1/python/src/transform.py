from __future__ import annotations

import pandas as pd


TABLE_CONFIG: dict[str, dict[str, object]] = {
    "airlines": {
        "rename": {},
        "columns": ["carrier", "name"],
        "required": ["carrier", "name"],
        "int_not_null": [],
        "int_nullable": [],
        "float_not_null": [],
        "float_nullable": [],
        "datetime": [],
        "string": ["carrier", "name"],
    },
    "airports": {
        "rename": {
            "lat": "latitude",
            "lon": "longitude",
            "alt": "altitude",
            "tz": "timezone",
            "tzone": "timezone_name",
        },
        "columns": [
            "faa",
            "name",
            "latitude",
            "longitude",
            "altitude",
            "timezone",
            "dst",
            "timezone_name",
        ],
        "required": [
            "faa",
            "name",
            "latitude",
            "longitude",
            "altitude",
            "timezone",
            "dst",
            "timezone_name",
        ],
        "int_not_null": ["timezone"],
        "int_nullable": [],
        "float_not_null": ["latitude", "longitude", "altitude"],
        "float_nullable": [],
        "datetime": [],
        "string": ["faa", "name", "dst", "timezone_name"],
    },
    "planes": {
        "rename": {},
        "columns": [
            "tailnum",
            "year",
            "type",
            "manufacturer",
            "model",
            "engines",
            "seats",
            "speed",
            "engine",
        ],
        "required": [
            "tailnum",
            "type",
            "manufacturer",
            "model",
            "engines",
            "seats",
            "engine",
        ],
        "int_not_null": ["engines", "seats"],
        "int_nullable": ["year"],
        "float_not_null": [],
        "float_nullable": ["speed"],
        "datetime": [],
        "string": ["tailnum", "type", "manufacturer", "model", "engine"],
    },
    "weather": {
        "rename": {},
        "columns": [
            "origin",
            "year",
            "month",
            "day",
            "hour",
            "temp",
            "dewp",
            "humid",
            "wind_dir",
            "wind_speed",
            "wind_gust",
            "precip",
            "pressure",
            "visib",
            "time_hour",
        ],
        "required": ["origin", "year", "month", "day", "hour", "time_hour"],
        "int_not_null": ["year", "month", "day", "hour"],
        "int_nullable": [],
        "float_not_null": [],
        "float_nullable": [
            "temp",
            "dewp",
            "humid",
            "wind_dir",
            "wind_speed",
            "wind_gust",
            "precip",
            "pressure",
            "visib",
        ],
        "datetime": ["time_hour"],
        "string": ["origin"],
    },
    "flights": {
        "rename": {
            "dep_time": "actual_dep_time",
            "arr_time": "actual_arr_time",
        },
        "columns": [
            "carrier",
            "flight",
            "year",
            "month",
            "day",
            "hour",
            "minute",
            "actual_dep_time",
            "sched_dep_time",
            "dep_delay",
            "actual_arr_time",
            "sched_arr_time",
            "arr_delay",
            "tailnum",
            "origin",
            "dest",
            "air_time",
            "distance",
            "time_hour",
        ],
        "required": [
            "carrier",
            "flight",
            "year",
            "month",
            "day",
            "hour",
            "minute",
            "tailnum",
            "origin",
            "dest",
            "air_time",
            "distance",
            "time_hour",
        ],
        "int_not_null": ["flight", "year", "month", "day", "hour", "minute"],
        "int_nullable": [
            "actual_dep_time",
            "sched_dep_time",
            "dep_delay",
            "actual_arr_time",
            "sched_arr_time",
            "arr_delay",
        ],
        "float_not_null": ["air_time", "distance"],
        "float_nullable": [],
        "datetime": ["time_hour"],
        "string": ["carrier", "tailnum", "origin", "dest"],
    },
}


def _drop_unnamed_columns(df: pd.DataFrame) -> pd.DataFrame:
    unnamed_cols = [col for col in df.columns if str(col).startswith("Unnamed:")]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)
    return df


def transform_dataframe(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    config = TABLE_CONFIG[table_name]
    df = df.copy()

    df = _drop_unnamed_columns(df)
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    df = df.rename(columns=config["rename"])  # type: ignore[arg-type]
    df = df.drop_duplicates()

    expected_columns = config["columns"]  # type: ignore[assignment]
    df = df[expected_columns]

    for col in config["int_nullable"]:  # type: ignore[index]
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    for col in config["int_not_null"]:  # type: ignore[index]
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    for col in config["float_nullable"]:  # type: ignore[index]
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in config["float_not_null"]:  # type: ignore[index]
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in config["datetime"]:  # type: ignore[index]
        df[col] = pd.to_datetime(df[col], errors="coerce", utc=True)

    for col in config["string"]:  # type: ignore[index]
        df[col] = df[col].astype("string").str.strip()

    required_columns = config["required"]  # type: ignore[assignment]
    df = df.dropna(subset=required_columns)

    for col in config["int_not_null"]:  # type: ignore[index]
        df[col] = df[col].astype(int)

    return df