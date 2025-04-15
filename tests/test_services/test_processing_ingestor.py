from app.services.embrapa.processing_ingestor import ProcessingIngestor

paths = ["download/ProcessaViniferas.csv", "download/ProcessaAmericanas.csv", "download/ProcessaMesa.csv", "download/ProcessaSemclass.csv"]


def test_fetch_csv():

    for path in paths:
        separator =  ";" if path == "download/ProcessaViniferas.csv" else "\t"

        df = ProcessingIngestor().fetch_csv(path, separator)
        assert not df.empty
        assert "cultura" in df.columns

def test_reshape():
    ingestor = ProcessingIngestor()

    for path in paths:
        separator =  ";" if path == "download/ProcessaViniferas.csv" else "\t"

        df = ingestor.fetch_csv(path, separator)
        melted = ingestor.reshape(df)
        assert "ano" in melted.columns
        assert "quantidade_kg" in melted.columns