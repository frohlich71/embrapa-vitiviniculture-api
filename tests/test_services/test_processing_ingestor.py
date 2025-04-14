import pandas as pd
import pytest
from unittest.mock import Mock, patch
from sqlmodel import Session

from app.models.processing import ProcessingCreate
from app.services.embrapa.processing_ingestor import ProcessingIngestor


@pytest.fixture
def sample_df():
    """Create a sample DataFrame that mimics the CSV structure"""
    data = {
        "cultivar": ["Cultivar 1", "Cultivar 2"],
        "2020": ["1000,0", "2000,0"],
        "2021": ["1500,0", "2500,0"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def ingestor():
    return ProcessingIngestor()


def test_reshape(ingestor, sample_df):
    """Test the reshape method that converts wide format to long format"""
    result = ingestor.reshape(sample_df)
    
    # Check the shape is correct (4 rows: 2 cultivars * 2 years)
    assert result.shape == (4, 3)
    
    # Check column names
    assert set(result.columns) == {"cultivar", "ano", "quantidade_kg"}
    
    # Check values are correctly transformed
    assert "2020" in result["ano"].values
    assert "2021" in result["ano"].values


@patch("app.services.embrapa.base_ingestor.httpx.get")
def test_fetch_csv(mock_get, ingestor):
    """Test CSV fetching with mocked HTTP response"""
    # Mock response
    mock_response = Mock()
    mock_response.text = "cultivar;2020;2021\nCultivar 1;1000,0;1500,0\nCultivar 2;2000,0;2500,0"
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    
    df = ingestor.fetch_csv()
    
    # Verify HTTP call was made with correct URL
    mock_get.assert_called_once_with(f"{ingestor.BASE_URL}/{ingestor.CSV_PATH}")
    
    # Check DataFrame structure
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 3)


def test_ingest(ingestor, sample_df):
    """Test the ingestion process"""
    # Mock session and database operations
    session = Mock(spec=Session)
    
    # Mock get_by_year_and_cultivate to simulate both new and existing records
    with patch("app.services.embrapa.processing_ingestor.get_by_year_and_cultivate") as mock_get:
        with patch("app.services.embrapa.processing_ingestor.create_processing") as mock_create:
            # Simulate one existing record and one new record
            mock_get.side_effect = [None, True, None, True]  # Alternating new/existing
            
            # Mock fetch_csv to return our sample data
            with patch.object(ingestor, "fetch_csv", return_value=sample_df):
                ingestor.ingest(session)
                
                # Verify create_processing was called for new records
                assert mock_create.call_count == 2
                
                # Verify the data passed to create_processing
                calls = mock_create.call_args_list
                for call in calls:
                    args = call[0]
                    assert isinstance(args[1], ProcessingCreate)
                    assert isinstance(args[1].quantity_kg, float)
                    assert isinstance(args[1].year, int)
                    assert isinstance(args[1].cultivate, str)


def test_ingest_error_handling(ingestor):
    """Test error handling during ingestion"""
    session = Mock(spec=Session)
    
    # Create a DataFrame with invalid data
    bad_data = {
        "cultivar": ["Cultivar 1"],
        "2020": ["invalid"],  # This will cause a ValueError during conversion
    }
    bad_df = pd.DataFrame(bad_data)
    
    with patch.object(ingestor, "fetch_csv", return_value=bad_df):
        # Should not raise an exception
        ingestor.ingest(session)
