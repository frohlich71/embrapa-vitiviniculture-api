from enum import Enum


class Category(str, Enum):
    """Exportation categories based on CSV file structure."""

    VINHO = "vinho"
    ESPUMANTES = "espumantes"
    UVA = "uva"
    SUCO = "suco"


# Mapping from CSV file paths to categories
CATEGORY_MAPPING = {
    "download/ExpVinho.csv": Category.VINHO,
    "download/ExpEspumantes.csv": Category.ESPUMANTES,
    "download/ExpUva.csv": Category.UVA,
    "download/ExpSuco.csv": Category.SUCO,
}

# List of exportation file paths
EXPORTATION_PATHS = list(CATEGORY_MAPPING.keys())

# Invalid values that should be converted to 0
INVALID_VALUES = {"nan", "na", "-", "", "null", "none"}
