import pandas as pd
from sqlmodel import Session
import logging

from app.core.base_ingestor import EmbrapaBaseIngestor
from app.exportation.crud import create_exportation, get_by_year_and_country_and_category
from app.exportation.models import ExportationCreate
from app.exportation.constants import EXPORTATION_PATHS, CATEGORY_MAPPING, INVALID_VALUES

logger = logging.getLogger(__name__)


class ExportationIngestor(EmbrapaBaseIngestor):
    """Ingestor for exportation data from CSV files."""

    def ingest(self, session: Session):
        """Ingest exportation data from all CSV files."""
        n_inserts = 0
        n_skipped = 0

        for path in EXPORTATION_PATHS:
            logger.info(f"Processing {path}...")
            
            # Set CSV_PATH for base class
            self.CSV_PATH = path
            
            # Get category from file path
            category = CATEGORY_MAPPING[path]
            
            # Use tab separator for all exportation files
            df = self.fetch_csv(separator="\t")
            
            # Transform dataframe
            df_transformed = self._prepare_dataframe(df, category)

            # Insert data
            for _, row in df_transformed.iterrows():
                try:
                    # Check if record already exists
                    existing = get_by_year_and_country_and_category(
                        session, row["year"], row["country"], category
                    )
                    if existing:
                        n_skipped += 1
                        continue

                    # Create and insert new record
                    data = ExportationCreate(
                        year=row["year"],
                        country=row["country"],
                        quantity_kg=row["quantity_kg"],
                        value=row["value"],
                        category=row["category"],
                    )
                    create_exportation(session, data)
                    n_inserts += 1
                except Exception as e:
                    logger.warning(f"Error inserting row — {row.to_dict()} — {e}")

        logger.info(
            f"Exportation ingestion complete: {n_inserts} inserted, {n_skipped} skipped."
        )

    def _prepare_dataframe(self, df: pd.DataFrame, category: str) -> pd.DataFrame:
        """Transform raw CSV data into the required format."""
        df = df.drop(columns=["Id"], errors="ignore")

        # Find year columns - each year appears twice: YYYY (quantity) and YYYY.1 (value)
        year_cols = [col for col in df.columns if col.isdigit()]
        
        # Create a list to store all processed rows
        processed_rows = []
        
        for year_col in year_cols:
            year = int(year_col)
            quantity_col = year_col  # e.g., "1970"
            value_col = f"{year_col}.1"  # e.g., "1970.1"
            
            # Check if both columns exist
            if quantity_col in df.columns and value_col in df.columns:
                for _, row in df.iterrows():
                    country = row["País"]
                    quantity_kg = row[quantity_col]
                    value = row[value_col]
                    
                    processed_rows.append({
                        "country": country,
                        "year": year,
                        "quantity_kg": quantity_kg,
                        "value": value,
                        "category": category
                    })
            elif quantity_col in df.columns:
                # Only quantity column exists
                for _, row in df.iterrows():
                    country = row["País"]
                    quantity_kg = row[quantity_col]
                    
                    processed_rows.append({
                        "country": country,
                        "year": year,
                        "quantity_kg": quantity_kg,
                        "value": 0,  # No value data available
                        "category": category
                    })
        
        # Create new DataFrame from processed rows
        df_processed = pd.DataFrame(processed_rows)
        
        # Clean and convert data
        df_processed = df_processed.dropna(subset=["year", "quantity_kg"])
        
        # Process quantity_kg - convert to int with rounding
        df_processed["quantity_kg"] = (
            df_processed["quantity_kg"]
            .astype(str)
            .str.lower()
            .str.replace(",", ".", regex=False)
            .apply(lambda x: x if x not in INVALID_VALUES else "0")
            .astype(float)
            .round()
            .astype(int)
        )
        
        # Process value - convert to int with rounding
        df_processed["value"] = (
            df_processed["value"]
            .astype(str)
            .str.lower()
            .str.replace(",", ".", regex=False)
            .apply(lambda x: x if x not in INVALID_VALUES else "0")
            .astype(float)
            .round()
            .astype(int)
        )

        logger.info(f"Transformed {category} data: {df_processed.shape}")
        return df_processed
