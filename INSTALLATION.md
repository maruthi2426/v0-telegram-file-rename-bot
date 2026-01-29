# Complete Installation Guide

Comprehensive step-by-step guide for installing and deploying the File Rename Bot.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Getting Credentials](#getting-credentials)
3. [Local Development Setup](#local-development-setup)
4. [Deployment Options](#deployment-options)
5. [Post-Deployment Configuration](#post-deployment-configuration)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

- **Python**: 3.11 or higher
- **Operating System**: Windows, macOS, or Linux
- **RAM**: 512 MB minimum
- **Storage**: 500 MB minimum
- **Internet**: Stable connection required

### Accounts Needed

1. **Telegram Account** (Free)
   - https://telegram.org

2. **MongoDB Account** (Free tier available)
   - https://www.mongodb.com/cloud/atlas

3. **Deployment Platform** (Choose one):
   - Render (Recommended) - https://render.com
   - Heroku - https://www.heroku.com
   - Railway - https://railway.app
   - Koyeb - https://koyeb.com

## Getting Credentials

### 1. Telegram API Credentials

#### Step A: Get API_ID and API_HASH

1. Go to https://my.telegram.org/auth
2. Sign in with your phone number
3. Click "API development tools"
4. Fill in the form:
   - App title: "File Rename Bot"
   - Short name: "frbot" (or any name)
   - Application type: "Desktop"
   - Description: "File renaming bot"
5. Accept terms and submit
6. You'll see your **API_ID** and **API_HASH**

**Save these values!**

#### Step B: Create Bot Token

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Choose a name for your bot (e.g., "File Rename Bot")
4. Choose a username (must end with "bot", e.g., "myfilebott")
5. BotFather will give you your **BOT_TOKEN**

**Save this value!**

#### Step C: Get Your User ID

1. In Telegram, search for **@userinfobot**
2. Send `/start`
3. It will show your **User ID** (save as OWNER_ID)

### 2. MongoDB Setup

#### Step A: Create MongoDB Account

1. Go to https://www.mongodb.com/cloud/atlas
2. Click "Try Free"
3. Sign up with email or Google
4. Verify email address

#### Step B: Create Cluster

1. Click "Create" to create a new project
2. Name it "FileRenameBot"
3. Click "Create Project"
4. Choose "Build a Database"
5. Select "Free" tier
6. Choose your preferred region
7. Name cluster "filerenamebot"
8. Click "Create"

#### Step C: Get Connection String

1. Wait for cluster to be created (2-3 minutes)
2. Click "Connect"
3. Choose "Drivers"
4. Select Python and version 4.0+
5. Copy the connection string

You'll see something like:
```
mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
```

#### Step D: Create Database User

1. In MongoDB Atlas, go to "Database Access"
2. Click "Add New Database User"
3. Create username and password
4. Note down username and password
5. Replace `<username>` and `<password>` in connection string

**Your DB_URL will look like:**
```
mongodb+srv://myuser:mypassword@cluster.mongodb.net/
```

#### Step E: Whitelist IP (Important)

1. Go to "Network Access" in MongoDB Atlas
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (for development)
4. For production, add specific IPs
5. Confirm

### 3. Create Log Channel

1. Open Telegram
2. Create a new group → "File Rename Bot Logs"
3. Make it a private channel
4. Add the bot you created as an admin
5. Send a test message
6. Forward the message to **@userinfobot**
7. It will show message info including **Chat ID** (negative number with -100 prefix)
8. Save this as **LOG_CHANNEL**

## Local Development Setup

### Windows

#### Step 1: Install Python

1. Go to https://www.python.org/downloads
2. Download Python 3.11+
3. Run installer
4. **IMPORTANT**: Check "Add Python to PATH"
5. Click "Install Now"

#### Step 2: Install Git

1. Download from https://git-scm.com
2. Run installer with default settings

#### Step 3: Setup Bot

```batch
# Open Command Prompt in desired directory

# Clone repository
git clone https://github.com/yourusername/file-rename-bot.git
cd file-rename-bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your command prompt

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env with your favorite text editor (Notepad, VSCode, etc.)
# Add all your credentials

# Run the bot
python main.py
```

You should see:
```
Bot started successfully
Bot name: YourBotName (@yourbotusername)
```

### macOS

#### Step 1: Install Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Step 2: Install Python

```bash
brew install python@3.11
brew install git
```

#### Step 3: Setup Bot

```bash
# Navigate to desired directory
cd ~/Desktop  # or your preferred location

# Clone repository
git clone https://github.com/yourusername/file-rename-bot.git
cd file-rename-bot

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) before your prompt

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit with your editor
nano .env  # or open with TextEdit

# Run the bot
python main.py
```

### Linux (Ubuntu/Debian)

```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.11 python3.11-venv git -y

# Clone repository
git clone https://github.com/yourusername/file-rename-bot.git
cd file-rename-bot

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit with nano
nano .env

# Make main.py executable (optional)
chmod +x main.py

# Run the bot
python main.py
```

## Deployment Options

### Option 1: Render (Recommended - Easiest)

#### Prerequisites

- GitHub account
- Render account (free)
- All credentials ready

#### Steps

1. **Push Code to GitHub**

```bash
# Initialize git
git init
git add .
git commit -m "Initial commit"

# Create repository on GitHub
# Then:
git remote add origin https://github.com/yourusername/file-rename-bot.git
git branch -M main
git push -u origin main
```

2. **Connect to Render**

- Go to https://render.com
- Click "New +" button
- Select "Web Service"
- Connect your GitHub account
- Select your repository

3. **Configure Service**

- **Name**: file-rename-bot
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python main.py`

4. **Add Environment Variables**

- Click "Environment"
- Add each variable (copy from your .env):
  - API_ID
  - API_HASH
  - BOT_TOKEN
  - DB_URL
  - DATABASE_NAME
  - OWNER_ID
  - LOG_CHANNEL
  - FORCE_SUBS (optional)
  - START_PIC (optional)

5. **Deploy**

- Click "Create Web Service"
- Wait 2-3 minutes
- Check "Logs" tab for confirmation

Your bot is now live! Get the URL from Render dashboard.

### Option 2: Heroku

```bash
# Install Heroku CLI
# Windows: https://devcenter.heroku.com/articles/heroku-command-line
# macOS: brew tap heroku/brew && brew install heroku
# Linux: curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create your-app-name

# Add remote
git remote add heroku https://git.heroku.com/your-app-name.git

# Set environment variables
heroku config:set API_ID=123456
heroku config:set API_HASH=abc123
heroku config:set BOT_TOKEN=xxx
heroku config:set DB_URL=mongodb+srv://...
heroku config:set DATABASE_NAME=file_rename_bot
heroku config:set OWNER_ID=987654
heroku config:set LOG_CHANNEL=-100123456

# Deploy
git push heroku main

# Check logs
heroku logs --tail
```

### Option 3: Railway

1. Go to https://railway.app
2. Click "Create New Project"
3. Select "Deploy from GitHub"
4. Authorize and select repository
5. Add environment variables from .env
6. Deploy

### Option 4: Koyeb

1. Go to https://koyeb.com
2. Sign up
3. Create new app
4. Connect GitHub
5. Select repository and branch
6. Configure:
   - Builder: Dockerfile or Python buildpack
   - Environment variables: Add from .env
7. Deploy

## Post-Deployment Configuration

### Step 1: Verify Bot is Running

Send `/start` to your bot. It should respond with welcome message.

### Step 2: Create Log Channel

1. Create a private Telegram channel
2. Add bot as administrator
3. Get channel ID from @userinfobot
4. Update LOG_CHANNEL if needed
5. Bot will send all logs here

### Step 3: Set Up Admin Controls

```
Send these commands to bot:

/add_admin [user_id] - Add administrators
/addchnl [channel_username] - Setup force subscribe
/broadcast [message] - Test broadcasting
```

### Step 4: Test All Features

- `/autorename` - Set rename format
- `/viewthumb` - Upload thumbnail
- `/set_caption` - Set custom caption
- `/leaderboard` - Check leaderboard

## Testing

### Before Going Live

1. **Test rename functionality**
   - Set format: `/autorename S{season}E{episode} - {title}`
   - Send test video file
   - Verify it's renamed correctly

2. **Test admin commands**
   - Use `/add_admin [your_id]`
   - Try `/ban` and `/unban`
   - Test `/broadcast`

3. **Test force subscribe**
   - Add channel: `/addchnl mychannel`
   - Try accessing bot from non-subscribed account

4. **Check logs**
   - All actions should appear in log channel
   - Verify database is storing data

## Troubleshooting

### "ModuleNotFoundError: No module named 'pyrogram'"

**Solution**:
```bash
pip install -r requirements.txt
# or
pip install pyrogram==1.4.16
```

### "Can't find .env file"

**Solution**:
```bash
# Create it from example
cp .env.example .env
# Edit with values
nano .env  # or open in text editor
```

### "Invalid API_ID"

**Solution**:
- API_ID must be a number
- Get from https://my.telegram.org
- Check no spaces in value

### "Bot token invalid"

**Solution**:
- Get fresh token from @BotFather
- No extra spaces
- Check exact copy-paste

### "MongoDB connection refused"

**Solution**:
- Check internet connection
- Verify username/password in DB_URL
- Check IP whitelist in MongoDB Atlas
- Use correct connection string format

### "Bot doesn't respond"

**Solution**:
- Check bot token is correct
- Verify all environment variables
- Check logs for errors
- Restart the bot
- Verify internet connection

### "Database errors"

**Solution**:
- Check database is running
- Verify DB_URL
- Check user permissions
- Increase connection pool size if needed

## Next Steps

1. Customize bot behavior in `config.py`
2. Add more features by extending handlers
3. Set up custom messages and branding
4. Monitor bot performance
5. Regular database backups

## Getting Help

1. Check README.md for full documentation
2. Review logs in deployment platform
3. Check Telegram Bot API documentation
4. Visit Pyrogram documentation: https://docs.pyrogram.org
5. MongoDB documentation: https://docs.mongodb.com

## Security Checklist

- [ ] Never commit .env file to git
- [ ] Use strong MongoDB password
- [ ] Enable IP whitelist in MongoDB
- [ ] Use HTTPS for external APIs
- [ ] Keep dependencies updated
- [ ] Regular security audits
- [ ] Backup database regularly
- [ ] Monitor admin actions

Congratulations! Your bot is now installed and deployed! 🎉
