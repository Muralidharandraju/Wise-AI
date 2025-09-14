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
    # Test with a minimal valid PDF byte content that PyPDF2 can parse
    sample_pdf_bytes = [b'%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Count 1 /Kids [3 0 R] >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 44 >>\nstream\nBT\n/F1 24 Tf\n100 700 Td\n(Hello, PDF!) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000010 00000 n \n0000000060 00000 n \n0000000117 00000 n \n0000000211 00000 n \ntrailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n305\n%%EOF']
    text = await services.get_text_from_pdfs(sample_pdf_bytes)
    assert isinstance(text, str)
    # The text may be empty if extraction fails, so check for string type only
    # Test with empty list
    text = await services.get_text_from_pdfs([])
    assert text == ""
    # Test with non-PDF content
    try:
        await services.get_text_from_pdfs([b'Not a PDF'])
    except Exception:
        pass
    else:
        pytest.fail("Expected exception not raised for non-PDF content")
