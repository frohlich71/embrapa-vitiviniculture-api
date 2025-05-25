import abc
import os
import logging
from io import StringIO

import httpx
import pandas as pd

logger = logging.getLogger(__name__)


class EmbrapaBaseIngestor(abc.ABC):
    """
    Base class for ingesting Embrapa CSV data.
    """
    BASE_URL = os.getenv("EMBRAPA_BASE_URL", "http://vitibrasil.cnpuv.embrapa.br")
    CSV_PATH: str  # should be defined in subclasses

    def fetch_csv(self, url: str = None, separator: str = ";") -> pd.DataFrame:
        """
        Download CSV from EMBRAPA or load from local 'downloads' folder.
        Priority:
        1. Load from self.CSV_PATH if it exists.
        2. Try to download from remote URL.
        """
        if os.path.exists(self.CSV_PATH):
            return self._load_csv(self.CSV_PATH, separator)

        path = url or self.CSV_PATH
        full_url = f"{self.BASE_URL}/{path}"

        try:
            response = httpx.get(full_url, timeout=10.0, trust_env=False)
            response.raise_for_status()
            df = pd.read_csv(StringIO(response.text), sep=separator, encoding="utf-8")
            logger.info(f"Downloaded CSV from {full_url} (shape={df.shape})")
            return df
        except Exception as e:
            logger.warning(f"Failed to fetch {full_url}: {e}")
            raise RuntimeError(f"Unable to download CSV from {full_url}")

    def _load_csv(self, filepath: str, separator: str) -> pd.DataFrame:
        df = pd.read_csv(filepath, sep=separator, encoding="utf-8")
        logger.info(f"Loaded CSV from {filepath} (shape={df.shape})")
        return df

    @abc.abstractmethod
    def ingest(self, session):
        """
        Ingest transformed data into the database.
        """
        raise NotImplementedError("Subclasses must implement the ingest method.")
