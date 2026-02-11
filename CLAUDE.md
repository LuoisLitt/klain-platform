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

