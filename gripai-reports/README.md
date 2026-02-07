# GripAI Weekrapportage

Automatische wekelijkse financiële rapportages voor MKB-bedrijven.

## Quick Start

```bash
# 1. Clone en install
cd gripai-reports
pip install -r requirements.txt

# 2. Kopieer en vul environment variables
cp .env.example .env
# Edit .env met je API keys

# 3. Test met demo data
python src/main.py --test
```

## Setup

### Benodigde accounts (allemaal gratis tier)

1. **Anthropic** (Claude API)
   - https://console.anthropic.com
   - Maak API key aan

2. **Supabase** (Database)
   - https://supabase.com
   - Nieuw project aanmaken
   - SQL schema uitvoeren (zie onder)

3. **Resend** (Email)
   - https://resend.com
   - API key + domein verifiëren

### Database Schema

Voer dit uit in Supabase SQL Editor:

```sql
-- Klanten
CREATE TABLE customers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  company_name TEXT NOT NULL,
  accounting_system TEXT,
  accounting_credentials JSONB,
  report_day INTEGER DEFAULT 5,
  report_time TIME DEFAULT '17:00',
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Wekelijkse snapshots
CREATE TABLE weekly_snapshots (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id UUID REFERENCES customers(id),
  week_start DATE NOT NULL,
  week_end DATE NOT NULL,
  revenue DECIMAL(12,2),
  costs DECIMAL(12,2),
  invoices_sent INTEGER,
  invoices_paid INTEGER,
  outstanding_amount DECIMAL(12,2),
  raw_data JSONB,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Rapporten
CREATE TABLE reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id UUID REFERENCES customers(id),
  snapshot_id UUID REFERENCES weekly_snapshots(id),
  ai_analysis TEXT,
  html_content TEXT,
  pdf_url TEXT,
  sent_at TIMESTAMPTZ,
  opened_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Indexes
CREATE INDEX idx_snapshots_customer ON weekly_snapshots(customer_id);
CREATE INDEX idx_snapshots_week ON weekly_snapshots(week_end DESC);
CREATE INDEX idx_reports_customer ON reports(customer_id);
```

## Deployment (Railway)

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login en link
railway login
railway init

# 3. Set environment variables
railway variables set ANTHROPIC_API_KEY=sk-ant-...
railway variables set SUPABASE_URL=https://xxx.supabase.co
railway variables set SUPABASE_KEY=eyJ...
railway variables set RESEND_API_KEY=re_...
railway variables set FROM_EMAIL=rapport@gripai.nl

# 4. Deploy
railway up
```

De cron job draait automatisch elke vrijdag 17:00 CET.

## Nieuwe klant toevoegen

```python
from src.services.database import Database

db = Database()
await db.create_customer(
    name="Jan de Vries",
    email="jan@keukenleverancier.nl",
    company_name="Keukenleverancier Drenthe B.V.",
    accounting_system="moneybird",
    accounting_credentials={
        "admin_id": "123456789",
        "token": "xxx"
    }
)
```

## Supported Boekhoudpakketten

- [x] Moneybird
- [ ] Exact Online (planned)
- [ ] Snelstart (planned)
- [ ] e-Boekhouden (planned)
- [x] Excel upload (fallback)

## Kosten

| Service | Gratis tier | Daarna |
|---------|-------------|--------|
| Railway | $5/maand credit | $0.01/GB-hr |
| Supabase | 500MB database | $25/maand |
| Resend | 3000 emails/maand | $20/maand |
| Claude API | - | ~€0.50/rapport |

**Eerste 5 klanten: < €10/maand**

## License

Proprietary - GripAI
