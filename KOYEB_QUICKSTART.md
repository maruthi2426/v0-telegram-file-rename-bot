# Koyeb Quick Start - 10 Minutes to Live Bot

## The Fix
**Error Fixed:** `TypeError: Client.__init__() got an unexpected keyword argument 'name'`

Changed in `main.py`:
```python
# BEFORE (broken):
app = Client(name="FileRenameBot", ...)

# AFTER (fixed):
app = Client(session_name="FileRenameBot", ...)
```

## Deploy in 3 Steps

### Step 1: Push to GitHub (2 min)
```bash
git add .
git commit -m "Fix: Koyeb deployment - use session_name parameter"
git push origin main
```

### Step 2: Create Koyeb Service (3 min)

1. Go to https://app.koyeb.com
2. Click **"Create Service"**
3. Connect GitHub → Select your repo
4. Branch: `main`
5. Run Command: `python main.py`
6. Click **"Deploy"**

### Step 3: Add Environment Variables (3 min)

In Koyeb dashboard, go to **Settings → Environment Variables** and add:

```
API_ID = 24663402
API_HASH = your_api_hash_here
BOT_TOKEN = 7959043781:AAH1KLvMF...
DATABASE_URL = mongodb+srv://user:password@cluster.mongodb.net/database
OWNER_ID = 1061920195
```

## Verify It's Working

1. Check logs in Koyeb dashboard
2. Look for: `BOT IS RUNNING AND READY`
3. Open Telegram
4. Send `/start` to your bot
5. Bot responds → **Success!** ✓

## Common Issues

| Error | Fix |
|-------|-----|
| `Application exited with code 1` | Check environment variables |
| `No module named 'pyrogram'` | Push code to GitHub and redeploy |
| `Database connection failed` | Check DATABASE_URL format |
| `Bot doesn't respond` | Check API_ID, API_HASH, BOT_TOKEN |

## Key Differences: Koyeb vs Render

| Aspect | Koyeb | Render |
|--------|-------|--------|
| Free Hours | 100/month | 750/month |
| Setup | Easier | Similar |
| Cost | $5/month | $7/month |
| Restart | Auto | Auto |

## File That Was Fixed

**main.py** - Line 20-24:
```python
app = Client(
    session_name="FileRenameBot",  # Changed from "name"
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN"),
    workdir="sessions"
)
```

## What To Do Now

1. Read this file (you're doing it!)
2. Push code to GitHub
3. Deploy on Koyeb (follow Step-by-Step above)
4. Test in Telegram
5. Done! Bot is live

**Time to live bot: 10 minutes**
