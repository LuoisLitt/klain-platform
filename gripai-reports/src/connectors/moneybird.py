"""
GripAI - Moneybird Connector
Haalt financiële data op uit Moneybird boekhouding.
"""

import httpx
from datetime import datetime
from typing import Optional


class MoneybirdConnector:
    """Connector voor Moneybird boekhoudsysteem."""
    
    BASE_URL = "https://moneybird.com/api/v2"
    
    def __init__(self, admin_id: str, token: str):
        """
        Initialize Moneybird connector.
        
        Args:
            admin_id: Moneybird administratie ID
            token: API access token
        """
        self.admin_id = admin_id
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    async def get_weekly_data(self, week_start: datetime, week_end: datetime) -> dict:
        """
        Haal alle relevante data op voor een week.
        
        Returns:
            Dict met omzet, kosten, facturen, etc.
        """
        async with httpx.AsyncClient() as client:
            # Parallel ophalen van verschillende endpoints
            invoices = await self._get_invoices(client, week_start, week_end)
            payments = await self._get_payments(client, week_start, week_end)
            # expenses = await self._get_expenses(client, week_start, week_end)
            
            # Bereken metrics
            revenue = sum(float(inv.get('total_price_incl_tax', 0)) for inv in invoices)
            invoices_paid = len([p for p in payments if p.get('payment_date')])
            
            # Haal openstaande facturen op
            outstanding = await self._get_outstanding_invoices(client)
            outstanding_total = sum(float(inv.get('total_unpaid', 0)) for inv in outstanding)
            
            # Bepaal verlopen facturen (> 30 dagen)
            overdue = []
            overdue_total = 0
            for inv in outstanding:
                due_date = inv.get('due_date')
                if due_date:
                    due = datetime.strptime(due_date, '%Y-%m-%d')
                    days_overdue = (datetime.now() - due).days
                    if days_overdue > 0:
                        amount = float(inv.get('total_unpaid', 0))
                        overdue_total += amount
                        overdue.append({
                            'customer': inv.get('contact', {}).get('company_name', 'Onbekend'),
                            'amount': amount,
                            'days_overdue': days_overdue,
                            'invoice_id': inv.get('invoice_id')
                        })
            
            # Sorteer overdue op bedrag
            overdue.sort(key=lambda x: x['amount'], reverse=True)
            
            # Top klanten deze week
            customer_revenue = {}
            for inv in invoices:
                contact = inv.get('contact', {})
                name = contact.get('company_name') or contact.get('firstname', 'Onbekend')
                amount = float(inv.get('total_price_incl_tax', 0))
                customer_revenue[name] = customer_revenue.get(name, 0) + amount
            
            top_customers = [
                {'name': name, 'revenue': rev}
                for name, rev in sorted(customer_revenue.items(), key=lambda x: x[1], reverse=True)[:5]
            ]
            
            return {
                'revenue': revenue,
                'costs': 0,  # TODO: expenses endpoint
                'profit': revenue,  # Voorlopig zonder kosten
                'invoices_sent': len(invoices),
                'invoices_paid': invoices_paid,
                'outstanding_total': outstanding_total,
                'outstanding_overdue': overdue_total,
                'top_customers': top_customers,
                'overdue_invoices': overdue[:5]
            }
    
    async def _get_invoices(self, client: httpx.AsyncClient, start: datetime, end: datetime) -> list:
        """Haal facturen op voor periode."""
        url = f"{self.BASE_URL}/{self.admin_id}/sales_invoices"
        params = {
            'filter': f"period:{start.strftime('%Y%m%d')}..{end.strftime('%Y%m%d')}",
            'per_page': 100
        }
        
        response = await client.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    async def _get_payments(self, client: httpx.AsyncClient, start: datetime, end: datetime) -> list:
        """Haal betalingen op voor periode."""
        url = f"{self.BASE_URL}/{self.admin_id}/financial_mutations"
        params = {
            'filter': f"period:{start.strftime('%Y%m%d')}..{end.strftime('%Y%m%d')}",
            'per_page': 100
        }
        
        response = await client.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    async def _get_outstanding_invoices(self, client: httpx.AsyncClient) -> list:
        """Haal alle openstaande facturen op."""
        url = f"{self.BASE_URL}/{self.admin_id}/sales_invoices"
        params = {
            'filter': 'state:open',
            'per_page': 100
        }
        
        response = await client.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    async def test_connection(self) -> bool:
        """Test of de API credentials werken."""
        async with httpx.AsyncClient() as client:
            url = f"{self.BASE_URL}/{self.admin_id}/contacts"
            params = {'per_page': 1}
            
            try:
                response = await client.get(url, headers=self.headers, params=params)
                return response.status_code == 200
            except Exception:
                return False
