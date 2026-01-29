# Deployment Guide - Render, Heroku, Railway & Koyeb

Complete guide for deploying the File Rename Bot to different platforms.

## Table of Contents

1. [Render (Recommended)](#render-recommended)
2. [Heroku](#heroku)
3. [Railway](#railway)
4. [Koyeb](#koyeb)
5. [Post-Deployment Verification](#post-deployment-verification)
6. [Monitoring & Maintenance](#monitoring--maintenance)
7. [Troubleshooting](#troubleshooting)

---

## Render (Recommended)

Render is **the easiest and fastest option** for deploying this bot. Free tier available!

### Prerequisites

- GitHub account with code pushed
- Render account (free at https://render.com)
- All credentials ready (.env values)

### Step-by-Step Deployment

#### 1. Push Code to GitHub

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "File Rename Bot - Initial Commit"

# Create repository on GitHub (web interface)
# Then add remote:
git remote add origin https://github.com/yourusername/file-rename-bot.git
git branch -M main
git push -u origin main
```

#### 2. Create Render Account

1. Go to https://render.com
2. Click "Sign up"
3. Connect with GitHub account
4. Authorize Render

#### 3. Deploy on Render

1. Go to https://render.com/dashboard
2. Click "New +" button (top right)
3. Select "Web Service"
4. Click "Connect account" and authorize GitHub
5. Select your `file-rename-bot` repository
6. Fill in settings:
   - **Name**: `file-rename-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Instance Type**: Free tier
7. Click "Create Web Service"

#### 4. Add Environment Variables

1. In your service dashboard, go to **Environment**
2. Click "Add Environment Variable"
3. Add each variable from your .env:

```
API_ID              = 123456789
API_HASH            = your_api_hash_here
BOT_TOKEN           = your_bot_token_here
DB_URL              = mongodb+srv://user:pass@cluster.mongodb.net/
DATABASE_NAME       = file_rename_bot
OWNER_ID            = 987654321
LOG_CHANNEL         = -1001234567890
FORCE_SUBS          = optional_channel
START_PIC           = optional_url
```

4. Click "Save Changes"

#### 5. Deploy

- Click "Create Web Service"
- Wait 2-3 minutes for deployment
- Check "Logs" tab for "Bot started successfully"
- Your bot is now live!

#### 6. Keep Bot Always Running

Render free tier services go to sleep after 15 minutes of inactivity.

**Solution 1: Render Paid Plan**
- Upgrade to $7/month (Starter plan)
- Keeps bot running 24/7

**Solution 2: Keep Alive Service**
- Use a free service like UptimeRobot
- Ping your service every 5 minutes
- Keeps it awake

**Setup UptimeRobot (Free)**:
1. Go to https://uptimerobot.com
2. Create free account
3. Add new monitor
4. Monitor type: HTTP(s)
5. Get your Render URL from dashboard
6. Set interval to 5 minutes
7. Save

#### Render Dashboard Features

- **Logs** - Real-time bot output
- **Metrics** - CPU, memory, network usage
- **Environment** - Manage variables
- **Redeploy** - Restart without code changes
- **Settings** - Configure deployment

---

## Heroku

Heroku free tier is deprecated, but here's how to deploy if using paid tier.

### Prerequisites

- GitHub repository with code
- Heroku account (paid)
- Heroku CLI installed

### Installation & Setup

#### 1. Install Heroku CLI

**Windows**:
- Download from https://devcenter.heroku.com/articles/heroku-command-line
- Run installer
- Verify: `heroku --version`

**macOS**:
```bash
brew tap heroku/brew && brew install heroku
```

**Linux**:
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

#### 2. Login to Heroku

```bash
heroku login
# Opens browser for authentication
```

#### 3. Create Heroku App

```bash
heroku create file-rename-bot
# Creates app and adds git remote
```

#### 4. Set Environment Variables

```bash
heroku config:set API_ID=123456789
heroku config:set API_HASH=your_api_hash
heroku config:set BOT_TOKEN=your_bot_token
heroku config:set DB_URL=mongodb+srv://user:pass@cluster.mongodb.net/
heroku config:set DATABASE_NAME=file_rename_bot
heroku config:set OWNER_ID=987654321
heroku config:set LOG_CHANNEL=-1001234567890
```

Verify:
```bash
heroku config
```

#### 5. Deploy

```bash
# Deploy from git
git push heroku main

# Watch deployment
heroku logs --tail

# Should see: "Bot started successfully"
```

#### 6. Enable Dyno

```bash
# Scale to 1 dyno
heroku ps:scale worker=1

# Check status
heroku ps
```

### Managing Heroku App

```bash
# View logs
heroku logs --tail

# Restart
heroku restart

# Config variables
heroku config
heroku config:set KEY=value
heroku config:unset KEY

# Stop
heroku ps:scale worker=0

# Start
heroku ps:scale worker=1
```

---

## Railway

Modern alternative to Heroku. Free tier available!

### Prerequisites

- GitHub account
- Railway account (https://railway.app)

### Step-by-Step Deployment

#### 1. Create Railway Account

1. Go to https://railway.app
2. Sign up with GitHub
3. Authorize Railway

#### 2. Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Authorize Railway to access GitHub
4. Select your `file-rename-bot` repository

#### 3. Configure Service

1. Railway auto-detects Python
2. Go to **Variables** tab
3. Add environment variables:

```
API_ID=123456789
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
DB_URL=mongodb+srv://...
DATABASE_NAME=file_rename_bot
OWNER_ID=987654321
LOG_CHANNEL=-1001234567890
```

#### 4. Configure Start Command

1. Go to **Settings**
2. Set start command: `python main.py`

#### 5. Deploy

- Click "Deploy"
- Wait for deployment to complete
- Check logs for "Bot started successfully"

### Railway Features

- Free tier with monthly credits
- GitHub integration with auto-deploy
- Web UI for environment variables
- Real-time logs
- Easy scaling
- Custom domains

---

## Koyeb

Edge computing platform with global distribution.

### Prerequisites

- GitHub account
- Koyeb account (https://koyeb.com)

### Deployment Steps

#### 1. Create Koyeb Account

1. Go to https://koyeb.com
2. Sign up
3. Verify email

#### 2. Connect GitHub

1. Go to https://app.koyeb.com
2. Click "Create"
3. Select "GitHub"
4. Authorize Koyeb

#### 3. Configure App

1. Select repository: `file-rename-bot`
2. Fill in:
   - **App Name**: `file-rename-bot`
   - **GitHub Branch**: `main`
   - **Builder**: Select "Dockerfile" or "Python"
   - **Start Command**: `python main.py`

#### 4. Add Secrets (Environment Variables)

1. Go to **Secrets** section
2. Add each variable from .env

#### 5. Deploy

1. Click "Create & Deploy"
2. Monitor deployment in logs
3. Bot is live when you see "Bot started successfully"

### Koyeb Features

- Global edge deployment
- Free tier available
- Auto-scaling
- Custom domains
- Real-time logs
- Environment variable management

---

## Post-Deployment Verification

### Check Bot is Running

```bash
# Send /start command to your bot
# Should get welcome message
```

### Check Logs

**Render**:
- Dashboard → Service → Logs

**Heroku**:
```bash
heroku logs --tail
```

**Railway**:
- Dashboard → Deployments → View Logs

**Koyeb**:
- Dashboard → Service → Logs

### Test Commands

```
/start              ✓ Welcome message
/ping               ✓ Pong response
/help               ✓ Help text
/autorename         ✓ Format setup
/leaderboard        ✓ Shows leaderboard
[Send video file]   ✓ File gets renamed
```

### Verify Database Connection

- Bot should accept files
- Renamed files should be saved to database
- Leaderboard should show user activity

---

## Monitoring & Maintenance

### Regular Checks

**Daily**:
- Check if bot is responding
- Review error logs
- Check database connection

**Weekly**:
- Review user activity
- Check disk space usage
- Verify all features working

**Monthly**:
- Database backup
- Update dependencies
- Review security logs

### Updating Bot Code

#### Render

1. Make changes locally
2. Commit and push to GitHub
3. Render auto-deploys

```bash
git add .
git commit -m "Feature: Add new functionality"
git push origin main
```

Check deployment in Render dashboard.

#### Heroku

```bash
git add .
git commit -m "Update"
git push heroku main
```

#### Railway

Auto-deploys on GitHub push (if enabled).

#### Koyeb

Auto-deploys on GitHub push (if enabled).

### Updating Dependencies

```bash
# Update requirements.txt
pip install --upgrade pyrogram pymongo

# Regenerate
pip freeze > requirements.txt

# Commit
git add requirements.txt
git commit -m "Update dependencies"
git push
```

### Backup Database

**MongoDB Atlas** (Automatic):
- 7-day automatic backups
- Manual backup available
- Export data via Compass

**Manual Backup**:
```bash
# Export all data
mongoexport --uri "mongodb+srv://..." --db file_rename_bot --collection users --out users.json
```

---

## Troubleshooting

### Bot Not Starting

**Check logs first** - They usually show the issue.

#### Common Issues

**1. "Invalid API credentials"**
```
Solution:
- Verify API_ID and API_HASH from https://my.telegram.org
- API_ID must be a number
- No spaces in values
```

**2. "Module not found"**
```
Solution:
- Ensure requirements.txt is in root directory
- Check build command: pip install -r requirements.txt
```

**3. "MongoDB connection error"**
```
Solution:
- Verify DB_URL in environment variables
- Check IP whitelist in MongoDB Atlas
- Verify username/password
- Add your deployment platform IP to whitelist
```

**4. "Bot token invalid"**
```
Solution:
- Get fresh token from @BotFather
- Remove any spaces
- Exact copy-paste
```

### Bot Not Responding to Commands

**1. Check if running**
```bash
# Try /ping command
# Should respond immediately
```

**2. Check environment variables**
```bash
# Verify all variables are set
# Check there are no typos
```

**3. Check logs for errors**
```bash
# Look for exceptions or connection errors
# Check database connectivity
```

### Slow Response

**Causes**:
- Database overloaded
- Network latency
- Large file processing

**Solutions**:
- Add database indexes
- Use faster deployment region
- Optimize image processing
- Increase resources (paid plan)

### Database Errors

**Issue**: "Connection timeout"
```
Solution:
- Increase connection pool size
- Check internet connection
- Verify MongoDB Atlas cluster is running
```

**Issue**: "Authentication failed"
```
Solution:
- Verify username and password
- Check user permissions in MongoDB
- Regenerate credentials if needed
```

### Memory Issues

**Signs**:
- Bot crashes randomly
- Slow responses
- Log shows "Out of memory"

**Solutions**:
- Optimize image processing
- Delete old logs periodically
- Implement caching
- Upgrade to paid plan for more memory

### Deployment Won't Complete

**Check**:
- Python version (must be 3.11+)
- requirements.txt syntax
- Invalid environment variables
- File permissions

**Solution**:
```bash
# Verify locally
python main.py

# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r requirements.txt
```

---

## Performance Optimization

### Database Optimization

```python
# Add indexes in database.py
db.users.create_index("user_id")
db.thumbnails.create_index("user_id")
db.rename_formats.create_index("user_id")
```

### Caching

```python
# Cache leaderboard for 1 hour
leaderboard_cache = {}
leaderboard_time = None
```

### Rate Limiting

```python
# Limit requests per user
from collections import defaultdict
from time import time

rate_limit = defaultdict(lambda: {"count": 0, "reset": time()})
```

### Connection Pooling

MongoDB client uses connection pooling by default.

---

## Cost Comparison

| Platform | Free Tier | Price | Features |
|----------|-----------|-------|----------|
| Render | Yes | $7/month | Easy, auto-deploy, logs |
| Heroku | No | $25/month | Traditional, many features |
| Railway | Yes | Pay-as-you-go | Modern, competitive pricing |
| Koyeb | Yes | Pay-as-you-go | Global edge, scaling |

**Recommendation**: Start with **Render** free tier, upgrade to paid if needed.

---

## Migration Between Platforms

### Render → Heroku

```bash
# 1. Create Heroku app
heroku create new-app

# 2. Set variables
heroku config:set ...

# 3. Deploy
git push heroku main

# 4. Verify
heroku logs --tail
```

### Render → Railway

```bash
# 1. Create Railway project
# 2. Connect GitHub repo
# 3. Add environment variables
# 4. Deploy (automatic)
```

The code works the same on all platforms!

---

## Best Practices

1. **Environment Variables**
   - Never commit .env
   - Use .env.example template
   - Use strong passwords

2. **Deployment**
   - Test locally first
   - Use version control
   - Keep deployment logs

3. **Security**
   - Enable GitHub 2FA
   - Rotate credentials monthly
   - Monitor for suspicious activity

4. **Monitoring**
   - Set up uptime monitoring
   - Check logs regularly
   - Alert on errors

5. **Backups**
   - Weekly database backups
   - Export user data
   - Keep recovery procedures

---

## Support & Resources

- **Render Docs**: https://render.com/docs
- **Heroku Docs**: https://devcenter.heroku.com
- **Railway Docs**: https://docs.railway.app
- **Koyeb Docs**: https://koyeb.com/docs
- **MongoDB Docs**: https://docs.mongodb.com
- **Pyrogram Docs**: https://docs.pyrogram.org

---

Congratulations! Your bot is now deployed and running 24/7! 🚀

For updates and maintenance, refer to [README.md](README.md) and [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md).
