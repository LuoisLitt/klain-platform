# MEMORY.md — Iris' Langetermijngeheugen

## Ernst
- Accountmanager MKB bij Rabobank, regio Emmen/Coevorden/Klazienaveen/Dalen
- Analytisch, goed met cijfers, commercieel sterk
- Fan van Suits (vandaar "Louis Litt" alias op Telegram)
- Zit in crypto: $DUSK (dusk.network)

## Klain (Side Project)
Ernst's eerste serieuze side project — AI automatisering voor MKB.
- **Naam**: Klain — kort, krachtig, professioneel. Domein: klain.nl
- **Diensten**: Weekrapportages, Offerte Generator, Debiteurenbeheer
- **Doelgroep**: MKB in Drenthe, bedrijven tot €10M omzet
- **Website**: `/Users/ernstbeekman/.openclaw/workspace/klain-website/`
- **Status**: Website + demo's gebouwd (feb 2025), nog niet live

### Design keuzes
- Apple.com geïnspireerd, minimalistisch
- Geen emoji's — moet professioneel ogen
- Nederlands, formeel ("u")
- Prijzen: €99 / €199 / €349 per maand

## Voorkeuren
- Formeel taalgebruik op zakelijke websites ("u" niet "je")
- Brand first, dan naam
- Liever concrete voorbeelden dan abstracte beschrijvingen
- Houdt van efficiëntie — niet te veel woorden
- **Spawn sub-agents voor uitwerkingen**: Als Ernst vraagt om iets uit te werken of als het anders is dan gewoon chatten → use sessions_spawn. Niet alles in de main session doen.
- **Per-minuut updates bij sub-agent werk**: Wil regelmatige statusupdates krijgen (ongeveer elke minuut) als een sub-agent aan het werk is, in plaats van zwijgend wachten

## Dura Fulfilment (Klant van Klain)
- Live dashboard: https://gripai-website.vercel.app/dura/
- Backend: https://dura-backend-production.up.railway.app (Railway)
- Backend repo: https://github.com/LuoisLitt/dura-backend
- Goedgepickt API base: `https://account.goedgepickt.nl/api/v1`
- 180 webshops, 299k+ orders
- API limiet: max 10k results via page param, cursor nodig voor meer

## Technisch
- Model: Claude Opus 4.6 (gepatcht in pi-ai models.generated.js)
- Vercel deployed via `npx vercel --prod --yes` (niet via GitHub)
- Railway: aparte repo nodig (monorepo root directory werkte niet)
- GitHub push via: `gh auth login` + credential helper fix

## Notities
- Iris vernoemd door Ernst — Griekse godin van de regenboog, boodschapper
- Workspace: `/Users/ernstbeekman/.openclaw/workspace/`
