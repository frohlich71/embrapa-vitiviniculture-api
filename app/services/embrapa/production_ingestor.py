from sqlmodel import Session
from app.services.embrapa.base_ingestor import EmbrapaBaseIngestor
from app.models.production import ProductionCreate
from app.crud.production import create_production, get_by_year_and_product

class ProductionIngestor(EmbrapaBaseIngestor):
    CSV_PATH = "download/Producao.csv"

    def ingest(self, session: Session):
        df = self.fetch_csv()
        melted = self.reshape(df)

        n_inserts = 0
        n_skipped = 0

        for idx, row in melted.iterrows():
            try:
                year = int(row["ano"])
                product = row["produto"]

                if get_by_year_and_product(session, year, product):
                    print(f"🔁 Skipping duplicate: {year} - {product}")
                    n_skipped += 1
                    continue

                data = ProductionCreate(
                    year=year,
                    state="Brasil",
                    product=product,
                    quantity_liters=float(str(row["quantidade_litros"]).replace(",", "."))
                )
                create_production(session, data)
                n_inserts += 1

            except (ValueError, KeyError, TypeError) as e:
                print(f"⚠️ Error on row {idx} — data: {row.to_dict()} — {e}")

        print(f"✅ Ingestion completed: {n_inserts} inserted, {n_skipped} skipped.")
