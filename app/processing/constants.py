from enum import Enum


class Category(str, Enum):
    VINIFERA = "vinifera"
    AMERICANAS = "americanas"
    MESA = "mesa"
    SEM_CLASSIFICACAO = "sem-classificacao"


class Subcategory(str, Enum):
    TINTAS = "tintas"
    BRANCAS = "brancas"
    BRANCAS_E_ROSADAS = "brancas-e-rosadas"
