# Render Deployment Guide - FIXED VERSION

## What Was Fixed

The "This action is not allowed" error has been fixed by:

1. ✅ **Correct environment variable handling** - Using `DATABASE_URL` (as shown in Render)
2. ✅ **Better error logging** - Now shows exactly what's wrong
3. ✅ **Validation before startup** - Checks all vars before bot starts
4. ✅ **Graceful shutdown** - Proper signal handling for Render
5. ✅ **Connection timeout handling** - MongoDB connection with retries
6. ✅ **Render-specific configuration** - Dedicated config file for Render

---

## Pre-Deployment Checklist

### 1. Local Validation (Do This First!)

Before deploying to Render, validate everything locally:

```bash
# Run the validation script
python validate.py
```

You should see:
```
✅ ALL VALIDATION CHECKS PASSED!
Your bot is ready for deployment to Render.
```

### 2. Collect Required Information

Get these values ready:

- **API_ID** - From https://my.telegram.org/apps
- **API_HASH** - From https://my.telegram.org/apps  
- **BOT_TOKEN** - From @BotFather on Telegram
- **OWNER_ID** - Your Telegram user ID (send /start to @userinfobot)
- **DATABASE_URL** - From MongoDB Atlas connection string
- **DATABASE_NAME** - Your database name (usually 'file_rename_bot')

### 3. MongoDB Setup

If not already set up:

1. Go to https://www.mongodb.com/cloud/atlas
2. Create a cluster (free tier available)
3. Create a user with username and password
4. Get connection string: Click "Connect" → "Connect your application"
5. Copy the MongoDB URI (looks like: `mongodb+srv://username:password@cluster.mongodb.net/?appName=Cluster0`)
6. **IMPORTANT**: In MongoDB Network Access, add IP whitelist:
   - Go to "Network Access"
   - Click "Add IP Address"
   - Enter `0.0.0.0/0` (allows all IPs for development)
   - Confirm

---

## Step-by-Step Render Deployment

### Step 1: Connect GitHub Repository

1. Go to https://render.com
2. Sign up / Sign in
3. Click "New +" → "Web Service"
4. Select "GitHub" as source
5. Authorize Render to access your GitHub
6. Select the repository with your bot code
7. Click "Connect"

### Step 2: Configure Build Settings

**Name:** `v0-telegram-file-rename-bot` (or any unique name)

**Branch:** `main` (or your branch)

