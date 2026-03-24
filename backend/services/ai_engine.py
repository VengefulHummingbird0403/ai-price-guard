import anthropic
import os
import logging
import json
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# Initialize Anthropic client
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY", "mock_key_for_testing")
)

async def generate_price_recommendation(
    product_name: str,
    wholesale_cost: float,
    current_retail_price: float,
    desired_margin: float,
    naira_drop_pct: float,
    competitor_price_increase_pct: float,
    competitor_avg_price: float
):
    """
    Calls Anthropic Claude to reason about the new price and identify anomalies.
    Returns a dict with 'recommended_price' and 'anomaly_detected'.
    """
    prompt = f"""
    You are an AI-driven price guard for small businesses in Nigeria.
    The user is selling '{product_name}'.
    Wholesale Cost: {wholesale_cost} NGN
    Current Retail Price: {current_retail_price} NGN
    Desired Profit Margin: {desired_margin}%
    
    Current Market Dynamics:
    - There is a {naira_drop_pct}% drop in the Naira (meaning imports are more expensive).
    - Competitor average price is now {competitor_avg_price} NGN, representing a {competitor_price_increase_pct}% increase.
    
    Task 1: Calculate and recommend a new retail price for the vendor to maintain their desired {desired_margin}% margin while adapting to the competitor's increase.
    Task 2: Detect anomalies. If the competitor's spike is unexpected or severe (e.g., > 10% suddenly), flag anomaly_detected as true and provide a preemptive warning message.
    
    Respond STRICTLY in JSON format with the following keys:
    - "recommended_price": float
    - "anomaly_detected": boolean
    - "warning_message": string (or null if no anomaly)
    - "reasoning": string (brief explanation of the math/strategy)
    """
    
    try:
        # If testing without an API key, return a mocked response.
        if os.environ.get("ANTHROPIC_API_KEY", "mock") == "mock" or os.environ.get("ANTHROPIC_API_KEY") == "mock_key_for_testing":
            rec_price = wholesale_cost * (1 + (desired_margin / 100))
            is_anomaly = competitor_price_increase_pct > 10
            return {
                "recommended_price": rec_price,
                "anomaly_detected": is_anomaly,
                "warning_message": "Preemptive Warning: Wholesaler prices for this product spiked unexpectedly." if is_anomaly else None,
                "reasoning": f"Calculated based on a desired {desired_margin}% margin over wholesale."
            }
            
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            temperature=0.2,
            system="You are an AI json generator.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.content[0].text
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        
        return json.loads(response_text)
    except Exception as e:
        logger.error(f"AI Engine Error: {e}")
        return {
            "recommended_price": current_retail_price,
            "anomaly_detected": False,
            "warning_message": str(e),
            "reasoning": "Error evaluating data."
        }
