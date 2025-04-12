import pandas as pd
from sqlmodel import Session

from app.crud.commercialization import create_commercialization, get_by_year_and_product
from app.models.commercialization import CommercializationCreate
from app.services.embrapa.base_ingestor import EmbrapaBaseIngestor


class CommercializationIngestor(EmbrapaBaseIngestor):
    CSV_PATH = "download/Comercio.csv"

    def reshape(self, df: pd.DataFrame) -> pd.DataFrame:
        id_vars = ["Produto"]
        value_vars = [col for col in df.columns if col.isdigit()]
        melted = df.melt(
            id_vars=id_vars,
            value_vars=value_vars,
            var_name="ano",
            value_name="quantidade_litros",
        )
        print(f"Transformed shape: {melted.shape}")
        return melted

    def ingest(self, session: Session):
        df = self.fetch_csv()
        melted = self.reshape(df)

        n_inserts = 0
        n_skipped = 0

        for idx, row in melted.iterrows():
            try:
                year = int(row["ano"])
                product = row["Produto"]

                if get_by_year_and_product(session, year, product):
                    print(f"Skipping duplicate: {year} - {product}")
                    n_skipped += 1
                    continue

                data = CommercializationCreate(
                    year=year,
                    product=product,
                    quantity_liters=float(str(row["quantidade_litros"]).replace(",", "."))
                )
                create_commercialization(session, data)
                n_inserts += 1

            except (ValueError, KeyError, TypeError) as e:
                print(f"Error on row {idx} — data: {row.to_dict()} — {e}")

        print(f"Ingestion completed: {n_inserts} inserted, {n_skipped} skipped.")

