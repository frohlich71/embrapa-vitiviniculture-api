import abc
import httpx
import pandas as pd
from io import StringIO

class EmbrapaBaseIngestor(abc.ABC):
    """
    Abstract base class for Embrapa data ingestion.
    """

    BASE_URL = "http://vitibrasil.cnpuv.embrapa.br"
    CSV_PATH: str  # to be defined in subclasses
    id_column: str = "produto"

    def fetch_csv(self) -> pd.DataFrame:
        """
        Download CSV from the given URL and return as a DataFrame.
        """
        full_url = f"{self.BASE_URL}/{self.CSV_PATH}"
        response = httpx.get(full_url)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text), sep=";", encoding="latin1")
        print(f"✅ Loaded CSV: {full_url} with shape: {df.shape}")
        return df

    def reshape(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert wide format to long format (year-wise pivot).
        """
        id_vars = [self.id_column]
        value_vars = [col for col in df.columns if col.isdigit()]
        melted = df.melt(id_vars=id_vars, value_vars=value_vars,
                         var_name="ano", value_name="quantidade_litros")
        print(f"🔄 Transformed shape: {melted.shape}")
        return melted

    @abc.abstractmethod
    def ingest(self, session):
        """
        Abstract method to implement ingestion into the database.
        """
        pass
