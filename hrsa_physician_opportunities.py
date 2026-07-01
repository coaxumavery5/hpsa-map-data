from playwright.sync_api import sync_playwright
import csv
import json

URL = "https://connector.hrsa.gov/connector/search?discipline=Physician,%20MD%2FDO"

captured_data = {"data": None}

def is_opportunities_response(response):
    return "opportunities" in response.url

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # ----------------------------
    # CAPTURE NETWORK RESPONSE
    # ----------------------------
    def handle_response(response):
        if is_opportunities_response(response):
            try:
                captured_data["data"] = response.json()
                print("Captured HRSA API response!")
            except:
                pass

    page.on("response", handle_response)

    print("Loading HRSA page...")
    page.goto(URL)

    # wait for JS + API calls to finish
    page.wait_for_timeout(10000)

    browser.close()

data = captured_data["data"]

if not data:
    print("No data captured. Try increasing wait time.")
    exit()

# ----------------------------
# EXTRACT RESULTS SAFELY
# ----------------------------
if isinstance(data, dict):
    results = (
        data.get("content")
        or data.get("results")
        or data.get("items")
        or []
    )
else:
    results = data

print(f"Total records: {len(results)}")

# ----------------------------
# FILTER: MD/DO ONLY (EXCLUDE PA)
# ----------------------------
physicians = []

for item in results:
    if not isinstance(item, dict):
        continue

    discipline = str(item.get("discipline", "")).lower()

    is_physician = (
        "physician" in discipline or
        "md" in discipline or
        "d.o" in discipline or
        "do" in discipline
    )

    is_pa = (
        "physician assistant" in discipline
        or discipline == "pa"
    )

    if is_physician and not is_pa:
        physicians.append(item)

print(f"Physicians found: {len(physicians)}")

# ----------------------------
# LIMIT TO FIRST 15 RECORDS
# ----------------------------
physicians = physicians

print(f"Using {len(physicians)} physicians for Webflow import.")

# ----------------------------
# SAVE TO CSV
# ----------------------------
csv_file = "/Users/avery/Documents/CareerMD Internship/GitHub/hpsa-map-data/hrsa_physician_opportunities.csv"
if physicians:
    keys = set()
    for item in physicians:
        keys.update(item.keys())

    keys = list(keys)

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(physicians)

print(f"Saved → {csv_file}")