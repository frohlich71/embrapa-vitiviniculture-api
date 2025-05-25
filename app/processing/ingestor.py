import logging

import pandas as pd
from sqlmodel import Session

from app.processing.crud import (
    create_processing,
    get_by_year_and_cultivate_and_category,
)
from app.processing.models import ProcessingCreate
from app.services.embrapa.base_ingestor import EmbrapaBaseIngestor

logger = logging.getLogger(__name__)


class ProcessingIngestor(EmbrapaBaseIngestor):
    PATHS = [
        "download/ProcessaViniferas.csv",
        "download/ProcessaAmericanas.csv",
        "download/ProcessaMesa.csv",
        "download/ProcessaSemclass.csv",
    ]

    CATEGORIES = {
        "download/ProcessaViniferas.csv": "VINIFERA",
        "download/ProcessaAmericanas.csv": "AMERICANAS",
        "download/ProcessaMesa.csv": "MESA",
        "download/ProcessaSemclass.csv": "SEM CLASSIFICACAO",
    }

    SUBCATEGORY_PREFIXES = {
        "AMERICANAS": {
            "ti_": "TINTAS",
            "br_": "BRANCAS E ROSADAS",
        },
        "MESA": {
            "ti_": "TINTAS",
            "br_": "BRANCAS",
        },
        "VINIFERA": {
            "ti_": "TINTAS",
            "br_": "BRANCAS E ROSADAS",
        },
    }

    def ingest(self, session: Session):
        n_inserts = n_skipped = 0

        for path in self.PATHS:
            self.CSV_PATH = path
            category = self.CATEGORIES[path]
            separator = ";" if "Viniferas" in path else "\t"

            df = self.fetch_csv(path, separator)
            melted = self._prepare_dataframe(df, category)

            for _, row in melted.iterrows():
                if get_by_year_and_cultivate_and_category(
                    session,
                    row["ano"],
                    row["cultivar"],
                    row["category"],
                    row["subcategory"],
                ):
                    n_skipped += 1
                    continue

                try:
                    data = ProcessingCreate(
                        year=row["ano"],
                        cultivate=row["cultivar"],
                        quantity_kg=row["quantidade_kg"],
                        category=row["category"],
                        subcategory=row["subcategory"],
                    )
                    create_processing(session, data)
                    n_inserts += 1
                except Exception as e:
                    logger.warning(f"Error inserting row — {row.to_dict()} — {e}")

        logger.info(
            f"Processing ingestion complete: {n_inserts} inserted, {n_skipped} skipped."
        )

    def _prepare_dataframe(self, df: pd.DataFrame, category: str) -> pd.DataFrame:
        df = df.drop(columns=["id"], errors="ignore")

        year_cols = [col for col in df.columns if col.isdigit()]
        df = df.melt(
            id_vars=["cultivar", "control"],
            value_vars=year_cols,
            var_name="ano",
            value_name="quantidade_kg",
        )

        df = df.dropna(subset=["ano", "quantidade_kg"])
        df["ano"] = df["ano"].astype(int)

        df["quantidade_kg"] = (
            df["quantidade_kg"]
            .astype(str)
            .str.lower()
            .str.replace(",", ".", regex=False)
            .apply(lambda x: x if x not in {"nd", "+", "*"} else "0")
            .astype(float)
            .astype(int)
        )

        df["category"] = category
        df["subcategory"] = df["control"].apply(
            lambda c: self._extract_subcategory(category, c)
        )
        df = df[
            ~((df["subcategory"] == "") & (df["category"] != "SEM CLASSIFICACAO"))
        ].drop(columns=["control"])

        logger.info(f"Transformed {category} data: {df.shape}")
        return df

    def _extract_subcategory(self, category: str, control_value: str) -> str:
        prefixes = self.SUBCATEGORY_PREFIXES.get(category, {})
        for prefix, subcat in prefixes.items():
            if control_value.startswith(prefix):
                return subcat
        return ""
