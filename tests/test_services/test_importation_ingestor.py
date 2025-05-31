from app.importation.ingestor import ImportationIngestor

paths = [
    "download/ImpVinhos.csv",
    "download/ImpEspumantes.csv",
    "download/ImpFrescas.csv",
    "download/ImpPassas.csv",
    "download/ImpSuco.csv",
]


def test_fetch_csv():

    for path in paths:
        separator = ";" if path == "download/ImpSuco.csv" else "\t"

        df = ImportationIngestor().fetch_csv(path, separator)
        assert not df.empty
        assert "cultura" in df.columns


def test_reshape():
    ingestor = ImportationIngestor()

    for path in paths:
        separator = ";" if path == "download/ImpSuco.csv" else "\t"

        df = ingestor.fetch_csv(path, separator)
        melted = ingestor.reshape(df)
        assert "ano" in melted.columns
        assert "quantidade_kg" in melted.columns
