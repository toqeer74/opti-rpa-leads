import json
import os
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials


def push_csv_to_sheet(csv_path: str, sheet_name: str):
    creds_json = os.environ.get("SHEETS_SA_JSON")
    if not creds_json:
        print("⚠️ No SHEETS_SA_JSON env found, skipping upload.")
        return
    info = json.loads(creds_json)
    creds = Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    gc = gspread.authorize(creds)
    try:
        sh = gc.open(sheet_name)
    except gspread.SpreadsheetNotFound:
        sh = gc.create(sheet_name)
    ws = sh.sheet1
    df = pd.read_csv(csv_path)
    ws.clear()
    ws.update([df.columns.values.tolist()] + df.values.tolist())
    print(f"📤 Uploaded {len(df)} rows to Google Sheet '{sheet_name}'")

