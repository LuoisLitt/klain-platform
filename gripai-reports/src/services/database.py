"""
GripAI - Database Service (Supabase)
"""

import os
import json
from datetime import datetime
from typing import Optional
from supabase import create_client, Client


class Database:
    """Supabase database service voor GripAI."""
    
    def __init__(self):
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY required")
        
        self.client: Client = create_client(url, key)
    
    async def get_active_customers(self) -> list[dict]:
        """Haal alle actieve klanten op."""
        response = self.client.table('customers').select('*').eq('active', True).execute()
        return response.data
    
    async def get_customer(self, customer_id: str) -> Optional[dict]:
        """Haal specifieke klant op."""
        response = self.client.table('customers').select('*').eq('id', customer_id).single().execute()
        return response.data
    
    async def get_previous_snapshot(self, customer_id: str) -> Optional[dict]:
        """Haal meest recente snapshot op voor vergelijking."""
        response = (
            self.client.table('weekly_snapshots')
            .select('*')
            .eq('customer_id', customer_id)
            .order('week_end', desc=True)
            .limit(1)
            .execute()
        )
        
        if response.data:
            snapshot = response.data[0]
            # Parse raw_data JSON
            if snapshot.get('raw_data'):
                return snapshot['raw_data']
        
        return None
    
    async def save_snapshot(
        self,
        customer_id: str,
        week_start: datetime,
        week_end: datetime,
        data: dict
    ) -> str:
        """Sla weekdata snapshot op."""
        response = self.client.table('weekly_snapshots').insert({
            'customer_id': customer_id,
            'week_start': week_start.strftime('%Y-%m-%d'),
            'week_end': week_end.strftime('%Y-%m-%d'),
            'revenue': data.get('revenue', 0),
            'costs': data.get('costs', 0),
            'invoices_sent': data.get('invoices_sent', 0),
            'invoices_paid': data.get('invoices_paid', 0),
            'outstanding_amount': data.get('outstanding_total', 0),
            'raw_data': data
        }).execute()
        
        return response.data[0]['id']
    
    async def save_report(
        self,
        customer_id: str,
        snapshot_id: str,
        analysis: str,
        sent: bool
    ) -> str:
        """Sla gegenereerd rapport op."""
        response = self.client.table('reports').insert({
            'customer_id': customer_id,
            'snapshot_id': snapshot_id,
            'ai_analysis': analysis,
            'sent_at': datetime.now().isoformat() if sent else None
        }).execute()
        
        return response.data[0]['id']
    
    async def create_customer(
        self,
        name: str,
        email: str,
        company_name: str,
        accounting_system: str,
        accounting_credentials: dict
    ) -> str:
        """Maak nieuwe klant aan."""
        response = self.client.table('customers').insert({
            'name': name,
            'email': email,
            'company_name': company_name,
            'accounting_system': accounting_system,
            'accounting_credentials': accounting_credentials
        }).execute()
        
        return response.data[0]['id']
