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

