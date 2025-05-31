import logging

import pandas as pd
from sqlmodel import Session

from app.core.base_ingestor import EmbrapaBaseIngestor
from app.importation.constants import (
    CATEGORY_MAPPING,
    IMPORTATION_PATHS,
    INVALID_VALUES,
)
from app.importation.crud import (
    create_importation,
    get_by_year_and_country_and_category,
)
from app.importation.models import ImportationCreate

logger = logging.getLogger(__name__)


class ImportationIngestor(EmbrapaBaseIngestor):
    PATHS = IMPORTATION_PATHS

    def ingest(self, session: Session):
        n_inserts = n_skipped = 0

        for path in self.PATHS:
            self.CSV_PATH = path
            category = CATEGORY_MAPPING[path]
            separator = ";" if "ImpSuco" in path else "\t"

            df = self.fetch_csv(path, separator)
            melted = self._prepare_dataframe(df, category)

            for _, row in melted.iterrows():
                if get_by_year_and_country_and_category(
                    session,
                    row["year"],
                    row["country"],
                    row["category"],
                ):
                    n_skipped += 1
                    continue

                try:
                    data = ImportationCreate(
                        year=row["year"],
                        country=row["country"],
                        quantity_kg=row["quantity_kg"],
                        category=row["category"],
                    )
                    create_importation(session, data)
                    n_inserts += 1
                except Exception as e:
                    logger.warning(f"Error inserting row — {row.to_dict()} — {e}")

        logger.info(
            f"Importation ingestion complete: {n_inserts} inserted, {n_skipped} skipped."
        )

    def _prepare_dataframe(self, df: pd.DataFrame, category: str) -> pd.DataFrame:
        df = df.drop(columns=["Id"], errors="ignore")

        year_cols = [col for col in df.columns if col.isdigit()]
        df = df.melt(
            id_vars=["País"],
            value_vars=year_cols,
            var_name="year",
            value_name="quantity_kg",
        )

        df = df.dropna(subset=["year", "quantity_kg"])
        df["year"] = df["year"].astype(int)

        df["quantity_kg"] = (
            df["quantity_kg"]
            .astype(str)
            .str.lower()
            .str.replace(",", ".", regex=False)
            .apply(lambda x: x if x not in INVALID_VALUES else "0")
            .astype(float)
            .round()
            .astype(int)
        )

        df = df.rename(columns={"País": "country"})
        df["category"] = category

        logger.info(f"Transformed {category} data: {df.shape}")
        return df
