#!/usr/bin/env python3
"""
GripAI Weekrapportage - Main Entry Point
Draait elke vrijdag om 17:00 via Railway cron
"""

import argparse
import asyncio
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

from services.database import Database
from services.email import EmailService
from analysis.weekly_report import WeeklyReportAnalyzer
from connectors.moneybird import MoneybirdConnector


async def generate_report_for_customer(customer: dict, db: Database, analyzer: WeeklyReportAnalyzer, email_service: EmailService):
    """Genereer en verstuur weekrapport voor één klant."""
    
    print(f"📊 Generating report for {customer['company_name']}...")
    
    # 1. Bepaal week periode
    today = datetime.now()
    week_end = today - timedelta(days=today.weekday() + 1)  # Afgelopen zondag
    week_start = week_end - timedelta(days=6)  # Maandag ervoor
    
    # 2. Haal data op uit boekhoudsysteem
    connector = get_connector(customer)
    if not connector:
        print(f"  ⚠️  No connector for {customer['accounting_system']}")
        return False
    
    try:
        weekly_data = await connector.get_weekly_data(week_start, week_end)
    except Exception as e:
        print(f"  ❌ Failed to fetch data: {e}")
        return False
    
    # 3. Haal vorige week op voor vergelijking
    previous_week = await db.get_previous_snapshot(customer['id'])
    
    # 4. Sla snapshot op
    snapshot_id = await db.save_snapshot(
        customer_id=customer['id'],
        week_start=week_start,
        week_end=week_end,
        data=weekly_data
    )
    
    # 5. Genereer AI analyse met Claude
    analysis = await analyzer.analyze(
        company_name=customer['company_name'],
        current_week=weekly_data,
        previous_week=previous_week,
        week_start=week_start,
        week_end=week_end
    )
    
    # 6. Genereer en verstuur email
    success = await email_service.send_report(
        to_email=customer['email'],
        company_name=customer['company_name'],
        analysis=analysis,
        data=weekly_data,
        week_start=week_start,
        week_end=week_end
    )
    
    # 7. Log rapport in database
    await db.save_report(
        customer_id=customer['id'],
        snapshot_id=snapshot_id,
        analysis=analysis,
        sent=success
    )
    
    if success:
        print(f"  ✅ Report sent to {customer['email']}")
    else:
        print(f"  ❌ Failed to send report")
    
    return success


def get_connector(customer: dict):
    """Return juiste connector voor klant's boekhoudsysteem."""
    system = customer.get('accounting_system', '').lower()
    credentials = customer.get('accounting_credentials', {})
    
    if system == 'moneybird':
        return MoneybirdConnector(
            admin_id=credentials.get('admin_id'),
            token=credentials.get('token')
        )
    # Voeg hier meer connectors toe:
    # elif system == 'exact':
    #     return ExactConnector(...)
    # elif system == 'snelstart':
    #     return SnelstartConnector(...)
    
    return None


async def run_all_reports():
    """Genereer rapporten voor alle actieve klanten."""
    
    print("=" * 50)
    print("🚀 GripAI Weekrapportage")
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    # Initialize services
    db = Database()
    analyzer = WeeklyReportAnalyzer()
    email_service = EmailService()
    
    # Haal alle actieve klanten op
    customers = await db.get_active_customers()
    
    if not customers:
        print("Geen actieve klanten gevonden.")
        return
    
    print(f"📋 {len(customers)} klant(en) gevonden\n")
    
    # Genereer rapport voor elke klant
    success_count = 0
    for customer in customers:
        success = await generate_report_for_customer(
            customer, db, analyzer, email_service
        )
        if success:
            success_count += 1
    
    print("\n" + "=" * 50)
    print(f"✅ Klaar: {success_count}/{len(customers)} rapporten verzonden")
    print("=" * 50)


async def run_test_report():
    """Test met demo data (geen echte klant nodig)."""
    
    print("🧪 Running test report with demo data...\n")
    
    analyzer = WeeklyReportAnalyzer()
    email_service = EmailService()
    
    # Demo data
    demo_data = {
        'revenue': 24750.00,
        'costs': 18200.00,
        'profit': 6550.00,
        'invoices_sent': 12,
        'invoices_paid': 8,
        'outstanding_total': 15420.00,
        'outstanding_overdue': 4200.00,
        'top_customers': [
            {'name': 'Familie de Vries', 'revenue': 8500.00},
            {'name': 'Bakkerij Jansen', 'revenue': 4200.00},
            {'name': 'Restaurant het Dorp', 'revenue': 3800.00},
        ],
        'overdue_invoices': [
            {'customer': 'Bouwbedrijf Klaassen', 'amount': 2800.00, 'days_overdue': 21},
            {'customer': 'Garage Pietersen', 'amount': 1400.00, 'days_overdue': 7},
        ]
    }
    
    previous_week = {
        'revenue': 21300.00,
        'costs': 16800.00,
        'profit': 4500.00,
        'invoices_sent': 9,
        'invoices_paid': 11,
        'outstanding_total': 12800.00,
    }
    
    today = datetime.now()
    week_end = today - timedelta(days=today.weekday() + 1)
    week_start = week_end - timedelta(days=6)
    
    # Genereer analyse
    analysis = await analyzer.analyze(
        company_name="Keukenleverancier Drenthe B.V.",
        current_week=demo_data,
        previous_week=previous_week,
        week_start=week_start,
        week_end=week_end
    )
    
    print("📝 Generated Analysis:")
    print("-" * 40)
    print(analysis)
    print("-" * 40)
    
    # Optioneel: verstuur test email
    test_email = os.getenv('TEST_EMAIL')
    if test_email:
        print(f"\n📧 Sending test email to {test_email}...")
        success = await email_service.send_report(
            to_email=test_email,
            company_name="Keukenleverancier Drenthe B.V.",
            analysis=analysis,
            data=demo_data,
            week_start=week_start,
            week_end=week_end
        )
        print("✅ Sent!" if success else "❌ Failed")
    else:
        print("\n💡 Set TEST_EMAIL env var to receive test report")


def main():
    parser = argparse.ArgumentParser(description='GripAI Weekrapportage')
    parser.add_argument('--run-reports', action='store_true', help='Run reports for all customers')
    parser.add_argument('--test', action='store_true', help='Run test with demo data')
    args = parser.parse_args()
    
    if args.run_reports:
        asyncio.run(run_all_reports())
    elif args.test:
        asyncio.run(run_test_report())
    else:
        print("GripAI Weekrapportage")
        print("Usage:")
        print("  python main.py --test         Run test with demo data")
        print("  python main.py --run-reports  Generate reports for all customers")


if __name__ == '__main__':
    main()
