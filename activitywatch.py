import requests
import datetime
import os

# --- CONFIGURE YOUR LIMITS BELOW ---
LIMITS = [
    {"type": "domain", "target": "youtube.com", "limit_minutes": 120, "app": "chrome.exe"},
    {"type": "domain", "target": "roblox.com", "limit_minutes": 60, "app": "chrome.exe"},
    {"type": "domain", "target": "minecraft.com", "limit_minutes": 60, "app": "chrome.exe"},
    {"type": "app", "target": "roblox.exe", "limit_minutes": 30},
    {"type": "app", "target": "minecraft.exe", "limit_minutes": 60}
]
# ------------------------------------

base_url = 'http://localhost:5600/api/0'
now = datetime.datetime.now()
start_time = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
end_time = now.isoformat()

def get_buckets():
    try:
        r = requests.get(f"{base_url}/buckets")
        return r.json()
    except Exception as e:
        print("❌ Could not connect to ActivityWatch. Is it running?")
        exit(1)

def get_events(bucket_id):
    r = requests.get(f"{base_url}/buckets/{bucket_id}/events",
                     params={'start': start_time, 'end': end_time})
    return r.json()

def calculate_domain_usage(domain):
    buckets = get_buckets()
    web_bucket = next((v for k, v in buckets.items() if 'aw-watcher-web' in k), None)
    if not web_bucket:
        print("⚠️ No web tracking data found.")
        return 0

    events = get_events(web_bucket['id'])
    total = 0
    for i in range(len(events) - 1):
        url = events[i]['data'].get('url', '')
        if domain in url:
            t1 = datetime.datetime.fromisoformat(events[i]['timestamp'])
            t2 = datetime.datetime.fromisoformat(events[i + 1]['timestamp'])
            total += (t2 - t1).total_seconds()
    return total

def calculate_app_usage(app_name):
    buckets = get_buckets()
    app_bucket = next((v for k, v in buckets.items() if 'aw-watcher-window' in k), None)
    if not app_bucket:
        print("⚠️ No app tracking data found.")
        return 0

    events = get_events(app_bucket['id'])
    total = 0
    for i in range(len(events) - 1):
        app = events[i]['data'].get('app', '')
        if app.lower() == app_name.lower():
            t1 = datetime.datetime.fromisoformat(events[i]['timestamp'])
            t2 = datetime.datetime.fromisoformat(events[i + 1]['timestamp'])
            total += (t2 - t1).total_seconds()
    return total

# --- MAIN LOGIC ---
for limit in LIMITS:
    target = limit["target"]
    limit_sec = limit["limit_minutes"] * 60

    if limit["type"] == "domain":
        used = calculate_domain_usage(target)
    elif limit["type"] == "app":
        used = calculate_app_usage(target)
    else:
        continue  # invalid type, skip

    used_min = used / 60
    print(f"⏱ {target}: {used_min:.1f} / {limit['limit_minutes']} minutes used")

    if used > limit_sec:
        app_to_kill = limit.get("app", target)  # fallback to app name if not specified
        os.system(f"taskkill /f /im {app_to_kill}")
        print(f"🚫 Closed {app_to_kill} — daily limit exceeded!")
