import shutil
import pathlib
import kuzu
from demo.create import create_kuzu_tables
from demo.copy import ingest_data_to_kuzu_tables


def run_create_and_copy():
    # set data to be used throughout notebook
    parquet_dir = "data/g2c_lite_2.8.4.full.with-metanames.dataset.parquet"

    kuzu_dir = parquet_dir.replace(".parquet", ".kuzu")

    dataset_name_to_cypher_table_type_map = {"nodes": "node", "edges": "rel"}

    print(f"Kuzu dir: {kuzu_dir}")

    # create path for the kuzu database to reside
    if pathlib.Path(kuzu_dir).is_dir():
        shutil.rmtree(kuzu_dir)
    pathlib.Path(kuzu_dir).mkdir(exist_ok=True)

    # init a Kuzu database and connection
    db = kuzu.Database(f"{kuzu_dir}")
    kz_conn = kuzu.Connection(db)

    create_kuzu_tables(
        parquet_dir=parquet_dir,
        kz_conn=kz_conn,
        dataset_name_to_cypher_table_type_map=dataset_name_to_cypher_table_type_map,
    )

    ingest_data_to_kuzu_tables(
        parquet_dir=parquet_dir,
        kz_conn=kz_conn,
        dataset_name_to_cypher_table_type_map=dataset_name_to_cypher_table_type_map,
    )