import requests, os, shutil, subprocess
from datetime import datetime, timezone
from pathlib import Path

# --- CONFIGURATION ---
APP_LIMITS = {
    "chrome.exe": 900,
    "minecraft.exe": 30,
    "RobloxPlayerBeta.exe": 30,  # Adjusted to actual process name you showed
}

WEB_DOMAIN_LIMITS = {
    "youtube.com": 60,
    "roblox.com": 30,
    "minecraft.com": 30,
}

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
BACKUP_HOSTS_PATH = HOSTS_PATH + ".backup"

BASE_URL = "http://localhost:5600/api/0"
WINDOW_BUCKET_PREFIX = "aw-watcher-window"
WEB_BUCKET_PREFIX = "aw-watcher-web-chrome"
# ----------------------

def get_buckets():
    r = requests.get(f"{BASE_URL}/buckets"); r.raise_for_status()
    return r.json()

def get_events(bucket_id, start, end):
    r = requests.get(f"{BASE_URL}/buckets/{bucket_id}/events", params={"start":start.isoformat(),"end":end.isoformat()})
    r.raise_for_status()
    return r.json()

def calculate_app_usage(events, app):
    return sum(ev.get("duration",0) for ev in events if ev.get("data",{}).get("app","").lower() == app.lower()) / 60

def calculate_domain_usage(events, domain):
    tot = 0
    for ev in events:
        d = ev.get("data", {})
        if domain.lower() in (d.get("url", "") + d.get("title", "")).lower():
            tot += ev.get("duration", 0)
    return tot / 60

def find_bucket(buckets, prefix):
    return next((b for b in buckets if b.startswith(prefix)), None)

def ensure_host_backup():
    if not Path(BACKUP_HOSTS_PATH).exists():
        shutil.copy(HOSTS_PATH, BACKUP_HOSTS_PATH)

def block_domains(domains):
    with open(HOSTS_PATH, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.writelines(lines)
        for domain in domains:
            if any(domain in line for line in lines):
                continue
            f.write(f"127.0.0.1 {domain}\n127.0.0.1 www.{domain}\n")
        f.truncate()

def restore_hosts():
    if Path(BACKUP_HOSTS_PATH).exists():
        shutil.copy(BACKUP_HOSTS_PATH, HOSTS_PATH)

def auto_close_app(app):
    try:
        subprocess.run(
            ["taskkill", "/f", "/im", app],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"SUCCESS: The process \"{app}\" has been terminated.")
    except subprocess.CalledProcessError as e:
        if "not found" in e.stderr.lower():
            # Process was not found, ignore silently
            pass
        else:
            print(f"ERROR: {e.stderr.strip()}")

def main():
    ensure_host_backup()
    now = datetime.now(timezone.utc)
    start = datetime(year=now.year, month=now.month, day=now.day, tzinfo=timezone.utc)
    buckets = get_buckets()

    wb = find_bucket(buckets, WINDOW_BUCKET_PREFIX)
    vb = find_bucket(buckets, WEB_BUCKET_PREFIX)
    if not wb or not vb:
        print("Missing watchers."); return

    wevents = get_events(wb, start, now)
    wevweb = get_events(vb, start, now)

    # Check apps usage
    for app, limit in APP_LIMITS.items():
        usage = calculate_app_usage(wevents, app)
        print(f"{app}: {usage:.1f}/{limit} min")
        if usage > limit:
            auto_close_app(app)

    # Check domains usage
    domains_to_block = []
    for dom, limit in WEB_DOMAIN_LIMITS.items():
        usage = calculate_domain_usage(wevweb, dom)
        print(f"{dom}: {usage:.1f}/{limit} min")
        if usage > limit:
            domains_to_block.append(dom)

    if domains_to_block:
        print("Blocking domains:", ", ".join(domains_to_block))
        block_domains(domains_to_block)

    # Reset hosts at midnight (within first minute)
    if now.hour == 0 and now.minute == 0:
        print("Resetting hosts file for new day...")
        restore_hosts()

if __name__ == "__main__":
    main()
