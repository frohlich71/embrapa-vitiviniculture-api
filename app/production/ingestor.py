import logging

import numpy as np
import pandas as pd
from sqlmodel import Session

from app.production.constants import Category
from app.production.crud import create_production, get_by
from app.production.models import ProductionCreate
from app.core.base_ingestor import EmbrapaBaseIngestor

logger = logging.getLogger(__name__)


class ProductionIngestor(EmbrapaBaseIngestor):
    CSV_PATH = "download/Producao.csv"

    CATEGORY_PREFIXES = {
        "vm_": Category.VINHO_DE_MESA,
        "vv_": Category.VINHO_FINO_DE_MESA_VINIFERA,
        "su_": Category.SUCO,
        "de_": Category.DERIVADOS,
    }

    REQUIRED_COLUMNS = {"produto", "control"}

    def ingest(self, session: Session):
        df = self.fetch_csv()
        transformed = self._prepare_dataframe(df)

        n_inserts = n_skipped = 0

        for _, row in transformed.iterrows():
            if get_by(session, row["ano"], row["produto"], row["category"]):
                n_skipped += 1
                continue

            try:
                data = ProductionCreate(
                    year=row["ano"],
                    product=row["produto"],
                    quantity_liters=row["quantidade_litros"],
                    category=row["category"],
                )
                create_production(session, data)
                n_inserts += 1
            except Exception as e:
                logger.warning(
                    f"Error inserting row — year: {row['ano']}, product: {row['produto']} — {e}"
                )

        logger.info(f"Ingestion completed: {n_inserts} inserted, {n_skipped} skipped.")

    def _prepare_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.drop(columns=["id"], errors="ignore")

        missing = self.REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns in CSV: {missing}")

        # Map category based on control prefix using numpy
        conditions = [
            df["control"].str.startswith(prefix) for prefix in self.CATEGORY_PREFIXES
        ]
        categories = [cat.value for cat in self.CATEGORY_PREFIXES.values()]
        df["category"] = np.select(conditions, categories, default="")

        # Remove rows without valid category
        df = df[df["category"] != ""]

        year_cols = [col for col in df.columns if col.isdigit()]
        df = df.melt(
            id_vars=["produto", "category"],
            value_vars=year_cols,
            var_name="ano",
            value_name="quantidade_litros",
        )

        df = df.dropna(subset=["ano", "quantidade_litros"])
        df["ano"] = df["ano"].astype(int)
        df["quantidade_litros"] = df["quantidade_litros"].astype(int)

        logger.info(f"Transformed shape: {df.shape}")
        return df
