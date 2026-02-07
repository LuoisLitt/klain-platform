"""
GripAI - Weekly Report Analysis using Claude Sonnet
"""

import os
from datetime import datetime
from anthropic import Anthropic


class WeeklyReportAnalyzer:
    """Analyseert weekdata met Claude Sonnet."""
    
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model = "claude-sonnet-4-20250514"
    
    async def analyze(
        self,
        company_name: str,
        current_week: dict,
        previous_week: dict | None,
        week_start: datetime,
        week_end: datetime
    ) -> str:
        """
        Genereer AI analyse van weekdata.
        
        Returns:
            Geformatteerde analyse tekst in het Nederlands.
        """
        
        # Bouw context voor Claude
        prompt = self._build_prompt(
            company_name=company_name,
            current=current_week,
            previous=previous_week,
            week_start=week_start,
            week_end=week_end
        )
        
        # Roep Claude aan
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            messages=[
                {"role": "user", "content": prompt}
            ],
            system=self._get_system_prompt()
        )
        
        return response.content[0].text
    
    def _get_system_prompt(self) -> str:
        return """Je bent een financieel analist voor MKB-bedrijven in Nederland. 
Je schrijft wekelijkse rapportages die:
- Direct en to-the-point zijn
- Concrete cijfers benoemen
- Vergelijkingen maken met vorige periodes
- Actionable inzichten geven
- Risico's signaleren waar nodig

Schrijf in het Nederlands, zakelijk maar toegankelijk.
Gebruik geen emoji's.
Structureer met korte paragrafen, geen bullet points in de hoofdtekst.
Eindig altijd met 1-2 concrete aanbevelingen.

Houd de analyse beknopt: maximaal 250 woorden."""

    def _build_prompt(
        self,
        company_name: str,
        current: dict,
        previous: dict | None,
        week_start: datetime,
        week_end: datetime
    ) -> str:
        
        week_str = f"{week_start.strftime('%d %b')} - {week_end.strftime('%d %b %Y')}"
        
        prompt = f"""Schrijf een weekrapportage voor {company_name}.
Periode: {week_str}

DEZE WEEK:
- Omzet: EUR {current.get('revenue', 0):,.2f}
- Kosten: EUR {current.get('costs', 0):,.2f}
- Winst: EUR {current.get('profit', 0):,.2f}
- Facturen verzonden: {current.get('invoices_sent', 0)}
- Facturen betaald: {current.get('invoices_paid', 0)}
- Openstaand totaal: EUR {current.get('outstanding_total', 0):,.2f}
- Waarvan verlopen: EUR {current.get('outstanding_overdue', 0):,.2f}
"""

        if current.get('top_customers'):
            prompt += "\nTop klanten deze week:\n"
            for c in current['top_customers'][:3]:
                prompt += f"- {c['name']}: EUR {c['revenue']:,.2f}\n"
        
        if current.get('overdue_invoices'):
            prompt += "\nVerlopen facturen:\n"
            for inv in current['overdue_invoices'][:5]:
                prompt += f"- {inv['customer']}: EUR {inv['amount']:,.2f} ({inv['days_overdue']} dagen)\n"
        
        if previous:
            prompt += f"""
VORIGE WEEK:
- Omzet: EUR {previous.get('revenue', 0):,.2f}
- Kosten: EUR {previous.get('costs', 0):,.2f}
- Winst: EUR {previous.get('profit', 0):,.2f}
- Openstaand: EUR {previous.get('outstanding_total', 0):,.2f}

Bereken en benoem de week-over-week veranderingen."""
        
        return prompt
