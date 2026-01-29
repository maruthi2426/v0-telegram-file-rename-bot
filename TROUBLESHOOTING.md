# Troubleshooting Guide

## Error: "This action is not allowed" on Render Deploy

### What Causes This Error?
This error typically occurs when:
1. **Missing environment variables** - Required vars not set in Render
2. **Incorrect environment variable names** - Using wrong var names
3. **Database connection fails** - MongoDB connection string is invalid
4. **Code execution errors** - Syntax or runtime errors in the code

### Solution Checklist

#### Step 1: Verify Environment Variables in Render
Go to your Render dashboard and check the Environment section. Ensure these variables are set:

**REQUIRED Variables:**
- `API_ID` - Your Telegram API ID
- `API_HASH` - Your Telegram API Hash
- `BOT_TOKEN` - Your Telegram Bot Token
- `DATABASE_URL` - MongoDB connection string (with auth)
- `OWNER_ID` - Your Telegram user ID

**OPTIONAL Variables:**
- `LOG_CHANNEL` - Channel ID for logs
- `ADMIN_IDS` - Comma-separated admin IDs
- `DATABASE_NAME` - Database name (default: file_rename_bot)

#### Step 2: Verify MongoDB Connection String

Your `DATABASE_URL` should look like:
```
mongodb+srv://username:password@cluster.mongodb.net/?appName=Cluster0
```

**Make sure:**
- Username and password are correct
- No special characters in password (URL encode if needed)
- Database cluster is accessible from Render (check MongoDB network settings)
- `appName` parameter is present

#### Step 3: Check Code Compatibility

The bot code has been updated to:
- ✅ Handle missing environment variables gracefully
- ✅ Support both `DATABASE_URL` and `DB_URL`
- ✅ Validate connections before starting
- ✅ Log detailed startup information
- ✅ Handle Render-specific requirements

#### Step 4: Deploy with Updated Code

1. Commit the updated code to your GitHub repository
   ```bash
   git add .
   git commit -m "Fix: Render deployment compatibility"
   git push
   ```

2. In Render dashboard:
   - Click the deploy button
   - Wait 2-3 minutes for build to complete
   - Check logs (click "Logs" tab)

#### Step 5: Read Deployment Logs

In Render dashboard, go to the "Logs" tab and look for:

**Success indicators:**
```
All required environment variables validated
TELEGRAM FILE RENAME BOT - RENDER DEPLOYMENT
Connected to MongoDB successfully
Bot client started successfully
BOT IS RUNNING AND READY
```

**Error indicators:**
```
MISSING REQUIRED ENVIRONMENT VARIABLES
Failed to connect to MongoDB
MongoDB Connection Failure
```

---

## Common Issues and Fixes

### Issue 1: "Missing required environment variables"
**Solution:**
1. Check spelling (case-sensitive)
2. Ensure no leading/trailing spaces
3. All 5 required variables must be set
4. Don't use quotes in the value

### Issue 2: "Failed to connect to MongoDB"
**Solutions:**
- Verify connection string is complete
- Check MongoDB credentials are correct
- Ensure whitelist includes Render's IP (or use 0.0.0.0/0)
- Test connection string locally first

### Issue 3: "Bot is starting but no response"
**Solutions:**
- Check if bot token is correct
- Verify API ID and API Hash are correct
- Wait 5-10 minutes (bot might be initializing)
- Check logs for errors

### Issue 4: "Service crashes immediately"
**Solutions:**
- Check build command: `pip install -r requirements.txt`
- Verify start command: `python main.py`
- Check logs for Python syntax errors
- Ensure all imports are valid

---

## Debugging Steps

### 1. Check Build Logs
In Render dashboard:
1. Go to "Logs" tab
2. Look for "Build started" section
3. Check for `pip install` errors
4. Look for any Python import errors

### 2. Check Runtime Logs
In Render dashboard:
1. Go to "Logs" tab
2. Look for "Build succeeded" section
3. Watch for startup messages
4. Look for connection errors

### 3. Local Testing
Before deploying to Render, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your actual credentials

# Run the bot
python main.py
```

You should see:
```
All required environment variables validated
TELEGRAM FILE RENAME BOT - RENDER DEPLOYMENT
Testing MongoDB connection with ping...
Connected to MongoDB successfully
Bot client started successfully
BOT IS RUNNING AND READY
```

---

## MongoDB IP Whitelist Configuration

If you get MongoDB connection errors:

1. Go to MongoDB Atlas dashboard
2. Click "Network Access" (left sidebar)
3. Add a new IP address entry:
   - IP: `0.0.0.0/0` (allows all IPs - for development)
   - Or specific Render IP: Check Render docs for static IPs

---

## Getting Help

If issues persist:

1. **Check logs carefully** - Most errors are in the logs
2. **Verify all env vars** - Re-check each one
3. **Test locally first** - Isolate if it's code or deployment issue
4. **Check MongoDB** - Ensure it's running and accessible
5. **Review recent changes** - If it worked before, what changed?

---

## Successful Deployment Checklist

✅ All 5 required environment variables set in Render
✅ Environment variable names are correct (case-sensitive)
✅ MongoDB connection string is complete and valid
✅ MongoDB allows connections from Render
✅ Code is committed to GitHub
✅ Build completes without errors
✅ Logs show "BOT IS RUNNING AND READY"
✅ Bot responds to /start command

---

## Still Not Working?

If you've checked everything and it still doesn't work:

1. **Redeploy** - Click "Deploy" button again
2. **Restart service** - In Render dashboard, click "Restart"
3. **Check bot token** - Make sure you didn't copy extra characters
4. **Clear old builds** - Render might have cached an old build
5. **Create new service** - Start fresh deployment if all else fails

Remember: Most deployment issues are environment variable related. Double-check them first!
