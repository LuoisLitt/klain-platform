# GripAI Weekrapportage — Technische Architectuur

## Flow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        ELKE VRIJDAG 17:00                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  1. TRIGGER (Cron Job)                                          │
│     Railway Cron of Trigger.dev                                 │
│     Start weekrapportage voor alle actieve klanten              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. DATA OPHALEN                                                │
│     Per klant: connectie met hun boekhoudsysteem                │
│                                                                 │
│     Supported:                                                  │
│     • Exact Online  → OAuth2 API                                │
│     • Snelstart     → API                                       │
│     • Moneybird     → API (makkelijkste!)                       │
│     • e-Boekhouden  → API                                       │
│     • Excel upload  → Fallback voor kleine klanten              │
│                                                                 │
│     Data: omzet, kosten, facturen, betalingen, openstaand       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. OPSLAG & HISTORIE                                           │
│     Supabase (PostgreSQL)                                       │
│                                                                 │
│     Tables:                                                     │
│     • customers        → klantgegevens, API keys                │
│     • weekly_snapshots → ruwe data per week                     │
│     • reports          → gegenereerde rapporten                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. AI ANALYSE                                                  │
│     OpenAI GPT-4o-mini (goedkoop, snel)                         │
│                                                                 │
│     Input:                                                      │
│     • Deze week vs vorige week                                  │
│     • Deze week vs zelfde week vorig jaar                       │
│     • Trends laatste 4 weken                                    │
│     • Openstaande debiteuren                                    │
│                                                                 │
│     Output:                                                     │
│     • 3-5 key insights                                          │
│     • Vergelijking met vorige periode                           │
│     • Concrete aanbevelingen                                    │
│     • Risk alerts (indien nodig)                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  5. RAPPORT GENEREREN                                           │
│     React Email of MJML templates                               │
│                                                                 │
│     Formaat:                                                    │
│     • HTML email (mobile-friendly)                              │
│     • PDF bijlage (optioneel, voor archief)                     │
│                                                                 │
│     Branding: GripAI huisstijl, klantlogo                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  6. VERZENDEN                                                   │
│     Resend (transactional email)                                │
│                                                                 │
│     • Naar klant + CC naar jou                                  │
│     • Open/click tracking                                       │
│     • Retry bij falen                                           │
└─────────────────────────────────────────────────────────────────┘


## Tech Stack

| Component       | Keuze              | Waarom                          | Kosten        |
|-----------------|--------------------|---------------------------------|---------------|
| **Runtime**     | Railway            | Simple, goede DX, gratis start  | $0-5/maand    |
| **Taal**        | Python             | Beste voor data/AI              | -             |
| **Database**    | Supabase           | Postgres + auth + gratis tier   | $0            |
| **AI**          | OpenAI gpt-4o-mini | Goedkoop, snel, goed genoeg     | ~€0.30/rapport|
| **Email**       | Resend             | Modern, goede API, gratis tier  | $0            |
| **Cron**        | Railway Cron       | Ingebouwd, geen extra service   | $0            |
| **Secrets**     | Railway env vars   | Veilig, encrypted               | $0            |

**Totaal bij 1 klant: < €5/maand**
**Totaal bij 10 klanten: ~€10-15/maand**


## Database Schema (Supabase)

```sql
-- Klanten
CREATE TABLE customers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  company_name TEXT NOT NULL,
  accounting_system TEXT, -- 'moneybird', 'exact', 'snelstart', etc.
  accounting_credentials JSONB, -- encrypted API keys
  report_day INTEGER DEFAULT 5, -- 1=ma, 5=vr
  report_time TIME DEFAULT '17:00',
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Wekelijkse snapshots (ruwe data)
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
  raw_data JSONB, -- volledige API response
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Gegenereerde rapporten
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
```


## Project Structuur

```
gripai-reports/
├── src/
│   ├── main.py              # Entry point, cron handler
│   ├── connectors/          # Boekhouding integraties
│   │   ├── moneybird.py
│   │   ├── exact.py
│   │   └── excel.py
│   ├── analysis/
│   │   └── weekly_report.py # AI analyse logica
│   ├── templates/
│   │   └── report.html      # Email template
│   └── services/
│       ├── database.py      # Supabase client
│       └── email.py         # Resend client
├── requirements.txt
├── railway.toml             # Deploy config
└── .env.example
```


## Eerste Klant Onboarding Flow

1. **Intake gesprek**
   - Welk boekhoudsysteem?
   - Wie ontvangt het rapport?
   - Welke dag/tijd?

2. **Technische setup** (jij, eenmalig 30 min)
   - API koppeling maken
   - Klant in database
   - Test rapport draaien

3. **Go-live**
   - Eerste echte rapport vrijdag
   - Feedback verzamelen
   - Eventueel template aanpassen


## Uitbreidingen (later)

- [ ] Dashboard voor klant (Supabase + Next.js)
- [ ] WhatsApp/Telegram delivery optie
- [ ] Automatische alerts bij afwijkingen
- [ ] Vergelijking met branchegemiddelden
- [ ] Multi-user per bedrijf


## Kosten Eerste Jaar (1-5 klanten)

| Item                  | Per maand |
|-----------------------|-----------|
| Railway               | €0-5      |
| Supabase              | €0        |
| Resend                | €0        |
| OpenAI API            | €5-15     |
| Domein (gripai.nl)    | €1        |
| **Totaal**            | **€6-21** |

Bij €99/klant marge: **€78-93 per klant per maand**
