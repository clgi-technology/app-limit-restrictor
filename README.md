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

