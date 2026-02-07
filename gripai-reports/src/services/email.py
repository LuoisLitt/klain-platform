"""
GripAI - Email Service (Resend)
"""

import os
from datetime import datetime
from pathlib import Path
from jinja2 import Template
import resend


class EmailService:
    """Email verzending via Resend."""
    
    def __init__(self):
        resend.api_key = os.getenv('RESEND_API_KEY')
        self.from_email = os.getenv('FROM_EMAIL', 'rapport@gripai.nl')
        self.template = self._load_template()
    
    def _load_template(self) -> Template:
        """Laad email template."""
        template_path = Path(__file__).parent.parent / 'templates' / 'report.html'
        
        if template_path.exists():
            return Template(template_path.read_text())
        
        # Fallback inline template
        return Template(self._get_default_template())
    
    async def send_report(
        self,
        to_email: str,
        company_name: str,
        analysis: str,
        data: dict,
        week_start: datetime,
        week_end: datetime
    ) -> bool:
        """Verstuur weekrapport email."""
        
        week_str = f"{week_start.strftime('%d %b')} - {week_end.strftime('%d %b %Y')}"
        
        # Render HTML
        html = self.template.render(
            company_name=company_name,
            week_period=week_str,
            analysis=analysis,
            revenue=f"€{data.get('revenue', 0):,.2f}",
            costs=f"€{data.get('costs', 0):,.2f}",
            profit=f"€{data.get('profit', 0):,.2f}",
            invoices_sent=data.get('invoices_sent', 0),
            invoices_paid=data.get('invoices_paid', 0),
            outstanding=f"€{data.get('outstanding_total', 0):,.2f}",
            outstanding_overdue=f"€{data.get('outstanding_overdue', 0):,.2f}",
            year=datetime.now().year
        )
        
        try:
            resend.Emails.send({
                "from": f"GripAI <{self.from_email}>",
                "to": [to_email],
                "subject": f"Weekrapport {company_name} | {week_str}",
                "html": html
            })
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False
    
    def _get_default_template(self) -> str:
        return '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weekrapport {{ company_name }}</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1a1a1a; max-width: 600px; margin: 0 auto; padding: 20px;">
    
    <div style="border-bottom: 2px solid #1a1a1a; padding-bottom: 20px; margin-bottom: 30px;">
        <h1 style="margin: 0; font-size: 24px; font-weight: 600;">Weekrapport</h1>
        <p style="margin: 5px 0 0 0; color: #666;">{{ company_name }} | {{ week_period }}</p>
    </div>
    
    <div style="background: #f8f9fa; border-radius: 8px; padding: 20px; margin-bottom: 30px;">
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
            <div>
                <p style="margin: 0; color: #666; font-size: 12px; text-transform: uppercase;">Omzet</p>
                <p style="margin: 5px 0 0 0; font-size: 20px; font-weight: 600;">{{ revenue }}</p>
            </div>
            <div>
                <p style="margin: 0; color: #666; font-size: 12px; text-transform: uppercase;">Winst</p>
                <p style="margin: 5px 0 0 0; font-size: 20px; font-weight: 600;">{{ profit }}</p>
            </div>
            <div>
                <p style="margin: 0; color: #666; font-size: 12px; text-transform: uppercase;">Facturen verzonden</p>
                <p style="margin: 5px 0 0 0; font-size: 20px; font-weight: 600;">{{ invoices_sent }}</p>
            </div>
            <div>
                <p style="margin: 0; color: #666; font-size: 12px; text-transform: uppercase;">Facturen betaald</p>
                <p style="margin: 5px 0 0 0; font-size: 20px; font-weight: 600;">{{ invoices_paid }}</p>
            </div>
        </div>
    </div>
    
    <div style="margin-bottom: 30px;">
        <h2 style="font-size: 16px; font-weight: 600; margin: 0 0 15px 0;">Analyse</h2>
        <div style="color: #333;">
            {{ analysis | replace('\n\n', '</p><p style="margin: 15px 0;">') | replace('\n', '<br>') | safe }}
        </div>
    </div>
    
    <div style="background: #fff3cd; border-radius: 8px; padding: 15px; margin-bottom: 30px;">
        <p style="margin: 0; font-size: 14px;">
            <strong>Openstaand:</strong> {{ outstanding }}<br>
            <strong>Waarvan verlopen:</strong> {{ outstanding_overdue }}
        </p>
    </div>
    
    <div style="border-top: 1px solid #eee; padding-top: 20px; color: #666; font-size: 12px;">
        <p style="margin: 0;">
            Dit rapport is automatisch gegenereerd door GripAI.<br>
            Vragen? Mail naar support@gripai.nl
        </p>
        <p style="margin: 15px 0 0 0;">
            &copy; {{ year }} GripAI. Grip op uw bedrijf.
        </p>
    </div>
    
</body>
</html>'''
