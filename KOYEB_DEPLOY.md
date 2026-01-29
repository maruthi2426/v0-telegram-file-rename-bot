# Koyeb Deployment Guide for Telegram File Rename Bot

## What Was Fixed
The error `TypeError: Client.__init__() got an unexpected keyword argument 'name'` has been fixed.
- Changed `name=` parameter to `session_name=` in Pyrogram Client initialization
- This is the correct parameter for Pyrogram 1.4.16+

## Prerequisites
Before deploying to Koyeb, ensure you have:

1. **Koyeb Account**: [Create free account](https://app.koyeb.com)
2. **GitHub Repository**: Push your code to GitHub
3. **Environment Variables Ready**:
   - `API_ID` - From my.telegram.org
   - `API_HASH` - From my.telegram.org
   - `BOT_TOKEN` - From @BotFather
   - `DATABASE_URL` - MongoDB connection string
   - `OWNER_ID` - Your Telegram user ID

## Step-by-Step Koyeb Deployment

### Step 1: Prepare Your GitHub Repository

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Fix: Pyrogram Client parameter for Koyeb deployment"

# Push to GitHub
git push origin main
```

### Step 2: Create Koyeb Service

1. Go to [Koyeb Dashboard](https://app.koyeb.com)
2. Click **"Create Service"** button
3. Select **"GitHub"** as source
4. Choose your repository
5. Select **main** branch

### Step 3: Configure Build Settings

In the Koyeb deployment form, configure:

**Build Settings:**
- **Builder:** Buildpack (automatic Python detection)
- **Build Command:** Leave empty (auto-detected)
- **Run Command:** `python main.py`

### Step 4: Configure Environment Variables

Add these environment variables in Koyeb:

| Variable | Value | Example |
|----------|-------|---------|
| `API_ID` | Your API ID | `24663402` |
| `API_HASH` | Your API Hash | `xxxxxxxxxxxxxxxxxxxx` |
| `BOT_TOKEN` | Your Bot Token | `7959043781:AAH1KLvMF...` |
| `DATABASE_URL` | MongoDB URL | `mongodb+srv://user:pass@cluster.mongodb.net/db` |
| `OWNER_ID` | Your User ID | `1061920195` |

**Important:** Make sure `DATABASE_URL` includes the password and database name:
```
mongodb+srv://username:password@cluster.mongodb.net/database_name
```

### Step 5: Configure Port Settings

**Important for Koyeb:**
- **Port:** Leave default (Telegram doesn't require webhook port)
- **Protocol:** Default (not needed for bot polling)

### Step 6: Deploy

1. Click **"Deploy"** button
2. Wait for deployment (2-5 minutes)
3. Check logs for: `BOT IS RUNNING AND READY`

### Step 7: Verify Deployment

After deployment completes:

1. Check the Koyeb deployment logs
2. Look for these success messages:
   ```
   All required environment variables validated
   TELEGRAM FILE RENAME BOT
   Database connected successfully
   Bot started successfully
   Bot name: YourBotName (@your_bot_username)
   ```

3. Test your bot:
   - Open Telegram
   - Find your bot by username
   - Send `/start` command
   - Bot should respond

## Troubleshooting Koyeb Deployment

### Issue: "Application exited with code 1"

**Solution:** Check environment variables:
```bash
# Verify in Koyeb dashboard under:
Settings → Environment Variables

# Make sure all these are set:
- API_ID (integer)
- API_HASH (string)
- BOT_TOKEN (string)
- DATABASE_URL (full MongoDB URL with password)
- OWNER_ID (integer)
```

### Issue: "No module named 'pyrogram'"

**Solution:** Koyeb should auto-detect `requirements.txt`
- Ensure `requirements.txt` exists in root directory
- Contains: `pyrogram==1.4.16`

### Issue: Database connection failed

**Solution:** Check MongoDB connection string:
```
# INCORRECT (missing password):
mongodb+srv://user@cluster.mongodb.net/db

# CORRECT (includes password):
mongodb+srv://user:password@cluster.mongodb.net/db
```

### Issue: Bot starts but doesn't respond

**Solution:** Check Telegram credentials:
1. `API_ID` and `API_HASH` from my.telegram.org (must match)
2. `BOT_TOKEN` from @BotFather (must be valid)
3. Bot must be started with /start command in Telegram

## Koyeb vs Other Platforms

| Feature | Koyeb | Render | Heroku |
|---------|-------|--------|--------|
| Free Tier | Yes (100 hours/month) | Yes (750 hours) | No |
| Auto-restart | Yes | Yes | Yes |
| Python Support | Excellent | Excellent | Good |
| Setup Time | 5-10 min | 5-10 min | 10-15 min |
| Cost | Free → $5/month | Free → $7/month | $7+/month |

## Monitoring Deployment

### View Logs in Koyeb

1. Go to your service dashboard
2. Click **"Logs"** tab
3. Monitor real-time logs

### Health Checks

Koyeb will check if your service is running:
- If bot crashes, Koyeb auto-restarts it
- Check logs if service keeps restarting

## Best Practices for Koyeb

1. **Keep logs clean**: Remove debug prints in production
2. **Use environment variables**: Never hardcode secrets
3. **Monitor memory**: Bot is lightweight (~50MB)
4. **Test locally first**: Run locally before deploying
5. **Keep dependencies updated**: Regularly update Python packages

## Quick Checklist

- [ ] GitHub repository created and code pushed
- [ ] All environment variables set in Koyeb
- [ ] MongoDB URL includes password
- [ ] `requirements.txt` has all dependencies
- [ ] `main.py` uses correct Pyrogram parameters
- [ ] Bot token is from @BotFather
- [ ] API credentials from my.telegram.org
- [ ] Owner ID is your Telegram user ID
- [ ] Deployed and logs show no errors
- [ ] Bot responds to /start in Telegram

## Getting Help

If deployment fails:

1. **Check logs**: Koyeb dashboard → Logs tab
2. **Verify env vars**: Settings → Environment Variables
3. **Test locally**: `python main.py` after setting .env
4. **Common fixes**:
   - Restart service (Koyeb dashboard)
   - Redeploy from GitHub
   - Check for typos in environment variables

## Next Steps

1. Deploy to Koyeb using this guide
2. Test bot functionality
3. Monitor logs for 24 hours
4. Share bot with users

---

**Your bot should be live in 10-15 minutes!**
