# Importation module constants
from enum import Enum

# File paths for importation data ingestion
IMPORTATION_PATHS = [
    "download/ImpVinhos.csv",
    "download/ImpEspumantes.csv",
    "download/ImpFrescas.csv",
    "download/ImpPassas.csv",
    "download/ImpSuco.csv",
]


# Categories for importation data based on file types
class Category(str, Enum):
    VINHOS = "vinhos"  # ImpVinhos.csv
    ESPUMANTES = "espumantes"  # ImpEspumantes.csv
    FRESCAS = "frescas"  # ImpFrescas.csv
    PASSAS = "passas"  # ImpPassas.csv
    SUCO = "suco"  # ImpSuco.csv


# Mapping from file paths to categories
CATEGORY_MAPPING = {
    "download/ImpVinhos.csv": Category.VINHOS,
    "download/ImpEspumantes.csv": Category.ESPUMANTES,
    "download/ImpFrescas.csv": Category.FRESCAS,
    "download/ImpPassas.csv": Category.PASSAS,
    "download/ImpSuco.csv": Category.SUCO,
}

# Invalid values found in importation data
INVALID_VALUES = {"nd", "+", "*"}
