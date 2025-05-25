import pandas as pd
from sqlmodel import Session

from app.crud.importation import get_by_year_and_country_and_path, create_importation
from app.models.importation import ImportationCreate
from app.services.embrapa.base_ingestor import EmbrapaBaseIngestor


class ImportationIngestor(EmbrapaBaseIngestor):
    PATHS = [
        "download/ImpVinhos.csv",
        "download/ImpEspumantes.csv",
        "download/ImpFrescas.csv",
        "download/ImpPassas.csv",
        "download/ImpSuco.csv",
    ]

    def reshape(self, df: pd.DataFrame) -> pd.DataFrame:
        id_vars = ["País"]  # Mantemos "País" como identificador
        value_vars = [col for col in df.columns if col.isdigit()]  # Só anos

        # Transformação dos dados
        melted = df.melt(
            id_vars=id_vars,
            value_vars=value_vars,
            var_name="ano",
            value_name="quantidade",
        )

        print(f"Transformed shape: {melted.shape}")
        return melted

    def ingest(self, session: Session):
        n_inserts = 0
        n_skipped = 0

        for path in self.PATHS:
            separator = ";" if path == "download/ImpSuco.csv" else "\t"

            df = self.fetch_csv(path, separator)
            melted = self.reshape(df)

            for idx, row in melted.iterrows():
                try:
                    year = int(row["ano"])
                    country = row["País"]

                    # Verifica se já existe
                    if get_by_year_and_country_and_path(session, year, country, path):
                        print(f"Skipping duplicate: {year} - {country} - {path}")
                        n_skipped += 1
                        continue

                    valores_invalidos = {"nd", "+", "*"}
                    quantidade_raw = str(row["quantidade"])

                    # Checagem de validade
                    if quantidade_raw in valores_invalidos or pd.isna(
                        row["quantidade"]
                    ):
                        quantidade = 0.0
                    else:
                        quantidade = float(quantidade_raw.replace(",", "."))

                    # Criação do registro
                    data = ImportationCreate(
                        year=year,
                        country=country,
                        quantity_kg=quantidade,
                        path=path.split("/")[1].split(".")[0],
                    )
                    create_importation(session, data)
                    n_inserts += 1

                except (ValueError, KeyError, TypeError) as e:
                    print(f"Error on row {idx} — data: {row.to_dict()} — {e}")

        print(f"Ingestion completed: {n_inserts} inserted, {n_skipped} skipped.")
