import httpx
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

async def get_latest_naira_fx_rate() -> float:
    """
    Fetches the latest official Naira/USD FX rate.
    Uses a standard public API or mocks the CBN endpoint because explicit API keys are not available.
    """
    try:
        # We simulate a call to a financial API, here mocking 1500 NGN per USD
        # In production this would be: response = await client.get("https://...cbn.gov.ng/api/...")
        mock_rate = 1500.00
        return mock_rate
    except Exception as e:
        logger.error(f"Error fetching FX rate: {e}")
        return 1500.00 # Fallback 
