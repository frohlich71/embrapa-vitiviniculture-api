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
        Fallback: if download fails, load from local 'resources/' folder.
        """
        path = url or self.CSV_PATH
        full_url = f"{self.BASE_URL}/{path}"
        try:
            response = httpx.get(full_url, timeout=10.0, trust_env=False)
            response.raise_for_status()
            df = pd.read_csv(StringIO(response.text), sep=separator, encoding="latin1")
            print(f"Loaded CSV: {full_url} with shape: {df.shape}")
            return df
        except Exception as e:
            print(f"[WARN] Falha ao baixar CSV de {full_url}: {e}")
            print(os.path.basename(path))
            local_path = os.path.join(os.path.dirname(__file__), "..", "..", "resources", os.path.basename(path))
            local_path = os.path.abspath(local_path)
            print(f"Tentando carregar CSV local: {local_path}")
            df = pd.read_csv(local_path, sep=separator, encoding="latin1")
            print(f"Loaded local CSV: {local_path} with shape: {df.shape}")
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
