# mapping.py
import re

DIRECT_MAP = {
    "Estoque Corporativo - CD Pereiro - CE 1": "Pereiro Corporativo 1",
    "Estoque Corporativo - CD Pereiro - CE 2": "Pereiro Corporativo 2",
    "CD Pereiro/Lagoa Nova - CE": "Lagoa nova 1",
    "CD Pereiro/Lagoa Nova - CE 2": "Lagoa nova 2",
    "CD Lagoa Nova / Segurança Patrimonial": "Lagoa Nova Segurança patrimonial 1",
    "CD Lagoa Nova / Segurança Patrimonial CD 2": "Lagoa Nova Segurança patrimonial 2",
    "CD Pereiro/Lagoa Nova - Torre CE": "Lagoa Nova Torre 1",
    "CD Pereiro/Lagoa Nova - Torre CE 2": "Lagoa Nova Torre 2",
    "Estoque Manutenção - CD Ceara/Pereiro": "Pereiro Manutenção 1",
    "Estoque Manutenção - CD Ceara/Pereiro 2": "Pereiro Manutenção 2",
    "CD Ceará/Pereiro": "Pereiro 1",
    "CD Ceará/Pereiro 2": "Pereiro 2",
    "CD Ceara/Jaguaribe": "Jaguaribe 1",
    "CD Ceara/Jaguaribe 2": "Jaguaribe 2",
    "Centro de Distribuição - Estoque Manutenção - CD Lagoa Nova - CE": "Lagoa nova Manutenção 1",
    "Centro de Distribuição - Estoque Manutenção - CD Lagoa Nova - CE 2": "Lagoa nova Manutenção 2",
}

PATTERNS = [
    (r'(?i)corporativo.*pereiro.*\b1\b', "Pereiro Corporativo 1"),
    (r'(?i)corporativo.*pereiro.*\b2\b', "Pereiro Corporativo 2"),
    (r'(?i)manuten[çc][aã]o.*pereiro.*\b1\b', "Pereiro Manutenção 1"),
    (r'(?i)manuten[çc][aã]o.*pereiro.*\b2\b', "Pereiro Manutenção 2"),
    (r'(?i)lagoa\s*nova.*seguran', "Lagoa Nova Segurança patrimonial 1"),
    (r'(?i)lagoa\s*nova.*seguran.*\b2\b', "Lagoa Nova Segurança patrimonial 2"),
    (r'(?i)lagoa\s*nova.*torre.*\b1\b', "Lagoa Nova Torre 1"),
    (r'(?i)lagoa\s*nova.*torre.*\b2\b', "Lagoa Nova Torre 2"),
    (r'(?i)lagoa\s*nova.*\b1\b', "Lagoa nova 1"),
    (r'(?i)lagoa\s*nova.*\b2\b', "Lagoa nova 2"),
    (r'(?i)jaguaribe.*\b1\b', "Jaguaribe 1"),
    (r'(?i)jaguaribe.*\b2\b', "Jaguaribe 2"),
    (r'(?i)pereiro.*\b1\b', "Pereiro 1"),
    (r'(?i)pereiro.*\b2\b', "Pereiro 2"),
]

def normalizar_deposito(nome: str) -> str | None:
    if not nome or str(nome).strip() == "":
        return None
    nome = str(nome).strip()
    if nome in DIRECT_MAP:
        return DIRECT_MAP[nome]
    for patt, destino in PATTERNS:
        if re.search(patt, nome):
            return destino
    return nome
