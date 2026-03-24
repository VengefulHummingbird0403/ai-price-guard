from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact_number = Column(String)  # WhatsApp number
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    inventory = relationship("InventoryItem", back_populates="tenant")

class InventoryItem(Base):
    __tablename__ = "inventory_items"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    product_name = Column(String, index=True)
    wholesale_cost = Column(Float)
    desired_margin_percent = Column(Float)
    current_retail_price = Column(Float)
    is_active = Column(Boolean, default=True)
    
    tenant = relationship("Tenant", back_populates="inventory")
    logs = relationship("PriceLog", back_populates="item")

class PriceLog(Base):
    __tablename__ = "price_logs"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("inventory_items.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    competitor_avg_price = Column(Float)
    naira_fx_rate = Column(Float)
    ai_recommended_price = Column(Float)
    anomaly_detected = Column(Boolean, default=False)
    
    item = relationship("InventoryItem", back_populates="logs")
