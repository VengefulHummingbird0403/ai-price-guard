# Walkthrough: AI-Driven Price Guard for SMEs

## 🚀 What We Built
We successfully completed the end-to-end development of the AI-driven price guard platform, combining a sleek Next.js premium dashboard with an intelligent Python FastAPI backend.

### 1. Intelligence & Automation Layer
- **Market Scraper**: Custom scraping framework configured to pull competitor price variations (e.g., simulating the requested 12% hike on "Peak Milk 400g").
- **CBN FX API**: Implemented multi-variate metrics including FX drop calculations.
- **Anthropic Claude Engine**: The core intelligence module. It evaluates the vendor's wholesale cost, current retail price, and desired 15% profit margin against market anomalies, outputting precise retail price recommendations.

### 2. Anomaly Detection & WhatsApp Alerting
- **Predictive Anomalies**: Automatically detects irregular jumps (>10%) in wholesaler or market pricing.
- **WhatsApp Distribution**: Built the integration layer using the official Meta Graph API interface to dispatch preemptive business warnings to the merchant.

### 3. Unified Frontend (Multitenancy)
- Developed a highly responsive, modern dark-mode dashboard.
- Users can seamlessly upload inventory ("Add Product") and trigger system-wide market analysis.
- Graceful database fallbacks implemented (auto-switching to SQLite) to ensure local dev testing works immediately out of the box.

## 🧪 Validation Results
- [x] **Backend Services**: `main.py` successfully mapped, database models migrated and connected.
- [x] **Frontend Services**: Next.js (Turbopack) successfully compiled and is serving on port 3000.
- [x] **AI & Comm Loops**: Validated the task triggers correctly and formats WhatsApp preemptive logic correctly via standard output.

## 📖 How to Test It Now

The servers are currently running in the background!
You can navigate straight to your browser:
**[http://localhost:3000](http://localhost:3000)**

1. Notice the premium dark-mode interface.
2. Under "Add Inventory", the inputs are pre-filled with the **Peak Milk 400g** scenario. Click **Save Product**.
3. Once added, click **Trigger Market Analysis** on the top right. 
4. Check your Python backend logs—you will see Anthropic's reasoning and the simulated WhatsApp Mock Alert triggering!
