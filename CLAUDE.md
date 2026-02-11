# CLAUDE.md - Klain Platform Team Rules

## Project Overview
- **Repo**: klain-platform (monorepo)
- **Live site**: klain.nl (hosted on Vercel, static site)
- **Structure**: `gripai-website/` is the main served directory (via vercel.json)
- **Tech**: Pure HTML/CSS/JS (no framework), DM Sans + Fraunces fonts, CSS custom properties
- **Deployment**: Vercel static hosting, routes everything through `gripai-website/`

## File Structure
```
gripai-website/
  index.html          - Main landing page (klain.nl)
  styles.css          - Shared styles for demo pages
  demo.html           - Weekrapport demo
  demo-offerte.html   - Offerte keuken demo
  demo-offerte-bouw.html - Offerte bouw demo
  demo-cashflow.html  - Cashflow demo
  demo-debiteuren.html - Debiteuren demo
  dura/               - Dura Fulfilment portal
  demos/              - Client-specific demos
  images/             - Images directory
```

## Design System
- Colors: --blue (#2563eb), --black (#0f1117), --gray-* scale, --green, --orange
- Fonts: Fraunces (serif, headings), DM Sans (body)
- Border radius: --radius (16px), --radius-sm (10px), --radius-lg (24px)
- Animations: fade-up with IntersectionObserver, hover transforms

## Team Rules (STRICT)

### 1. Plan Approval Required
- **frontend_dev** and **backend_dev** MUST submit plans before writing ANY code
- Plans go through the team lead for approval
- No code changes without an approved plan

### 2. The Skeptic (Read-Only)
- **the_skeptic** can NOT write or edit any code files
- Role is limited to: reviewing plans, reviewing docs, security analysis, UX review
- Plays devil's advocate on all plans before approval

### 3. Decision Log
- ALL teammates must update this CLAUDE.md with their decisions
- Add decisions under the "Decision Log" section below
- Format: `- [DATE] [AGENT] Decision: <description>`

### 4. Current Conventions (DO NOT BREAK)
- Maintain current HTML/CSS/JS structure (no frameworks)
- Keep the design system consistent (colors, fonts, spacing)
- All text in Dutch (NL)
- Mobile-responsive design required
- Keep styles inline in index.html (it has its own styles)
- Demo pages use shared styles.css
- **SECURITY**: Endpoints under `/api/auth/` bypass the verify_auth middleware. Do NOT add non-auth endpoints under this prefix without adding explicit auth checks.

## Backlog Items
- Ernst's foto toevoegen aan About sectie
- Logo's aanpassen
- Security setup (2FA, API keys, RLS)
- Backend: FastAPI endpoints, Dura frontend-backend connection

---

## Decision Log
<!-- Teammates: add your decisions here -->

- [2026-02-11] [backend_dev] Decision: Removed /api/ai-insights/debug endpoint that exposed API key prefixes publicly. Pushed to main for immediate Railway deploy.
- [2026-02-11] [backend_dev] Decision: Tightened CORS to only allow klain.nl origins (with CORS_ORIGINS env var for dev override). Restricted methods to GET/OPTIONS, headers to Content-Type/Accept.
- [2026-02-11] [backend_dev] Decision: Sanitized all error responses - replaced detail=str(e) with generic "Internal server error" across all 13 endpoints. Added print logging for server-side debugging.
- [2026-02-11] [backend_dev] Decision: Added .gitignore to dura-backend, removed tracked __pycache__/*.pyc files.
- [2026-02-11] [backend_dev] Decision: Added security headers to vercel.json (X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, Referrer-Policy).
- [2026-02-11] [backend_dev] Decision: Reduced AI insights polling from 15s to 300s (5 min) in ai-insights.js to reduce unnecessary API load.
- [2026-02-11] [frontend_dev] Decision: Removed hardcoded employee passwords (Michel, Jarne) from demo-dura-login.html. Only demo account remains.
- [2026-02-11] [frontend_dev] Decision: Fixed innerHTML XSS in dura/ai-insights.js — changed to textContent and DOM createElement for API data rendering.
- [2026-02-11] [frontend_dev] Decision: Replaced all GripAI branding with klain in demos/borghuis-keukens/ (dashboard.html + login.html). Updated URLs from gripai-website.vercel.app to klain.nl.
- [2026-02-11] [frontend_dev] Decision: Self-hosted Google Fonts (DM Sans + Fraunces) in gripai-website/fonts/ to comply with GDPR. Removed external Google Fonts links from index.html.
- [2026-02-11] [frontend_dev] Decision: Added KvK/BTW placeholders to footer. Created privacy.html with Dutch privacy policy. Updated footer Privacy link.
- [2026-02-11] [frontend_dev] Decision: Added OG meta tags, canonical URL, skip-to-content link, mobile menu improvements (aria-expanded, close-on-outside-click, CTA button), FAQ aria attributes, footer fixes (logo color, debiteurenbeheer link, phone), CTA phone number, about stats.
- [2026-02-11] [backend_dev] Decision: Added X-API-Key middleware to dura-backend for all /api/* endpoints. Uses DURA_API_KEY env var (Railway), hmac.compare_digest for timing-safe comparison. Fail-closed if env var not set. Committed but NOT pushed - requires coordinated deploy with frontend updates.
- [2026-02-11] [ai-specialist] Decision: Analysed all 6 portal pages + backend + ai-insights.js/ai_updates.py. Current AI: Claude Haiku generates insights 3x/dag (08:30, 13:00, 17:30) via /api/ai-insights. Dashboard toont AI briefing hero block, andere pagina's tonen 1-regel page_insight. Voorstel: uitbreiden naar pagina-specifieke AI blokken met contextuele, actionable inzichten per pagina i.p.v. generieke 1-liners.
- [2026-02-11] [security-analist] Decision: Volledige security review uitgevoerd. Bevindingen: (1) KRITIEK: API key hardcoded in auth.js en ai-insights.js — zichtbaar voor elke browser gebruiker. (2) HOOG: XSS via innerHTML in index.html, orders.html, verzendingen.html, warehouse.html, voorraad.html — API data wordt ongeëscaped in innerHTML gezet. (3) HOOG: CORS laat POST toe naast GET/OPTIONS in backend — Decision Log zegt alleen GET/OPTIONS maar code toont allow_methods=["GET","POST","OPTIONS"]. (4) MIDDEL: Session token in sessionStorage — kwetsbaar voor XSS token theft. (5) MIDDEL: Geen rate limiting op login endpoint — brute force mogelijk. (6) MIDDEL: Geen CSRF-bescherming. (7) LAAG: Google Fonts nog extern geladen in dura/ subpagina's (GDPR). (8) LAAG: Geen Content-Security-Policy header. (9) INFO: SESSION_SECRET fallback naar lege string — goed dat login weigert als niet gezet.
- [2026-02-11] [business-analist] Decision: Volledige analyse van alle 6 portal pagina's, backend, auth, CSS en JS afgerond. Sector-onderzoek naar fulfilment KPI's en 3PL klantportaal best practices gedaan. Verbeterplan opgesteld in 3 prioriteiten (P1 Security, P2 UX/Functionaliteit, P3 AI) — zie hieronder.
- [2026-02-11] [business-analist] Decision: Frontend review van frontend-dev ontvangen en beoordeeld. Bevestigt: (1) Inter font imports in 5 dura/ pagina's zijn overbodig (styles.css definieert DM Sans), (2) 1500+ regels CSS duplicatie in index.html en warehouse.html, (3) JS duplicatie (STATUS_MAP 3x, extractCarrier 4x, formatDutchDate 3x), (4) Hamburger menu zonder JS handler. Besluit: CSS/JS refactoring geparkeerd als P2.5 — focus blijft P1 security fixes eerst.
- [2026-02-11] [backend_dev] Decision: P1.1 + P1.3 geimplementeerd. Vervangen verify_api_key middleware door verify_auth: accepteert nu session tokens (Bearer header) naast X-API-Key (backward compat). POST whitelist toegevoegd: alleen /api/auth/login en /api/ai-insights/refresh accepteren POST, rest krijgt 405. Auth method wordt gelogd voor debugging. Frontend hoeft nu alleen session token te sturen, geen API key meer.
- [2026-02-11] [business-analist] Decision: Backend-dev volledige review ontvangen (18 endpoints, 15 bevindingen). Nieuwe items geprioriteerd: (1) P1.5 rate limiting + AI refresh auth check + SESSION_SECRET check — direct na P1.2/P1.4, (2) P2: hardcoded users naar env/db, revenue berekening optimalisatie, lifespan migratie, cache lock cleanup, (3) P3: overige code quality items. Verbeterplan bijgewerkt.
- [2026-02-11] [business-analist] Decision: AI-specialist analyse ontvangen en verwerkt. P3 scope vastgesteld met Optie B aanpak (rijkere page_insights, meerdere bullet points per pagina). P3.1 Quick Wins: bottleneck detectie orders, voorraad burn-rate, carrier analyse, capaciteitsplanning warehouse. P3.2 Middellang: historische data opslag, anomalie-detectie, herbestelpunten. P3.3 Backlog: interactieve AI chat, seizoensvoorspellingen. Security review P1.1+P1.3 toegewezen aan security-analist (task #16).
- [2026-02-11] [backend_dev] Decision: P1.5 geimplementeerd — drie onderdelen: (1) Rate limiting op /api/auth/login: in-memory RateLimiter class, max 5 pogingen per 15 min per IP, 429 response bij overschrijding. (2) Session auth op /api/ai-insights/refresh: vereist geldig Bearer session token, logt wie refresh triggert. (3) SESSION_SECRET guard in create_session_token: raised ValueError als secret niet geconfigureerd, voorkomt tokens met lege HMAC key.
- [2026-02-11] [security-analist] Decision: Review P1.1+P1.3 backend implementatie. Backend GOEDGEKEURD: verify_auth middleware is fail-closed, timing-safe (hmac.compare_digest), accepteert Bearer tokens + API key backward compat. POST whitelist waterdicht (alleen /api/auth/login en /api/ai-insights/refresh). OPEN PUNT: API key staat nog hardcoded in frontend (auth.js regel 14, ai-insights.js regel 8) — frontend-dev moet key verwijderen. Na deploy: DURA_API_KEY op Railway roteren want oude key is publiek gelekt.
- [2026-02-11] [frontend_dev] Decision: P1.2 XSS fixes voltooid in alle 5 dura/ pagina's (orders.html, index.html, verzendingen.html, voorraad.html, warehouse.html). Alle innerHTML met API data vervangen door textContent + createElement. Helper functies toegevoegd per pagina (createProductRow, createAlertItem, renderOrderRow, etc.). Alleen statische innerHTML overgebleven (SVG icons, paginatie met numerieke waarden).
- [2026-02-11] [frontend_dev] Decision: P1.4 self-hosted fonts voltooid. Externe Google Fonts verwijderd uit alle 7 dura/ bestanden (6 HTML + styles.css). @font-face declaraties toegevoegd voor DM Sans + Fraunces met ../fonts/ pad. warehouse.html font-family gewijzigd van Inter naar DM Sans. Nul externe font-verzoeken, GDPR compliant.
- [2026-02-11] [frontend_dev] Decision: P1.1 frontend deel voltooid — API key verwijderd uit auth.js (var API_KEY + X-API-Key header) en ai-insights.js (fallback API key + hardcoded API_BASE). auth.js stuurt nu alleen Bearer session token. ai-insights.js vereist window.DURA_API_BASE/HEADERS (gezet door auth.js), doet early return als niet beschikbaar. Nul API key referenties in frontend code. BELANGRIJK: Na deploy moet DURA_API_KEY op Railway geroteerd worden (taak #19).
- [2026-02-11] [backend_dev] Decision: P2.1 SLA Metrics endpoint geimplementeerd. Nieuw GET /api/metrics/sla?period=today|week|month met 4 KPI's (On-Time Shipping, Order Accuracy, Cycle Time, Perfect Order Rate), trend indicators, today-vs-yesterday vergelijking. Cache TTL 300s.
- [2026-02-11] [backend_dev] Decision: P2.3 Report export endpoint geimplementeerd. Nieuw GET /api/reports/export?format=csv&period=week|month|custom met StreamingResponse CSV download. Bevat 4 secties: samenvatting (orders, omzet, SLA metrics), orders per dag, top webshops, carrier verdeling. Puntkomma-delimiter voor NL Excel compatibiliteit + UTF-8 BOM. Geen extra dependencies (csv is stdlib). Session auth via middleware + logging wie exporteert.
- [2026-02-11] [backend_dev] Decision: P2.6 Hardcoded users naar env vars. USERS dict vervangen door _load_users() functie die DURA_USERS env var (JSON) leest. Fallback naar alleen demo account als env var niet gezet. Michel en Jarne credentials verwijderd uit broncode. Ernst moet DURA_USERS env var instellen op Railway met JSON van alle 3 users.
- [2026-02-11] [security-analist] Decision: P1.2 XSS review GOEDGEKEURD voor productie. Alle 5 dura/ pagina's gecontroleerd: index.html, orders.html, verzendingen.html, voorraad.html, warehouse.html — geen innerHTML met API data meer. 1 minor restpunt: orders.html paginering gebruikt innerHTML met integer API waarden (laag risico). ai-insights.js en rapportages.html alleen statische innerHTML (veilig).
- [2026-02-11] [business-analist] Decision: P1 SPRINT VOLLEDIG AFGEROND. Alle P1 taken completed: P1.1 session auth, P1.2 XSS fixes, P1.3 CORS POST, P1.4 self-hosted fonts, P1.5 rate limiting, API key verwijderd uit frontend. Alle backend implementaties security-reviewed en goedgekeurd. ACTIE NODIG: DURA_API_KEY roteren op Railway (task #19) — oude key is publiek gelekt. P2 sprint loopt: P2.1 SLA Metrics done, P2.3 Report export in progress.
- [2026-02-11] [backend_dev] Decision: P2.1 SLA Metrics endpoint geimplementeerd. Nieuw GET /api/metrics/sla?period=today|week|month endpoint met 4 KPI's: On-Time Shipping % (orders binnen 24u SLA), Order Accuracy Rate (geen attentionNeeded), Order Cycle Time (avg/mediaan/P95), Perfect Order Rate (on-time + accuraat + afgerond). Inclusief trend indicators (vergelijking met vorige periode) en today-vs-yesterday vergelijking. Cache TTL 300s. Parallel data ophalen voor huidige en vorige periode.
- [2026-02-11] [security-analist] Decision: Review P1.5 rate limiting implementatie. GOEDGEKEURD: RateLimiter sliding window correct, check VOOR bcrypt, AI refresh vereist Bearer token, SESSION_SECRET guard fail-closed. Aandachtspunten (niet-blokkerend): succesvolle logins tellen mee bij rate limit, in-memory limiter reset bij restart, geen GC op _attempts dict.
- [2026-02-11] [security-analist] Decision: Review P1.2 XSS fixes alle 5 dura/ pagina's. GOEDGEKEURD voor productie. index.html, verzendingen.html, voorraad.html, warehouse.html: alle innerHTML met API data vervangen door textContent/createElement. orders.html: 1 minor restpunt — paginering (regels 521-531) gebruikt innerHTML met API-afgeleide integers (laag risico). ai-insights.js: innerHTML alleen voor statische UI, API tekst via textContent. Resterende innerHTML bevat uitsluitend statische SVG of numerieke waarden.
- [2026-02-11] [business-analist] Decision: Alle backend P1 taken afgerond (P1.1+P1.3+P1.5 COMPLETED). Backend-dev toegewezen aan P2.1 SLA Metrics endpoint (task #17). P2.3 Report export (task #18) als volgende. BELANGRIJK open punt van security-analist: API key op Railway moet geroteerd worden na frontend deploy — oude key is publiek gelekt.
- [2026-02-11] [security-analist] Decision: Review P1.5 rate limiting implementatie. GOEDGEKEURD: (1) RateLimiter sliding window correct, check VOOR bcrypt (voorkomt CPU-burn). (2) AI refresh vereist Bearer session token + logt wie triggert. (3) SESSION_SECRET guard fail-closed. Aandachtspunten (niet-blokkerend): succesvolle logins tellen mee bij rate limit (kan legitieme gebruikers blokkeren), in-memory limiter reset bij Railway restart, geen garbage collection op _attempts dict.
- [2026-02-11] [security-analist] Decision: Review Task #21 — API key verwijdering uit frontend. GOEDGEKEURD. auth.js: API_KEY variabele en X-API-Key header volledig verwijderd, stuurt nu alleen Bearer session token. ai-insights.js: hardcoded API_BASE en fallback API key verwijderd, gebruikt nu window.DURA_API_BASE/HEADERS globals (gezet door auth.js), early return guard als auth niet geladen. Grep over gehele gripai-website/ directory bevestigt: NUL API key referenties meer in frontend code. HERINNERING: Task #19 (DURA_API_KEY roteren op Railway) blijft KRITIEK — de oude key is publiek gelekt en moet onmiddellijk geroteerd worden na deploy.
- [2026-02-11] [business-analist] Decision: DURA_API_KEY geroteerd op Railway (task #19 completed). P1 security sprint 100% afgerond. P2.6 users naar env vars completed. P3.1 AI sprint gestart (backend-dev + ai-specialist). DURA_USERS env var moet nog door Ernst op Railway gezet worden. P2.4 mobile menu goedgekeurd voor frontend-dev.
- [2026-02-11] [frontend_dev] Decision: P2.4 mobile hamburger menu voltooid. Nieuw nav.js script (44 regels) met toggle, aria-expanded, close-on-outside-click, close-on-Escape, close-on-link-click. Hamburger button (met aria-label) toegevoegd aan alle 5 dura/ pagina's. Hamburger CSS + active X-animatie + mobile dropdown styles toegevoegd aan styles.css en index.html inline styles. Op mobiel (<=768px) verbergt global-search, btn-warehouse en nav-user voor ruimte.
- [2026-02-11] [frontend_dev] Decision: P2.1 SLA Metrics dashboard sectie voltooid. 4 KPI cards toegevoegd aan index.html (On-Time Shipping, Order Accuracy, Doorlooptijd, Perfect Order Rate) met periode-selector (Vandaag/Week/Maand). Fetcht van /api/metrics/sla endpoint. Trend indicators met SVG pijlen (groen=beter, rood=slechter). Cycle time omgekeerde trend (omlaag=goed). Auto-refresh elke 60s. Alle data via textContent (XSS-safe). Purple kpi-icon class + --purple-light variabele toegevoegd.
- [2026-02-11] [ai-specialist] Decision: P3.1 backend her-review na fixes: GOEDGEKEURD voor productie. Beide blokkers opgelost: (1) page_insights format nu correct items[] met {type, text} objecten, (2) max_tokens verhoogd naar 1200. Validatie dekt 3 formaten (string/array/dict) voor backward compatibility. Bottleneck drempel 2u geaccepteerd als startpunt — bijstellen na live feedback.
- [2026-02-11] [business-analist] Decision: P3.1 backend completed (task #27). P3.1 frontend task #31 aangemaakt voor multi-bullet AI rendering in ai-insights.js. Frontend-dev pakt op na P2.2. P2.2 order modal (task #29) toegewezen aan frontend-dev.
- [2026-02-11] [frontend_dev] Decision: P2.2 Order detail modal uitgebreid met SLA status bar. createSLABar(order) helper toegevoegd aan orders.html en verzendingen.html. Berekent client-side of order on-time (groen), in behandeling (oranje) of vertraagd (rood) is op basis van createDate vs finishDate/shippedDate/now met 24u SLA. Visuele progress bar + badge + tijdsdetail. SLA_HOURS constante (24) bovenin beide scripts.
- [2026-02-11] [backend_dev] Decision: P3.1 AI prompt templates per pagina geimplementeerd in ai_updates.py. Volledige herschrijving generate_insights(): (1) Nieuwe _gather_extended_data() functie met 11 parallelle API calls voor uitgebreide data per pagina. (2) Bottleneck detectie: orders >2u open + attentionNeeded flag. (3) Burn-rate analyse: voorraad/dagelijkse verkoop = dagen resterend per product. (4) Carrier verdeling uit shipments. (5) Warehouse data: picks per medewerker, picks per uur, openstaande orders. (6) Week-over-week trend vergelijking. (7) Nieuw prompt template (AI_PROMPT_TEMPLATE) met gestructureerde instructies per pagina. (8) page_insights nu objecten met items array (type+text per bullet) i.p.v. 1 string — afgestemd met ai-specialist. (9) max_tokens 500->1200. (10) Uitgebreide backward compatibility: string, array, en object formaten worden allemaal genormaliseerd.
- [2026-02-11] [backend_dev] Decision: P2.7 Lifespan migratie. Deprecated @app.on_event("startup") vervangen door asynccontextmanager lifespan. Startup: cache pre-warming task + AI scheduler. Shutdown (nieuw): cancel cache task + close GoedgepicktAPI httpx client (aclose). Global _warm_task verwijderd, warm_task is nu local in lifespan scope. Geen API wijzigingen, puur backend code quality + correcte resource cleanup bij Railway redeploy.

---

## Verbeterplan Dura Fulfilment Portal (Business Analist)

### Huidige Staat - Samenvatting
Het portal bestaat uit 6 pagina's (Dashboard, Orders, Voorraad, Verzendingen, Warehouse Display, Rapportages) met live data uit Goedgepickt via een FastAPI backend op Railway. De basis is solide: live KPI's, order pipeline, carrier verdeling, AI briefing, zoekfunctie, export, en auto-refresh. Er zijn echter significante security issues en UX-verbetermogelijkheden.

### PRIORITEIT 1 — SECURITY (Blocker, moet eerst)
Gebaseerd op input security-analist. Zonder deze fixes kan de portal NIET in productie.

**P1.1 - API Key uit frontend halen** [KRITIEK]
- auth.js bevat hardcoded API key: `V-pp2ua1yNmcsskUPFdQLz2ZB2EYZTd4USjjWYmMlUU`
- ai-insights.js bevat dezelfde key als fallback
- Oplossing: Backend moet session-based auth doorsturen naar Goedgepickt. Frontend stuurt alleen session token, nooit API key.
- Toewijzing: **backend-dev** (backend auth flow aanpassen) + **frontend-dev** (API key verwijderen uit JS)

**P1.2 - XSS sanitization** [HOOG]
- Meerdere plekken gebruiken innerHTML met API data (index.html, orders.html, verzendingen.html, warehouse.html, voorraad.html)
- Oplossing: Overal textContent + createElement gebruiken i.p.v. innerHTML met template literals
- Toewijzing: **frontend-dev**

**P1.3 - CORS POST verwijderen** [HOOG]
- Backend staat POST toe op alle endpoints, maar alleen login heeft POST nodig
- Oplossing: allow_methods beperken, of POST alleen toestaan op /api/auth/*
- Toewijzing: **backend-dev**

**P1.4 - Google Fonts self-hosting in dura/** [LAAG maar GDPR]
- Dura subpagina's (orders.html, voorraad.html, etc.) laden nog Google Fonts extern
- index.html is al gefixt, maar gebruikt andere fonts (Inter vs DM Sans — inconsistentie!)
- Oplossing: Alle dura/ pagina's self-hosted fonts gebruiken, consistent DM Sans
- Toewijzing: **frontend-dev**

### PRIORITEIT 2 — UX & FUNCTIONALITEIT
Gebaseerd op sector best practices en huidige gaps.

**P2.1 - SLA Metrics toevoegen** [HOOG]
- Ontbreekt volledig: On-Time Shipping %, Order Accuracy Rate, Perfect Order Rate
- Dit zijn de #1 KPI's die elke 3PL klant wil zien
- Backend kan dit afleiden uit bestaande Goedgepickt data (order create date vs ship date)
- Toewijzing: **backend-dev** (nieuwe endpoint /api/metrics/sla) + **frontend-dev** (dashboard sectie)

**P2.2 - Order Detail verbetering** [MIDDEL]
- Order modal is goed maar mist: verwachte levertijd, SLA status, retour-info
- Track & Trace links openen in nieuw tabblad (goed)
- Toewijzing: **frontend-dev** (modal uitbreiden)

**P2.3 - Rapportages pagina functioneel maken** [HOOG]
- PDF/Excel download buttons werken niet (alert placeholder)
- Periode selector doet niets
- "Top Performers" tabel toont "niet beschikbaar" — koppel aan /api/picks/stats
- Piek uren chart is leeg — data IS beschikbaar via warehouse pagina logica
- Toewijzing: **frontend-dev** (rapportages.html herschrijven) + **backend-dev** (report export endpoint)

**P2.4 - Mobile responsive verbetering** [MIDDEL]
- Hamburger menu is er maar opent niet (geen JS handler)
- Tabellen scrollen horizontaal niet goed op mobiel
- Toewijzing: **frontend-dev**

**P2.5 - Consistentie design system** [LAAG]
- index.html gebruikt inline styles, andere pagina's gebruiken styles.css
- Sommige pagina's laden Inter font, andere DM Sans — moet allemaal DM Sans zijn
- warehouse.html heeft eigen color scheme (Inter font, andere variabelen)
- Toewijzing: **frontend-dev** (uniforme font + CSS variabelen)

### PRIORITEIT 3 — AI VERBETERING
Gebaseerd op uitgebreide analyse ai-specialist. Aanpak: Optie B (rijkere page_insights met meerdere bullet points per pagina).

**P3.1 - Pagina-specifieke AI inzichten (Quick Wins)** [HOOG]
- ai_updates.py uitbreiden: meer data-queries per pagina meegeven aan Claude
- Orders: bottleneck detectie (orders die lang in status staan), webshop-analyse
- Voorraad: burn-rate berekening (verkoopsnelheid vs huidige voorraad)
- Verzendingen: carrier verdeling analyse, verzendingssnelheid
- Warehouse: capaciteitsplanning, pick-optimalisatie suggesties
- Rapportages: natuurlijke taal samenvattingen
- ai-insights.js aanpassen: meerdere bullet points renderen i.p.v. 1 zin
- Toewijzing: **ai-specialist** (prompt templates + data requirements), **backend-dev** (queries), **frontend-dev** (rendering)

**P3.2 - Historische data + anomalie detectie** [MIDDEL]
- Historische data opslag (orders/dag, verkoopsnelheid per product)
- Anomalie-detectie (vergelijken met gemiddelden, afwijkingen signaleren)
- Herbestelpunt voorspellingen
- Piek-uur voorspellingen
- Toewijzing: **backend-dev** (data opslag + queries), **ai-specialist** (prompts)

**P3.3 - Geavanceerde AI (Backlog)** [LAAG]
- Interactieve AI chat ("Vraag het aan AI")
- Seizoensgebonden voorspellingen
- Dead stock analyse
- Automatische acties (herbestellingen triggeren)
- Toewijzing: toekomstige iteratie

### Taak Verdeling

#### frontend-dev (in volgorde):
1. ~~P1.2 - XSS fixes in alle dura/ pagina's~~ [IN PROGRESS]
2. P1.4 - Self-hosted fonts in alle dura/ pagina's + consistent DM Sans
3. P1.1 - API key verwijderen uit auth.js en ai-insights.js (NA backend P1.1 fix)
4. P2.4 - Mobile menu fix (hamburger JS handler)
5. P2.5 - Design system consistentie
6. P2.3 - Rapportages pagina functioneel maken
7. P2.1 - SLA metrics dashboard sectie
8. P2.2 - Order detail modal uitbreiden
9. P3.1 - AI insights rendering (meerdere bullet points per pagina)

#### backend-dev (in volgorde):
1. ~~P1.1 - Session-based auth~~ [DONE]
2. ~~P1.3 - CORS methods beperken~~ [DONE]
3. P1.5 - Rate limiting login + auth check AI refresh + SESSION_SECRET fix [IN PROGRESS]
4. P2.1 - SLA metrics endpoint (/api/metrics/sla)
5. P2.3 - Report export endpoint
6. P2 - Hardcoded users naar env/db, lifespan migratie, cache lock cleanup
7. P3.1 - AI data queries per pagina (met ai-specialist)

#### ai-specialist (in volgorde):
1. P3.1 - Prompt templates per pagina + data requirements definieren
2. P3.2 - Anomalie-detectie prompts en historische data requirements

