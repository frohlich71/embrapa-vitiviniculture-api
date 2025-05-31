from enum import Enum


class Category(str, Enum):
    VINHO_DE_MESA = "vinho-de-mesa"
    VINHO_FINO_DE_MESA_VINIFERA = "vinho-fino-de-mesa-vinifera"
    SUCO = "suco"
    DERIVADOS = "derivados"
