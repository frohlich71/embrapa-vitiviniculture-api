import pandas as pd
from sqlmodel import Session

from app.exportation.crud import create_exportation, get_by_year_and_country_and_path
from app.exportation.models import ExportationCreate
from app.core.base_ingestor import EmbrapaBaseIngestor


class ExportationIngestor(EmbrapaBaseIngestor):
    PATHS = [
        "download/ExpVinho.csv",
        "download/ExpEspumantes.csv",
        "download/ExpUva.csv",
        "download/ExpSuco.csv",
    ]

    def reshape(self, df: pd.DataFrame) -> pd.DataFrame:
        id_vars = ["pais"]  # Alterado para "pais"
        value_vars = [col for col in df.columns if col.isdigit()]

        # Transformação das colunas de 'ano' e 'quantidade'
        melted = df.melt(
            id_vars=id_vars,
            value_vars=value_vars,
            var_name="ano",
            value_name="quantidade",
        )

        # Adicionada uma nova coluna de 'valores'
        melted["valores"] = df["valor"]

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
                    country = row["pais"]

                    # Verifica se já existe o dado para o ano, país e arquivo
                    if get_by_year_and_country_and_path(session, year, country, path):
                        print(f"Skipping duplicate: {year} - {country} - {path}")
                        n_skipped += 1
                        continue

                    is_valid_quantidade = True
                    is_valid_valor = True

                    valores_invalidos = {"nd", "+", "*"}
                    if row["quantidade"] in valores_invalidos or pd.isna(
                        row["quantidade"]
                    ):
                        is_valid_quantidade = False
                    if row["valores"] in valores_invalidos or pd.isna(row["valores"]):
                        is_valid_valor = False

                    # Converte as quantidades e valores (presumindo que os dados são numéricos)
                    quantidade = (
                        float(str(row["quantidade"]).replace(",", "."))
                        if is_valid_quantidade
                        else 0.0
                    )
                    valor = (
                        float(str(row["valores"]).replace(",", "."))
                        if is_valid_valor
                        else 0.0
                    )

                    # Cria o objeto de dados para inserção
                    data = ExportationCreate(
                        year=year,
                        country=country,
                        quantity_kg=quantidade,
                        value=valor,
                        path=path.split("/")[1].split(".")[0],
                    )
                    create_exportation(session, data)
                    n_inserts += 1

                except (ValueError, KeyError, TypeError) as e:
                    print(f"Error on row {idx} — data: {row.to_dict()} — {e}")

        print(f"Ingestion completed: {n_inserts} inserted, {n_skipped} skipped.")
