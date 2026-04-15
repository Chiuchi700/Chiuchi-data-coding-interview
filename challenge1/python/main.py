from pathlib import Path

from src.db import get_engine
from src.extract import read_csv_file
from src.transform import transform_dataframe
from src.load import load_to_postgres


FILE_TABLE_MAPPING: list[tuple[str, str]] = [
    ("nyc_airlines.csv", "airlines"),
    ("nyc_airports.csv", "airports"),
    ("nyc_planes.csv", "planes"),
    ("nyc_weather.csv", "weather"),
    ("nyc_flights.csv", "flights"),
]


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def process_table(file_name: str, table_name: str, row_limit: int | None = None) -> None:
    project_root = get_project_root()
    file_path = project_root / "challenge1/dataset" / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    print(f"\n[INFO] Processando {file_name} -> {table_name}")

    df = read_csv_file(file_path)
    print(f"[INFO] Linhas lidas: {len(df)}")

    df = transform_dataframe(df, table_name=table_name)

    if row_limit is not None:
        df = df.head(row_limit)

    print(f"[INFO] Linhas após transformação: {len(df)}")
    print(f"[INFO] Colunas finais: {df.columns.tolist()}")

    engine = get_engine()
    load_to_postgres(df=df, table_name=table_name, engine=engine)

    print(f"[INFO] Carga concluída na tabela {table_name}")


def main() -> None:
    print("[INFO] Iniciando carga das tabelas...")

    # coloque row_limit=10 para testes iniciais
    row_limit = 2000

    for file_name, table_name in FILE_TABLE_MAPPING:
        process_table(file_name=file_name, table_name=table_name, row_limit=row_limit)

    print("\n[INFO] Pipeline finalizado com sucesso.")


if __name__ == "__main__":
    main()