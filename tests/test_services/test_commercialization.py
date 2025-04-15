from app.services.embrapa.commercialization_ingestor import CommercializationIngestor


def test_fetch_csv():
    df = CommercializationIngestor().fetch_csv()
    assert not df.empty
    assert "produto" in df.columns


def test_reshape():
    ingestor = CommercializationIngestor()
    df = ingestor.fetch_csv()
    melted = ingestor.reshape(df)
    assert "ano" in melted.columns
    assert "quantidade_litros" in melted.columns
