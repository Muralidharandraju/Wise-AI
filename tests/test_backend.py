import sys
import os
import pytest

# Add the backend directory to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

def test_backend_example():
    # Example backend test case
    assert True

import importlib.util
import sys
import os
import pytest

# Dynamically import the services module from backend directory
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend/services.py'))
spec = importlib.util.spec_from_file_location("services", backend_path)
services = importlib.util.module_from_spec(spec)
sys.modules["services"] = services
spec.loader.exec_module(services)

import pytest
import asyncio
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_get_text_from_pdfs():
    with patch('services.get_text_from_pdfs', new_callable=AsyncMock) as mock_get_text:
        # Setup mock return value
        mock_get_text.return_value = "Mocked PDF text content"

        # Call the function (which is mocked)
        result = await services.get_text_from_pdfs([b'some pdf bytes'])

        # Assert the mock was called
        mock_get_text.assert_called_once()

        # Assert the result is the mocked return value
        assert result == "Mocked PDF text content"

@pytest.mark.asyncio
async def test_get_text_from_pdfs_real():
    # Test with a sample PDF byte content
    sample_pdf_bytes = [b'%PDF-1.4\n%...\n%%EOF']  # Replace with actual PDF byte content for a real test
    text = await services.get_text_from_pdfs(sample_pdf_bytes)
    assert isinstance(text, str)
    assert len(text) > 0  # Assuming the sample PDF has some text content
    # Test with empty list
    text = await services.get_text_from_pdfs([])
    assert text == ""
    # Test with non-PDF content
    with pytest.raises(Exception): # Adjust exception type as per your implementation
        await services.get_text_from_pdfs([b'Not a PDF'])
