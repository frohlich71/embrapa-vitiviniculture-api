from app.services.embrapa.production_ingestor import ProductionIngestor


def test_fetch_csv():
    df = ProductionIngestor().fetch_csv()
    assert not df.empty
    assert "produto" in df.columns


def test_reshape():
    ingestor = ProductionIngestor()
    df = ingestor.fetch_csv()
    melted = ingestor.reshape(df)
    assert "ano" in melted.columns
    assert "quantidade_litros" in melted.columns
