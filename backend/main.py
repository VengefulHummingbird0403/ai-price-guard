from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import models, schemas, database
from database import engine

# Automatically create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Price Guard API", version="1.0.0")

# Setup CORS to allow Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Price Guard API"}

@app.post("/api/tenants/", response_model=schemas.Tenant)
def create_tenant(tenant: schemas.TenantCreate, db: Session = Depends(get_db)):
    db_tenant = models.Tenant(**tenant.model_dump())
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant

@app.get("/api/tenants/{tenant_id}", response_model=schemas.Tenant)
def read_tenant(tenant_id: int, db: Session = Depends(get_db)):
    db_tenant = db.query(models.Tenant).filter(models.Tenant.id == tenant_id).first()
    if db_tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return db_tenant

@app.post("/api/inventory/{tenant_id}", response_model=schemas.InventoryItem)
def create_inventory_item(tenant_id: int, item: schemas.InventoryItemCreate, db: Session = Depends(get_db)):
    db_item = models.InventoryItem(**item.model_dump(), tenant_id=tenant_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/api/inventory/{tenant_id}", response_model=list[schemas.InventoryItem])
def get_inventory(tenant_id: int, db: Session = Depends(get_db)):
    return db.query(models.InventoryItem).filter(models.InventoryItem.tenant_id == tenant_id).all()

@app.post("/api/analysis/run/{tenant_id}")
async def trigger_analysis(tenant_id: int, db: Session = Depends(get_db)):
    from scheduler import run_market_analysis
    await run_market_analysis(db, tenant_id)
    return {"status": "Analysis completed. Check WhatsApp alerts if anomalies detected."}
