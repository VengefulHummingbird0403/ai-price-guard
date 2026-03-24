import httpx
import os
import logging

logger = logging.getLogger(__name__)

WHATSAPP_TOKEN = os.getenv("WHATSAPP_API_TOKEN", "mock_token")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_ID", "mock_phone_id")
META_GRAPH_URL = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

async def send_whatsapp_alert(to_number: str, message_body: str) -> bool:
    """
    Sends a WhatsApp message using the Official Meta Business API.
    """
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {
            "body": message_body
        }
    }
    
    try:
        # Mocking for local tests without actual tokens
        if WHATSAPP_TOKEN == "mock_token":
            print(f"✅ [MOCK WHATSAPP] To: {to_number} | Message:\n{message_body}\n")
            return True
            
        async with httpx.AsyncClient() as client:
            response = await client.post(META_GRAPH_URL, json=payload, headers=headers)
            response.raise_for_status()
            print(f"WhatsApp message sent successfully to {to_number}")
            return True
    except Exception as e:
        logger.error(f"Failed to send WhatsApp message: {e}")
        return False
