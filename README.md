**ActivityWatch** is a free, open-source, privacy-focused tool that **monitors how you spend your time on your computer**, including tracking which apps you use, for how long, and when.

---

## 🧠 What ActivityWatch Does

| Feature                  | Description                                                                                |
| ------------------------ | ------------------------------------------------------------------------------------------ |
| **App Usage Tracking**   | Tracks how long each app/window is active (e.g., Chrome, Word, Discord).                   |
| **Website Tracking**     | Tracks visited websites (in supported browsers like Chrome, Firefox).                      |
| **Idle Detection**       | Detects when you're not actively using the computer.                                       |
| **Cross-Platform**       | Works on **Windows, macOS, and Linux**.                                                    |
| **Local-Only**           | All data stays on your device — **no cloud sync** unless you set it up yourself.           |
| **Custom Timers & Tags** | Manually tag your time or create custom "buckets" for activities (e.g., "Work", "Gaming"). |

---

## 🔧 How to Use ActivityWatch

### 1. **Install It**

* Download from: [https://activitywatch.net](https://activitywatch.net)
* Choose your OS → Install

### 2. **Run It**

* It runs in the background.
* You’ll access it via a browser (usually at `http://localhost:5600`)

### 3. **Check Stats**

* View graphs of:

  * Time spent per app
  * Websites visited
  * Activity by hour
  * Time categories (if tagged)

---

## 📉 Can It Limit App Usage?

**By default: No**, ActivityWatch only tracks — it doesn’t block or limit.

BUT…

You can use it with third-party scripts/tools to enforce limits based on ActivityWatch’s logs.

For example:

* Monitor how long you use a game like Valorant
* After 1 hour, a script closes it automatically (using data from ActivityWatch’s JSON logs)

There’s an active community of developers using its **API** to build custom usage-based automation.

---

## ⚙️ Pros and Cons

### ✅ Pros

* Free & Open Source (FOSS)
* Works offline, respects your privacy
* Detailed usage analytics
* Customizable and scriptable (for advanced users)

### ❌ Cons

* No built-in app blocking or time limits
* UI is basic compared to commercial tools
* Requires technical knowledge for advanced automation

---

## ✅ Ideal For:

* People who want insight into their computer habits
* Developers, freelancers, students tracking productivity
* Privacy-conscious users (no cloud, no tracking)

---

Would you like help using ActivityWatch to build a custom usage-based time limiter or auto-shutdown system? I can guide you through that with code examples.


Yes, it is **possible** to automatically **close Chrome** **only if YouTube** (not just Chrome itself) was used for **more than 2 hours total** — but you'll need to use a combination of:

1. **ActivityWatch** – to **track** detailed browser usage (including time spent on YouTube specifically)
2. **A script** – to **parse ActivityWatch data** and **close Chrome** if the limit is exceeded

---

## ✅ What You Need

### 1. **ActivityWatch**

* Tracks time spent on websites (e.g., `youtube.com`) if the browser plugin is installed.
* Install extensions:

  * [ActivityWatch WebWatch Chrome Extension](https://chromewebstore.google.com/detail/nglaklhklhcoonedhgnpgddginnjdadi?utm_source=item-share-cb)

### 2. **Python Script**

* Reads data from ActivityWatch’s local API
* Finds total time spent on `youtube.com` today
* If over 2 hours, runs a `taskkill` to close Chrome

---

## 🔁 Workflow

1. You browse YouTube in Chrome.
2. ActivityWatch + browser extension logs `youtube.com`.
3. A Python script checks if `youtube.com` > 2 hours.
4. If true → it runs:

   ```cmd
   taskkill /f /im chrome.exe
   ```

---

## 🧪 Example: Python Script (Concept)

```python
import requests
import datetime
import os

# Connect to ActivityWatch
base_url = 'http://localhost:5600/api/0'
buckets = requests.get(f'{base_url}/buckets').json()

# Find the web browser bucket
web_bucket = next(b for b in buckets if 'aw-watcher-web' in b['id'])

# Time range: Today
now = datetime.datetime.now()
start_time = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
end_time = now.isoformat()

# Get events (web activity)
events = requests.get(
    f'{base_url}/buckets/{web_bucket["id"]}/events',
    params={'start': start_time, 'end': end_time}
).json()

# Accumulate time spent on YouTube
total_seconds = 0
for i in range(len(events) - 1):
    event = events[i]
    next_event = events[i + 1]
    if 'youtube.com' in event['data'].get('url', ''):
        duration = (datetime.datetime.fromisoformat(next_event['timestamp']) -
                    datetime.datetime.fromisoformat(event['timestamp'])).total_seconds()
        total_seconds += duration

# Close Chrome if limit exceeded (2 hours = 7200 seconds)
if total_seconds > 7200:
    os.system("taskkill /f /im chrome.exe")
    print("Closed Chrome due to excessive YouTube time.")
else:
    print(f"YouTube usage: {total_seconds/60:.2f} minutes.")
```

> ⚠️ You need the ActivityWatch browser extension installed **and enabled** for this to work.

---

## 🧰 How to Run the Script Automatically

* Save the script as `youtube_limiter.py`
* Use **Task Scheduler** to run it every 10–30 minutes

  * Trigger: "At logon" or every X minutes
  * Action: `python.exe "C:\path\to\youtube_limiter.py"`

---

## 🔐 Privacy Note

* All data stays local (ActivityWatch runs on `localhost`)
* No need for cloud, accounts, or external services

---

Would you like me to help you:

* Set up the Python environment?
* Customize this script for another website or browser?


Great! Let's set up everything step by step so you can **automatically close apps or limit websites (like YouTube or full browser usage)** to **2 hours per day** — no Microsoft account, no spyware, all local.

---

## ✅ OVERVIEW OF SETUP

We’ll do this in 4 parts:

| Step                                        | Goal                                         |
| ------------------------------------------- | -------------------------------------------- |
| 1. 🧩 Install ActivityWatch + Web Extension | To track website & app usage                 |
| 2. 🐍 Install Python                        | To run the logic that enforces the limits    |
| 3. 📜 Set up the Python Script              | To read data and close apps                  |
| 4. ⏰ Automate the Script                    | To run it every X minutes via Task Scheduler |

---

## 🧩 STEP 1: Install ActivityWatch + Browser Extension

### 🖥️ 1. Install ActivityWatch

* Go to: [https://activitywatch.net/downloads/](https://activitywatch.net/downloads/)
* Choose **Windows** version
* Run the installer → it will launch automatically

### 🌐 2. Install the Browser Extension

For **Chrome** or any Chromium-based browser:

* [ActivityWatch WebWatch Extension (Chrome)](https://chromewebstore.google.com/detail/activitywatch-webwatch/bpmibdpdmilmhdoogocmfcpmoapdffcb)
* After installing:

  * Click the extension → Enable it
  * Allow permissions for website tracking

> Optional for Firefox: [Webwatch for Firefox](https://addons.mozilla.org/en-US/firefox/addon/activitywatch-webwatch/)

---

## 🐍 STEP 2: Install Python

### 📥 Install Python (if you don’t have it already)

1. Download from: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
2. During install:

   * ✅ **Check “Add Python to PATH”**
   * Click **Install Now**

### 🧪 Test It

Open Command Prompt (`Win + R`, type `cmd`) and run:

```bash
python --version
```

You should see something like `Python 3.x.x`

---

## 📜 STEP 3: The Python Script

### 1. Open Notepad or VS Code and paste this script:

```python
import requests
import datetime
import os

# ---- CONFIGURATION ----
TARGET_APP = "chrome.exe"  # Change to app you want to limit
LIMIT_SECONDS = 2 * 60 * 60  # 2 hours
TARGET_DOMAIN = "youtube.com"  # Or use None to track all usage
# ------------------------

# Set up base URL
base_url = 'http://localhost:5600/api/0'

# Find browser bucket
try:
    buckets = requests.get(f'{base_url}/buckets').json()
    web_bucket = next(b for b in buckets if 'aw-watcher-web' in b['id'])
except Exception as e:
    print("Could not connect to ActivityWatch. Is it running?")
    exit(1)

# Get today's timeframe
now = datetime.datetime.now()
start_time = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
end_time = now.isoformat()

# Fetch events
events = requests.get(
    f'{base_url}/buckets/{web_bucket["id"]}/events',
    params={'start': start_time, 'end': end_time}
).json()

# Calculate usage time
total_seconds = 0
for i in range(len(events) - 1):
    event = events[i]
    next_event = events[i + 1]
    url = event['data'].get('url', '')

    if TARGET_DOMAIN is None or TARGET_DOMAIN in url:
        t1 = datetime.datetime.fromisoformat(event['timestamp'])
        t2 = datetime.datetime.fromisoformat(next_event['timestamp'])
        duration = (t2 - t1).total_seconds()
        total_seconds += duration

# Act on usage
if total_seconds > LIMIT_SECONDS:
    os.system(f"taskkill /f /im {TARGET_APP}")
    print(f"✅ Closed {TARGET_APP} due to time limit ({total_seconds//60} min)")
else:
    print(f"⏱ {TARGET_DOMAIN or 'App'} usage: {total_seconds//60:.1f} minutes")
```

### 2. Save as:

```plaintext
youtube_limiter.py
```

---

## ⏰ STEP 4: Automate It with Task Scheduler

### 1. Open **Task Scheduler**

* Press `Win + S` → search: `Task Scheduler` → open it

### 2. Create a Basic Task

* Click **“Create Basic Task”**
* Name: `YouTube Limiter`
* Trigger: **Daily** → Recur every 1 day
* Action: **Start a program**

  * **Program/script:** `python`
  * **Add arguments:** `"C:\Path\To\youtube_limiter.py"` *(include quotes if there are spaces)*
* Finish setup

### Optional:

* For better automation, set a trigger to **“Repeat every 30 minutes”** using **“Advanced Settings”** under “Triggers” tab (Edit after creation)

---

## ✅ You're Done!

The script will now:

* Track time spent on YouTube (or any app you configure)
* Automatically close the app if time exceeds 2 hours

---

## 🔄 Want to Limit a Different App (e.g., Discord, a game)?

Just change:

```python
TARGET_APP = "discord.exe"
TARGET_DOMAIN = None  # No website tracking, just app
```

Or you can mix: limit total browser usage (`chrome.exe`) instead of specific domains.

---

Would you like me to generate a version that limits **total Chrome usage**, not just YouTube? Or want a version that handles **multiple apps** with separate limits?

Great — you have **Python 3.13.3** installed and working. That’s perfect!

Let’s proceed with finalizing your **YouTube (or app) time limiter setup**.

---

## ✅ Next Steps Checklist

You’ve already completed:

* ✅ Installed Python ✔
* ✅ Installed ActivityWatch + Web Extension ✔
* ✅ Verified Python is working ✔

Now let’s **run the Python script** and test it before automating it.

---

## 🧪 Step-by-Step: Test the Script

### 1. **Create the Script File**

1. Open a text editor like **Notepad**, **VS Code**, or **Notepad++**.
2. Copy this Python script (YouTube limiter):

```python
import requests
import datetime
import os

# ---- CONFIGURATION ----
TARGET_APP = "chrome.exe"  # Change this if limiting another app
LIMIT_SECONDS = 2 * 60 * 60  # 2 hours in seconds
TARGET_DOMAIN = "youtube.com"  # Set to None to limit full browser usage
# ------------------------

base_url = 'http://localhost:5600/api/0'

try:
    buckets = requests.get(f'{base_url}/buckets').json()
    web_bucket = next(b for b in buckets if 'aw-watcher-web' in b['id'])
except Exception as e:
    print("❌ ERROR: Cannot connect to ActivityWatch. Is it running?")
    exit(1)

now = datetime.datetime.now()
start_time = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
end_time = now.isoformat()

events = requests.get(
    f'{base_url}/buckets/{web_bucket["id"]}/events',
    params={'start': start_time, 'end': end_time}
).json()

total_seconds = 0
for i in range(len(events) - 1):
    url = events[i]['data'].get('url', '')
    if TARGET_DOMAIN is None or TARGET_DOMAIN in url:
        t1 = datetime.datetime.fromisoformat(events[i]['timestamp'])
        t2 = datetime.datetime.fromisoformat(events[i + 1]['timestamp'])
        total_seconds += (t2 - t1).total_seconds()

if total_seconds > LIMIT_SECONDS:
    os.system(f"taskkill /f /im {TARGET_APP}")
    print(f"✅ Closed {TARGET_APP} after {total_seconds/60:.1f} minutes on {TARGET_DOMAIN}")
else:
    print(f"⏱ {TARGET_DOMAIN or 'App'} usage today: {total_seconds/60:.1f} minutes")
```

3. Save it as:

```plaintext
C:\Users\<YourUsername>\youtube_limiter.py
```

Replace `<YourUsername>` with your actual Windows user name.

---

### 2. **Make Sure ActivityWatch is Running**

* It should auto-start with Windows. If not, run it from:

  ```
  C:\Users\<YourUsername>\AppData\Local\Programs\ActivityWatch\activitywatch.exe
  ```

* Check that it’s running by visiting:

  ```
  http://localhost:5600
  ```

You should see the ActivityWatch dashboard.

---

### 3. **Run the Script Manually (Test It)**

Open Git Bash or Command Prompt, and run:

```bash
python "C:/Users/<YourUsername>/youtube_limiter.py"
```

You should see output like:

```bash
⏱ youtube.com usage today: 54.7 minutes
```

or, if limit is passed:

```bash
✅ Closed chrome.exe after 128.3 minutes on youtube.com
```

---

## 🎯 Optional Next Steps

Would you like help with one of the following?

1. **Make it run every 30 minutes automatically** via Task Scheduler
2. **Limit full Chrome usage**, not just YouTube
3. **Apply time limits to multiple apps or websites**
4. **Turn it into a system tray tool with a UI** (advanced)

Let me know how you'd like to continue!

Perfect — you want to apply **daily time limits to multiple apps or websites**, like:

* YouTube → 2 hours/day
* Discord → 1 hour/day
* Games → 90 minutes/day
* Or limit **total Chrome/Firefox time**, regardless of site

We’ll upgrade your script to handle **multiple entries**, each with its own limit.

---

## ✅ MULTI-LIMIT SCRIPT OVERVIEW

You’ll define a list like this:

```python
LIMITS = [
    {"type": "domain", "target": "youtube.com", "limit_minutes": 120, "app": "chrome.exe"},
    {"type": "domain", "target": "discord.com", "limit_minutes": 60, "app": "chrome.exe"},
    {"type": "app",    "target": "notepad.exe", "limit_minutes": 30},
    {"type": "app",    "target": "discord.exe", "limit_minutes": 60}
]
```

The script will:

* Pull usage data from ActivityWatch
* Add up today's usage for each target
* Close the relevant app if time exceeds the limit

---

## 🧠 PREREQUISITES (RECAP)

* ✅ \[x] ActivityWatch running (with web extension enabled for browser tracking)
* ✅ \[x] Python installed
* ✅ \[x] Know app names (like `chrome.exe`, `notepad.exe`, etc.)

---

## 🧠 SMART MULTI-TARGET SCRIPT (CONCEPT)

Here’s the full code:

```python
import requests
import datetime
import os

# --- CONFIGURE YOUR LIMITS HERE ---
LIMITS = [
    {"type": "domain", "target": "youtube.com", "limit_minutes": 120, "app": "chrome.exe"},
    {"type": "domain", "target": "discord.com", "limit_minutes": 60, "app": "chrome.exe"},
    {"type": "app", "target": "notepad.exe", "limit_minutes": 30},
    {"type": "app", "target": "discord.exe", "limit_minutes": 60}
]
# -----------------------------------

base_url = 'http://localhost:5600/api/0'
now = datetime.datetime.now()
start_time = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
end_time = now.isoformat()

def get_buckets():
    try:
        return requests.get(f"{base_url}/buckets").json()
    except Exception as e:
        print("❌ Could not connect to ActivityWatch. Is it running?")
        exit(1)

def get_events(bucket_id):
    r = requests.get(f"{base_url}/buckets/{bucket_id}/events",
                     params={'start': start_time, 'end': end_time})
    return r.json()

def calculate_domain_usage(domain):
    buckets = get_buckets()
    web_bucket = next((b for b in buckets if 'aw-watcher-web' in b['id']), None)
    if not web_bucket:
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
    app_bucket = next((b for b in buckets if 'aw-watcher-window' in b['id']), None)
    if not app_bucket:
        return 0

    events = get_events(app_bucket['id'])
    total = 0
    for i in range(len(events) - 1):
        title = events[i]['data'].get('app', '')
        if title.lower() == app_name.lower():
            t1 = datetime.datetime.fromisoformat(events[i]['timestamp'])
            t2 = datetime.datetime.fromisoformat(events[i + 1]['timestamp'])
            total += (t2 - t1).total_seconds()
    return total

# Main logic
for limit in LIMITS:
    target = limit["target"]
    limit_sec = limit["limit_minutes"] * 60

    if limit["type"] == "domain":
        used = calculate_domain_usage(target)
    elif limit["type"] == "app":
        used = calculate_app_usage(target)
    else:
        continue

    used_min = used / 60
    print(f"⏱ {target}: {used_min:.1f}/{limit['limit_minutes']} minutes")

    if used > limit_sec:
        app_to_kill = limit.get("app", target)
        os.system(f"taskkill /f /im {app_to_kill}")
        print(f"✅ Closed {app_to_kill} — over daily limit ({used_min:.1f} min)")

```

---

## 🔧 How to Use This Script

1. Save the script as:

```plaintext
multi_limiter.py
```

2. Edit the `LIMITS` list:

   * Set websites under `"type": "domain"`
   * Set direct apps under `"type": "app"`
   * Use `limit_minutes` to control each limit
   * `app` is optional unless the domain needs to be tied to a specific program (e.g., `chrome.exe`)

---

## 🔁 Automate It (Optional)

Use **Task Scheduler** to run:

```bash
python "C:\Path\To\multi_limiter.py"
```

* Run at login or every 30 minutes

---

## ✅ Example Use Cases

| Limit                      | Setup                                                                                    |
| -------------------------- | ---------------------------------------------------------------------------------------- |
| Limit YouTube to 2 hrs/day | `{"type": "domain", "target": "youtube.com", "limit_minutes": 120, "app": "chrome.exe"}` |
| Limit Discord desktop app  | `{"type": "app", "target": "discord.exe", "limit_minutes": 60}`                          |
| Limit Chrome entirely      | `{"type": "app", "target": "chrome.exe", "limit_minutes": 180}`                          |
| Limit Steam to 90 minutes  | `{"type": "app", "target": "steam.exe", "limit_minutes": 90}`                            |

---

Would you like help with:

* Saving + testing this script now?
* Adding a specific app or site to the `LIMITS` list?
* Setting it up to run automatically?

Yes — you can absolutely run the script **24/7** (or at regular intervals) using **Windows Task Scheduler**, which is built into Windows.

This lets the script:

* Track app and website usage continuously
* Automatically block sites like `youtube.com` via `hosts` file when limits are reached
* Optionally unblock them at midnight (daily reset)

---

### ✅ Here’s how to set it up:

#### 1. **Save your Python script**

Make sure it includes logic to:

* Track time
* Modify the `hosts` file when needed
* (Optional) Reset daily usage counters

Example name: `C:\Users\melba\Documents\activitywatch_blocker.py`

---

#### 2. **Create a `.bat` launcher script**

This helps Task Scheduler run the Python script reliably.

Example `launch_blocker.bat`:

```bat
@echo off
cd C:\Users\melba\Documents
python activitywatch_blocker.py
```

---

#### 3. **Schedule the script**

Open **Task Scheduler** and follow these steps:

##### ➤ General Tab:

* Name: `ActivityWatch Limiter`
* Select: **"Run with highest privileges"** (important for editing `hosts` file)
* Choose: "Run whether user is logged in or not"

##### ➤ Triggers Tab:

* Add: **Repeat task every 5 minutes**, indefinitely

##### ➤ Actions Tab:

* Action: **Start a program**
* Program/script: `C:\Users\melba\Documents\launch_blocker.bat`

##### ➤ Conditions & Settings:

* Uncheck "Start task only if on AC power" if you want it to run always
* Enable “Allow task to be run on demand” for testing

---

#### 4. **Run it manually once to test**

* Right-click the task → “Run”
* Check `hosts` file or console output
* Confirm it's working properly

---

### 🔄 Daily Reset Option

You can also schedule a **separate task at midnight** to:

* Clear time logs (optional)
* Restore original `hosts` file (to unblock all sites)

I can include that logic in the script if you want.

---

### ✅ Next Step:

Would you like the full script updated to:

* Modify `hosts` file for blocking/unblocking
* Track usage limits
* Be ready for Task Scheduler?

Just confirm and I’ll post it.

---

Fantastic! Here's the **complete solution** including:

1. **Python script** that:

   * Tracks app and website usage via ActivityWatch
   * Auto-closes apps when limits are exceeded
   * Modifies your `hosts` file to block specified domains when limits are reached
   * Resets blocks and internal tracking at midnight

2. A **`.bat` launcher script** for Task Scheduler

3. Setup instructions for Task Scheduler to run it regularly and daily reset

---

## 🐍 `activitywatch_blocker.py` — Full Script

```python
import requests, os, shutil
from datetime import datetime, timezone
from pathlib import Path

# --- CONFIGURATION ---
APP_LIMITS = {
    "chrome.exe": 180,
    "notepad++.exe": 30,
    "discord.exe": 60,
}

WEB_DOMAIN_LIMITS = {
    "youtube.com": 120,
    "roblox.com": 60,
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
    return sum(ev.get("duration",0) for ev in events if ev.get("data",{}).get("app","").lower()==app.lower())/60

def calculate_domain_usage(events, domain):
    tot=0
    for ev in events:
        d=ev.get("data",{})
        if domain.lower() in (d.get("url","")+d.get("title","")).lower():
            tot+=ev.get("duration",0)
    return tot/60

def find_bucket(buckets,prefix):
    return next((b for b in buckets if b.startswith(prefix)), None)

def ensure_host_backup():
    if not Path(BACKUP_HOSTS_PATH).exists():
        shutil.copy(HOSTS_PATH,BACKUP_HOSTS_PATH)

def block_domains():
    with open(HOSTS_PATH,'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.writelines(lines)
        for domain in WEB_DOMAIN_LIMITS:
            if any(domain in line for line in lines):
                continue
            f.write(f"127.0.0.1 {domain}\n127.0.0.1 www.{domain}\n")
        f.truncate()

def restore_hosts():
    if Path(BACKUP_HOSTS_PATH).exists():
        shutil.copy(BACKUP_HOSTS_PATH, HOSTS_PATH)

def auto_close_app(app):
    os.system(f"taskkill /f /im {app}")

def main():
    ensure_host_backup()
    now = datetime.now(timezone.utc)
    start = datetime(year=now.year,month=now.month,day=now.day,tzinfo=timezone.utc)
    buckets=get_buckets()

    wb=find_bucket(buckets,WINDOW_BUCKET_PREFIX)
    vb=find_bucket(buckets,WEB_BUCKET_PREFIX)
    if not wb or not vb:
        print("Missing watchers."); return

    wevents = get_events(wb,start,now)
    wevweb = get_events(vb,start,now)

    # Track flags if domains exceed limits
    domain_block_needed = False

    # Check apps
    for app,limit in APP_LIMITS.items():
        usage=calculate_app_usage(wevents,app)
        print(f"{app}: {usage:.1f}/{limit} min")
        if usage>limit:
            auto_close_app(app)

    # Check domains
    for dom,limit in WEB_DOMAIN_LIMITS.items():
        usage=calculate_domain_usage(wevweb,dom)
        print(f"{dom}: {usage:.1f}/{limit} min")
        if usage>limit:
            domain_block_needed=True

    if domain_block_needed:
        print("Blocking domains...")
        block_domains()

    # Reset at midnight: if now is within first minute of day
    if now.hour==0 and now.minute==0:
        print("Resetting hosts file for new day...")
        restore_hosts()

if __name__=="__main__":
    main()
```

---

## ⚙️ `launch_blocker.bat` — For Task Scheduler

```bat
@echo off
cd /d "%~dp0"
python "%~dp0activitywatch_blocker.py"
```

*(Place both files in the same folder, e.g. `C:\Users\melba\Documents\ActivityLimiter`)*

---

## 📅 Setup Task Scheduler

1. Open **Task Scheduler**
2. **Create New Task**

   * Name: `ActivityWatch Limiter`
   * Check “Run with highest privileges”
   * Select “Run whether user is logged on or not”
3. 📌 **Triggers**

   * Trigger 1: At startup, repeat every 5 minutes for duration: “Indefinitely”
   * Trigger 2: Daily at 00:00 (midnight), one-time—used for reset logic
4. 🔧 **Actions**

   * Action: Start a program

     * Program/script: `C:\Users\melba\Documents\ActivityLimiter\launch_blocker.bat`
5. **Conditions**: Uncheck “Only run on AC power” if needed
6. **Settings**: Enable “Allow task to be run on demand” for testing

---

## ✅ How It Works

* **Every \~5 minutes**:

  * Tracks usage
  * Auto-closes apps over limits
  * Blocks domains via `hosts` if website usage exceeds limits
* **At midnight**: restores original `hosts` to lift all blocks
* Your browser will redirect blocked sites to `127.0.0.1`, effectively stopping access

---

Got it! To run your Python script periodically with Windows Task Scheduler using a `.bat` file, here’s a step-by-step guide along with an example `.bat` script to create the scheduled task.

---

### 1. Create a `.bat` file to run your Python script

Create a file named, for example, `run_usage_limiter.bat` with the following content:

```bat
@echo off
REM Adjust python path if needed
SET PYTHON_PATH=C:\Path\To\Python\python.exe
SET SCRIPT_PATH=C:\Path\To\Your\script.py

REM Run the python script
"%PYTHON_PATH%" "%SCRIPT_PATH%"
```

* Replace `C:\Path\To\Python\python.exe` with the full path to your Python interpreter.
* Replace `C:\Path\To\Your\script.py` with the full path to your Python script.

---

### 2. Create a Task Scheduler task via another `.bat` file or PowerShell

You can automate the task creation with a `.bat` file like this:

Create a file named `create_task.bat` with:

```bat
@echo off
REM Replace the paths below
SET TASK_NAME=UsageLimiter
SET SCRIPT_BAT_PATH=C:\Path\To\run_usage_limiter.bat

REM Create a task to run every 5 minutes starting now
schtasks /create /sc minute /mo 5 /tn "%TASK_NAME%" /tr "\"%SCRIPT_BAT_PATH%\"" /rl highest /f

echo Task created: %TASK_NAME%
pause
```

* Replace `C:\Path\To\run_usage_limiter.bat` with your actual `.bat` file path.
* `/rl highest` runs the task with highest privileges (admin) which is required for hosts file and killing apps.
* `/mo 5` means every 5 minutes; change it to whatever interval you want (1, 10, etc.).

---

### 3. Run `create_task.bat` as Administrator

* Right-click the `create_task.bat` file and select **Run as administrator** to register the scheduled task.
* You should see “Task created: UsageLimiter” and then the task will be scheduled.

---

### 4. Verify in Task Scheduler

* Open **Task Scheduler** (`taskschd.msc`)
* Find the task named **UsageLimiter**
* Check triggers, actions, and run conditions
* You can run the task manually to test

---

### Summary

* Your python script is wrapped in `run_usage_limiter.bat` to run with the proper Python interpreter.
* `create_task.bat` registers the scheduled task to run every X minutes with admin rights.
* Modify paths and intervals as needed.

---


