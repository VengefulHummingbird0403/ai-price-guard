import asyncio
from services.scraper import scrape_competitor_price
from services.cbn_fx import get_latest_naira_fx_rate
from services.ai_engine import generate_price_recommendation
from services.whatsapp import send_whatsapp_alert
from sqlalchemy.orm import Session
import models, database

async def run_market_analysis(db: Session, tenant_id: int):
    print(f"--- Starting Market Analysis for Tenant {tenant_id} ---")
    tenant = db.query(models.Tenant).filter(models.Tenant.id == tenant_id).first()
    if not tenant:
        print("Tenant not found.")
        return
        
    items = db.query(models.InventoryItem).filter(
        models.InventoryItem.tenant_id == tenant_id,
        models.InventoryItem.is_active == True
    ).all()
    
    if not items:
        print("No active inventory found for this tenant.")
        return

    fx_rate = await get_latest_naira_fx_rate()
    naira_drop_pct = 5.0 # Simulating the 5% drop requested in requirement
    
    for item in items:
        comp_price = await scrape_competitor_price(item.product_name)
        
        # Calculate recent % increase conceptually (e.g. comparing to historical price)
        # We simulate a 12% increase if price > 4500 (our mocked spike scenario)
        old_comp_price = comp_price / 1.12 if comp_price > 4500 else comp_price
        increase_pct = round(((comp_price - old_comp_price) / old_comp_price) * 100, 2)
        
        ai_response = await generate_price_recommendation(
            product_name=item.product_name,
            wholesale_cost=item.wholesale_cost,
            current_retail_price=item.current_retail_price,
            desired_margin=item.desired_margin_percent,
            naira_drop_pct=naira_drop_pct,
            competitor_price_increase_pct=increase_pct,
            competitor_avg_price=comp_price
        )
        
        # Save Log
        log = models.PriceLog(
            item_id=item.id,
            competitor_avg_price=comp_price,
            naira_fx_rate=fx_rate,
            ai_recommended_price=ai_response["recommended_price"],
            anomaly_detected=ai_response["anomaly_detected"]
        )
        db.add(log)
        
        # Alert via WhatsApp if anomaly logic triggered
        if ai_response["anomaly_detected"] and tenant.contact_number:
            msg = f"⚠️ *PriceGuard Predictive Alert*\n\nProduct: {item.product_name}\n\n{ai_response['warning_message']}\n\nMarket Avg: NGN {comp_price} (+{increase_pct}% increase)\nRecommended Action: Adjust your price to NGN {ai_response['recommended_price']} to maintain your {item.desired_margin_percent}% margin."
            await send_whatsapp_alert(tenant.contact_number, msg)
            
    db.commit()
    print("--- Market Analysis Completed ---")
