import abc
import os
from io import StringIO

import httpx
import pandas as pd


class EmbrapaBaseIngestor(abc.ABC):
    """
    Abstract base class for Embrapa data ingestion.
    """
    BASE_URL = os.getenv("EMBRAPA_BASE_URL", "http://vitibrasil.cnpuv.embrapa.br")
    CSV_PATH: str # to be defined in subclasses

    def fetch_csv(self, url: str = None, separator: str = ";") -> pd.DataFrame:
        """
        Download CSV from the given URL and return as a DataFrame.
        """
        path = url or self.CSV_PATH
        full_url = f"{self.BASE_URL}/{path}"
        response = httpx.get(full_url)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text), sep=separator, encoding="latin1")
        print(f"Loaded CSV: {full_url} with shape: {df.shape}")
        return df

    @abc.abstractmethod
    def reshape(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert wide format to long format (year-wise pivot).
        """
        raise NotImplementedError("Subclasses must implement the reshape method.")

    @abc.abstractmethod
    def ingest(self, session):
        """
        Abstract method to implement ingestion into the database.
        """
        raise NotImplementedError("Subclasses must implement the ingest method.")
