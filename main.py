import pandas as pd
from datetime import datetime
from src.scraper import get_companies_and_people
from src.email_validator import validate_email_smtp
from src.export_to_sheets import push_csv_to_sheet


def main():
    print("🚀 Starting OptiRPA lead generation...")
    leads = []

    for c in get_companies_and_people():
        status = validate_email_smtp(c["email"])
        c["email_status"] = status
        c["discovered_at"] = datetime.utcnow().isoformat()
        leads.append(c)

    df = pd.DataFrame(leads)
    df.to_csv("data/leads.csv", index=False)
    print(f"✅ Saved {len(df)} leads to data/leads.csv")

    push_csv_to_sheet("data/leads.csv", "OptiRPA Leads")
    print("✅ Uploaded to Google Sheet")


if __name__ == "__main__":
    main()

