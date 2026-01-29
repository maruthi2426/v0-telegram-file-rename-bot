# Quick Start Guide

Get your File Rename Bot running in 5 minutes!

## Prerequisites

- Python 3.11+ installed
- Telegram account
- MongoDB Atlas free account

## Step 1: Get Your Credentials (3 minutes)

### Telegram API Credentials

1. Open https://my.telegram.org/auth
2. Login with your phone number
3. Click "API development tools"
4. Copy your **API_ID** and **API_HASH**

### Bot Token

1. Open @BotFather in Telegram
2. Send `/newbot`
3. Follow the prompts
4. Copy your **BOT_TOKEN**

### Your User ID

1. Send `/start` to your bot (we'll create it)
2. Check the logs to find your **User ID** (or send message to @userinfobot)

## Step 2: MongoDB Setup (2 minutes)

1. Go to https://www.mongodb.com/cloud/atlas
2. Create free account
3. Create a cluster
4. Click "Connect" → "Drivers"
5. Copy your connection string as **DB_URL**

Replace `<username>`, `<password>` with your credentials

## Step 3: Deploy to Render (5 minutes) - Fastest

### Via Render

1. **Create Render Account**
   - Go to https://render.com
   - Sign up (free tier available)

2. **Connect GitHub**
   - Click "GitHub" when prompted
   - Authorize Render to access your repos

3. **Deploy This Bot**
   ```bash
   # First, push this code to GitHub
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/file-rename-bot.git
   git branch -M main
   git push -u origin main
   ```

4. **Create Render Service**
   - Go to https://render.com/dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Fill in:
     - **Name**: file-rename-bot
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python main.py`

5. **Set Environment Variables**
   - In Render dashboard, click "Environment"
   - Add each variable:
     ```
     API_ID = 123456789
     API_HASH = your_api_hash_here
     BOT_TOKEN = your_bot_token_here
     DB_URL = mongodb+srv://user:pass@cluster.mongodb.net/
     DATABASE_NAME = file_rename_bot
     OWNER_ID = your_user_id
     LOG_CHANNEL = -1001234567890
     ```

6. **Create Log Channel**
   - In Telegram, create a new private channel
   - Add bot as admin
   - Send a test message
   - Forward to @userinfobot to get ID (with -100)
   - Update LOG_CHANNEL

7. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes for deployment
   - Your bot is now live!

## OR: Run Locally (Development)

```bash
# Clone repository
git clone https://github.com/yourusername/file-rename-bot.git
cd file-rename-bot

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use any text editor

# Run the bot
python main.py
```

## Testing Your Bot

1. **Start the bot**
   - Send `/start` to your bot
   - Should see welcome message

2. **Test basic commands**
   ```
   /ping → Should respond "Pong! Bot is running smoothly!"
   /help → Shows all commands
   /autorename → Set custom rename format
   /leaderboard → View top users
   ```

3. **Test file rename**
   - Set format: `/autorename` → `S{season}E{episode} - {title}`
   - Send a video file
   - Bot sends it back renamed

## Deploying to Other Platforms

### Heroku
```bash
heroku login
heroku create your-app-name
git push heroku main
# Set environment variables in Heroku dashboard
```

### Railway
1. Go to https://railway.app
2. Create new project
3. Connect GitHub repo
4. Add environment variables
5. Deploy

### Koyeb
1. Go to https://koyeb.com
2. Create new app
3. Connect GitHub
4. Set environment variables
5. Deploy

## Common Issues & Solutions

### "API_ID is invalid"
- Check API_ID is a NUMBER, not a string
- Verify from https://my.telegram.org/

### "Bot token invalid"
- Get fresh token from @BotFather
- Ensure no extra spaces in .env

### "MongoDB connection error"
- Check DB_URL spelling
- Verify IP whitelist in MongoDB Atlas
- Check user password is URL-encoded

### "Bot not responding"
- Check logs in deployment platform
- Verify environment variables are set
- Restart the bot

### "File rename not working"
- Set rename format first: `/autorename`
- Check bot has permissions
- Verify file format is supported

## Useful Telegram Commands for Setup

- **@BotFather** - Create/manage bots
- **@userinfobot** - Get your User ID
- **@RawDataBot** - Debug Telegram data

## API Variables Explained

| Variable | Where to Get | Example |
|----------|-------------|---------|
| API_ID | https://my.telegram.org | 123456789 |
| API_HASH | https://my.telegram.org | abc123def456ghi789 |
| BOT_TOKEN | @BotFather | 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11 |
| DB_URL | MongoDB Atlas | mongodb+srv://user:pass@cluster.mongodb.net/ |
| OWNER_ID | @userinfobot | 987654321 |
| LOG_CHANNEL | Forward message to @userinfobot | -1001234567890 |

## Next Steps

1. **Customize bot** - Edit `config.py` for custom messages
2. **Add features** - Extend handlers for more functionality
3. **Manage admins** - Use `/add_admin` to add administrators
4. **Setup force sub** - Use `/addchnl` to require channel joins

## Need Help?

1. Check [README.md](README.md) for detailed documentation
2. Review logs in your deployment platform
3. Check if environment variables are correctly set
4. Verify all credentials are from correct sources

## Success Checklist

- [ ] Created Telegram bot with @BotFather
- [ ] Got API_ID and API_HASH from https://my.telegram.org
- [ ] Created MongoDB Atlas cluster and got DB_URL
- [ ] Got your User ID
- [ ] Created log channel and got LOG_CHANNEL ID
- [ ] Set all environment variables
- [ ] Deployed to Render (or local server)
- [ ] Bot responds to `/start`
- [ ] Can set rename format with `/autorename`
- [ ] Can rename test video file

Once all checked, your bot is ready to use! 🎉
