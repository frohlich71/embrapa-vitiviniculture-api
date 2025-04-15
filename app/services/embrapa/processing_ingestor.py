import pandas as pd
from sqlmodel import Session

from app.crud.processing import get_by_year_and_cultivate_and_path, create_processing
from app.models.processing import ProcessingCreate
from app.services.embrapa.base_ingestor import EmbrapaBaseIngestor


class ProcessingIngestor(EmbrapaBaseIngestor):
    PATHS = ["download/ProcessaViniferas.csv", "download/ProcessaAmericanas.csv", "download/ProcessaMesa.csv", "download/ProcessaSemclass.csv"]	

    def reshape(self, df: pd.DataFrame) -> pd.DataFrame:
        id_vars = ["cultivar"]
        value_vars = [col for col in df.columns if col.isdigit()]
        melted = df.melt(
            id_vars=id_vars,
            value_vars=value_vars,
            var_name="ano",
            value_name="quantidade_kg",
        )
        print(f"Transformed shape: {melted.shape}")
        return melted

    def ingest(self, session: Session):
        n_inserts = 0
        n_skipped = 0
        
        for path in self.PATHS:
            separator =  ";" if path == "download/ProcessaViniferas.csv" else "\t"

            df = self.fetch_csv(path, separator)
            melted = self.reshape(df)

            for idx, row in melted.iterrows():
                try:
                    year = int(row["ano"])
                    cultivate = row["cultivar"]

                    if get_by_year_and_cultivate_and_path(session, year, cultivate, path):
                        print(f"Skipping duplicate: {year} - {cultivate} - {path}")
                        n_skipped += 1
                        continue

                    is_valid_qtd = True

                    valores_invalidos = {"nd", "+", "*"}

                    if row["quantidade_kg"] in valores_invalidos or pd.isna(row["quantidade_kg"]):
                        is_valid_qtd = False

                    qtd = float(str(row["quantidade_kg"]).replace(",", ".")) if is_valid_qtd else 0.0



                    data = ProcessingCreate(
                        year=year,
                        cultivate=cultivate,
                        quantity_kg=qtd,
                        path=path.split("/")[1].split(".")[0]
                    )
                    create_processing(session, data)
                    n_inserts += 1

                except (ValueError, KeyError, TypeError) as e:
                    print(f"Error on row {idx} — data: {row.to_dict()} — {e}")

        print(f"Ingestion completed: {n_inserts} inserted, {n_skipped} skipped.")