**Root Directory:** Leave empty (unless it's a monorepo)

**Language:** Python 3

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
python main.py
```

### Step 3: Add Environment Variables

In the "Environment" section, add these variables:

| Variable | Value | Example |
|----------|-------|---------|
| `API_ID` | Your API ID | `12345678` |
| `API_HASH` | Your API Hash | `abcdef1234567890...` |
| `BOT_TOKEN` | Your bot token | `7959043781:AAH1KL...` |
| `DATABASE_URL` | MongoDB connection string | `mongodb+srv://user:pass@cluster.mongodb.net/?appName=Cluster0` |
| `OWNER_ID` | Your Telegram user ID | `123456789` |
| `DATABASE_NAME` | Database name | `file_rename_bot` |
| `ADMIN_IDS` | Admin IDs (optional) | `123456789,987654321` |
| `LOG_CHANNEL` | Log channel ID (optional) | `-1001234567890` |

**⚠️ IMPORTANT:**
- Check each variable spelling (case-sensitive)
- No extra spaces before/after values
- Don't use quotes in values
- All variables marked REQUIRED must be filled

### Step 4: Instance Type Selection

For free deployment:
- Select **Free** tier ($0/month, 512MB RAM, 0.1 CPU)
- Free instances spin down after 15 min inactivity
- Perfect for testing

For production use:
- Select **Starter** tier ($7/month, 512MB RAM, 0.5 CPU)
- Always running, no spin down
- Recommended for production

### Step 5: Deploy

1. Click "Create Web Service"
2. Render will start building (watch the "Logs" tab)
3. You should see:
   ```
   Build started...
   Running build command...
   pip install -r requirements.txt
   ... (installing packages) ...
   Build succeeded!
   Starting bot...
   All required environment variables validated
   TELEGRAM FILE RENAME BOT - RENDER DEPLOYMENT
   Connected to MongoDB successfully
   Bot client started successfully
   BOT IS RUNNING AND READY
   ```

4. If you see "BOT IS RUNNING AND READY" → Success! ✅
5. If you see errors → See Troubleshooting section below

---

## Testing Your Deployment

### 1. Check Logs

In Render dashboard:
1. Click on your web service
2. Click "Logs" tab
3. Look for "BOT IS RUNNING AND READY"

### 2. Test Bot Commands

On Telegram:
1. Find your bot (search for @YourBotUsername)
2. Send `/start`
3. Bot should respond with welcome message

### 3. Check MongoDB

Send a message to the bot to trigger database operations:
1. Send `/help`
2. Check MongoDB Atlas → Collections → users
3. You should see an entry for your user

---

## Troubleshooting Deployment

### Error: "Build failed"

**Check:**
1. Logs show the exact Python error
2. All dependencies in requirements.txt
3. No syntax errors in Python files

**Fix:**
```bash
# Validate locally first
python validate.py
python -m py_compile main.py
```

### Error: "BOT_TOKEN invalid"

**Check:**
- Copied the full token from @BotFather
- No extra spaces or characters
- Correct case (should have uppercase letters)

**Fix:**
1. Go to @BotFather on Telegram
2. /revoke to reset token
3. /newbot to create new token
4. Update in Render environment variables

### Error: "DATABASE_URL connection failed"

**Check:**
- Connection string is complete (includes password)
- Username and password are correct
- MongoDB cluster is running
- IP whitelist allows Render IPs

**Fix:**
1. MongoDB Atlas → Network Access
2. Add IP `0.0.0.0/0` (or check Render IPs)
3. Test connection string locally

### Error: "API_ID or API_HASH invalid"

**Check:**
- From correct Telegram account
- At https://my.telegram.org/apps
- Not from another bot or service

**Fix:**
1. Go to https://my.telegram.org/apps
2. Sign in with your Telegram account
3. Copy API ID and API Hash
4. Update in Render

### Bot starts but doesn't respond

**Check:**
- Bot token is correct
- API ID and API Hash are correct
- Bot is online in Telegram

**Fix:**
1. Wait 30 seconds (bot initializing)
2. Try sending /start again
3. Check Render logs for errors
4. Redeploy (click "Deploy")

---

## Monitoring Your Bot

### View Live Logs

In Render dashboard:
1. Click web service
2. Click "Logs"
3. See real-time logs as bot runs

### Check Database

In MongoDB Atlas:
1. Go to Collections
2. Check "users", "thumbnails", "captions" etc.
3. See real-time data

### Monitor Resource Usage

In Render dashboard:
1. Click "Metrics"
2. See CPU, RAM, Network usage
3. Free tier shows: 512MB RAM, 0.1 CPU

---

## Keeping Bot Running

### Free Tier (Spins Down)
- Bot stops after 15 minutes of inactivity
- Automatically restarts when you send a command
- Good for testing, not production

### Paid Tier (Always Running)
- Minimum Starter at $7/month
- Bot runs 24/7
- Recommended for production use

### Manual Restart

If bot seems stuck:
1. In Render dashboard
2. Click "Restart Service"
3. Bot will restart in 30 seconds

---

## Updating Bot Code

After making changes:

1. **Commit to GitHub:**
   ```bash
   git add .
   git commit -m "Update bot features"
   git push
   ```

2. **Redeploy:**
   - Render automatically detects changes
   - Starts new deployment
   - No downtime (graceful reload)

---

## Getting Help

### Check Logs First
Most issues are visible in logs. Render logs are very detailed.

### Common Solutions
1. Redeploy (click "Deploy" button)
2. Restart service (click "Restart" button)
3. Check all environment variables again
4. Run `python validate.py` locally

### Still Stuck?
1. Check TROUBLESHOOTING.md
2. Verify all 5 required environment variables
3. Test MongoDB connection locally
4. Try different branch/fresh deployment

---

## Success Indicators

✅ Build completes without errors
✅ Logs show "BOT IS RUNNING AND READY"
✅ Bot responds to /start command
✅ MongoDB shows new user entry
✅ No error messages in logs

You're deployed and running! 🎉
