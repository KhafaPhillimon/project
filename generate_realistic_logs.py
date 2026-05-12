"""
Realistic IIS Web Server Log Generator
Generates a human-looking dataset for BI & Data Analytics assignment.
Fixes: multi-day span, skewed country distribution, repeat IPs,
       mixed HTTP methods, asset requests, irregular row count.
"""

import csv
import random
from datetime import datetime, timedelta

random.seed(42)

# ── 1. Country → IP prefix pool (realistic African/Western ranges) ──────────
COUNTRY_IP_POOLS = {
    "Botswana":     ["41.76", "41.92", "41.170", "196.41", "196.50"],
    "Nigeria":      ["102.29", "102.73", "102.104", "102.184", "154.113"],
    "South Africa": ["196.21", "196.57", "196.69", "41.1", "197.184"],
    "Zimbabwe":     ["41.78", "41.205", "102.65", "196.37"],
    "UK":           ["155.18", "155.85", "155.130", "178.62", "86.1"],
    "USA":          ["157.72", "157.117", "157.240", "52.14", "34.201"],
    "Canada":       ["172.68", "172.17", "172.196", "99.235", "70.66"],
    "India":        ["103.21", "103.84", "103.240", "117.196"],
}

# ── 2. Realistic traffic weights (African focus) ─────────────────────────────
COUNTRY_WEIGHTS = {
    "Botswana":     18,
    "Nigeria":      22,
    "South Africa": 20,
    "Zimbabwe":      8,
    "UK":           10,
    "USA":           9,
    "Canada":        8,
    "India":         5,
}

# ── 3. Pages, methods, service types ────────────────────────────────────────
PAGES = [
    ("/index.html",          "GET",  "Homepage",          [200,200,200,304,404]),
    ("/jobs.html",           "GET",  "Job Request",       [200,200,304,404,500]),
    ("/scheduledemo.php",    "GET",  "Demo Request",      [200,200,304,404,500]),
    ("/scheduledemo.php",    "POST", "Demo Submission",   [200,200,200,500]),
    ("/events.html",         "GET",  "Promotional Event", [200,200,304,404,500]),
    ("/assistant.php",       "GET",  "AI Assistant",      [200,200,304,404,500]),
    ("/prototype.php",       "GET",  "Prototype Request", [200,200,304,404,500]),
    ("/images/events.jpg",   "GET",  "Image Asset",       [200,200,304,304,404]),
    ("/images/logo.png",     "GET",  "Image Asset",       [200,200,304,304]),
    ("/css/style.css",       "GET",  "CSS Asset",         [200,304,304]),
    ("/jobs.html",           "POST", "Job Application",   [200,200,302,500]),
    ("/contact.html",        "GET",  "Contact Page",      [200,200,404]),
]

# Weights favour page-level over asset requests
PAGE_WEIGHTS = [18, 14, 10, 4, 10, 11, 12, 4, 3, 3, 5, 3]   # sums ~97 ≈ 100

# ── 4. Date range: 3 weeks (April 20 – May 11 2026) ─────────────────────────
START_DATE = datetime(2026, 4, 20)
END_DATE   = datetime(2026, 5, 11, 23, 59, 59)

def random_timestamp():
    delta = END_DATE - START_DATE
    rand_seconds = random.randint(0, int(delta.total_seconds()))
    dt = START_DATE + timedelta(seconds=rand_seconds)
    # Simulate busier hours (8am–10pm) with higher probability
    if random.random() < 0.7:
        hour = random.randint(8, 22)
        dt = dt.replace(hour=hour, minute=random.randint(0, 59),
                        second=random.randint(0, 59))
    return dt.strftime("%d/%m/%Y %H:%M:%S")

def random_ip(country):
    prefix = random.choice(COUNTRY_IP_POOLS[country])
    return f"{prefix}.{random.randint(1,254)}.{random.randint(1,254)}"

def random_response_size(page, status):
    if "Asset" in page or ".jpg" in page or ".png" in page or ".css" in page:
        return random.randint(500, 15000)
    if status == 304:
        return 0
    if status == 404:
        return random.randint(200, 800)
    return random.randint(1200, 12000)

# ── 5. Build a pool of repeat IPs (simulates returning visitors) ─────────────
REPEAT_IP_POOL = []
countries_list = list(COUNTRY_WEIGHTS.keys())
country_weights_list = list(COUNTRY_WEIGHTS.values())
for _ in range(80):
    c = random.choices(countries_list, weights=country_weights_list)[0]
    REPEAT_IP_POOL.append((c, random_ip(c)))

# ── 6. Generate rows ─────────────────────────────────────────────────────────
TARGET_ROWS = random.randint(487, 523)   # intentionally irregular
rows = []

for _ in range(TARGET_ROWS):
    # 25% chance of a returning visitor
    if random.random() < 0.25 and REPEAT_IP_POOL:
        country, ip = random.choice(REPEAT_IP_POOL)
    else:
        country = random.choices(countries_list, weights=country_weights_list)[0]
        ip = random_ip(country)

    page_entry = random.choices(PAGES, weights=PAGE_WEIGHTS)[0]
    page, method, service_type, status_pool = page_entry

    status = random.choice(status_pool)
    response_size = random_response_size(page, status)
    timestamp = random_timestamp()

    rows.append({
        "timestamp":     timestamp,
        "ip_address":    ip,
        "country":       country,
        "method":        method,
        "page":          page,
        "service_type":  service_type,
        "status_code":   status,
        "response_size": response_size,
    })

# Sort by timestamp so the log looks chronological
rows.sort(key=lambda r: datetime.strptime(r["timestamp"], "%d/%m/%Y %H:%M:%S"))

# ── 7. Write CSV ─────────────────────────────────────────────────────────────
out_file = "AI_Solutions_Web_Log_Dataset.csv"
fieldnames = ["timestamp","ip_address","country","method",
              "page","service_type","status_code","response_size"]

with open(out_file, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# ── 8. Summary ───────────────────────────────────────────────────────────────
from collections import Counter
print(f"✅ Generated {len(rows)} rows  →  {out_file}")
print(f"   Date range: {rows[0]['timestamp'][:10]} → {rows[-1]['timestamp'][:10]}")
print()
print("Country distribution:")
for k, v in Counter(r["country"] for r in rows).most_common():
    print(f"  {k:<15} {v:>4} rows  ({v/len(rows)*100:.1f}%)")
print()
print("Service type distribution:")
for k, v in Counter(r["service_type"] for r in rows).most_common():
    print(f"  {k:<22} {v:>4} rows")
print()
print("HTTP Method split:")
for k, v in Counter(r["method"] for r in rows).most_common():
    print(f"  {k}  {v}")
print()
print("Status code split:")
for k, v in Counter(str(r["status_code"]) for r in rows).most_common():
    print(f"  {k}  {v}")
