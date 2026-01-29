# Quick Reference Guide

**Cheat sheet for File Rename Bot**

---

## Environment Variables Needed

```env
API_ID=123456789                              # From https://my.telegram.org
API_HASH=abc123def456ghi789                   # From https://my.telegram.org
BOT_TOKEN=123456:ABC-DEF1234...               # From @BotFather
DB_URL=mongodb+srv://user:pass@cluster.net/   # From MongoDB Atlas
OWNER_ID=987654321                            # Your Telegram ID
LOG_CHANNEL=-1001234567890                    # Forward msg to @userinfobot
DATABASE_NAME=file_rename_bot                 # Optional (default shown)
FORCE_SUBS=channel1,channel2                  # Optional
START_PIC=https://example.com/image.jpg       # Optional
```

---

## File Locations

| File | Purpose | Lines |
|------|---------|-------|
| `main.py` | Start bot here | 93 |
| `config.py` | Edit messages/settings | 119 |
| `database.py` | Database operations | 335 |
| `handlers/*.py` | Bot command handlers | 1,764 |

---

## Installation

### Option 1: Render (Fastest - 5 minutes)

```bash
# Push to GitHub
git add . && git commit -m "init" && git push

# Go to https://render.com
# Create new Web Service
# Connect your GitHub repo
# Set environment variables
# Done! Bot is live
```

### Option 2: Local (Development)

```bash
# Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with credentials

# Run
python main.py
```

### Option 3: Heroku/Railway/Koyeb

See `DEPLOYMENT.md`

---

## Getting Credentials

### Telegram API
- Go: https://my.telegram.org
- Login → API development tools
- Get `API_ID` and `API_HASH`

### Bot Token
- Chat: @BotFather
- Command: `/newbot`
- Get `BOT_TOKEN`

### Your User ID
- Chat: @userinfobot
- Get your ID
- Set as `OWNER_ID`

### Log Channel
1. Create private channel
2. Add bot as admin
3. Send message
4. Forward to @userinfobot
5. Use Chat ID as `LOG_CHANNEL` (with -100 prefix)

### MongoDB
- Go: https://www.mongodb.com/cloud/atlas
- Create cluster
- Get connection string as `DB_URL`

---

## Most Used Commands

**For Users:**
```
/start          - Welcome
/autorename     - Set rename format
/showformat     - View format
/leaderboard    - Top users
```

**For Admins:**
```
/add_admin      - Add admin
/ban [id]       - Ban user
/broadcast      - Send message to all
/status         - Bot status
```

---

## Common Format Examples

```
S{season}E{episode} - {title}
{title} ({quality})
[{quality}] {title}
{title} - {season}x{episode}
{title} {quality}p
```

---

## File Structure Tree

```
file-rename-bot/
├── main.py                    ← Start bot here
├── config.py                  ← Edit messages here
├── database.py                ← Database code
├── utils.py                   ← Helper functions
├── handlers/                  ← Command handlers
│   ├── start_handler.py       /start, /help
│   ├── rename_handler.py      /autorename
│   ├── thumbnail_handler.py   /viewthumb
│   ├── caption_handler.py     /set_caption
│   ├── metadata_handler.py    /metadata
│   ├── user_handler.py        /leaderboard
│   └── admin_handler.py       /add_admin
├── requirements.txt           ← Dependencies
├── .env.example               ← Config template
├── Procfile                   ← Heroku config
├── render.yaml                ← Render config
└── Documentation/
    ├── README.md
    ├── QUICKSTART.md
    ├── INSTALLATION.md
    ├── DEPLOYMENT.md
    └── PROJECT_STRUCTURE.md
```

---

## Testing Checklist

- [ ] `/start` shows welcome message
- [ ] `/help` displays commands
- [ ] `/autorename` accepts format
- [ ] `/showformat` shows saved format
- [ ] Send video file - bot renames it
- [ ] `/viewthumb` works (upload one first)
- [ ] `/leaderboard` shows users
- [ ] `/add_admin [id]` (admin only)
- [ ] `/ban [id]` bans user (admin only)
- [ ] `/broadcast` sends to all (admin only)

---

## Deployment Checklist

- [ ] Got all 6 required credentials
- [ ] Created .env file with values
- [ ] Tested locally with `python main.py`
- [ ] Pushed code to GitHub
- [ ] Created log channel (got LOG_CHANNEL ID)
- [ ] Deployed to Render/Heroku
- [ ] Added environment variables to platform
- [ ] Bot responds to /start
- [ ] Tested file rename
- [ ] Verified logs in log channel

---

## Troubleshooting Quick Fixes

| Issue | Solution |
|-------|----------|
| "Invalid API_ID" | API_ID must be a NUMBER, not string |
| "Token invalid" | Get fresh token from @BotFather |
| "Bot not running" | Check internet, verify BOT_TOKEN |
| "DB connection error" | Check DB_URL, add IP to MongoDB |
| "File rename not working" | Set format first with /autorename |
| "Slow response" | Upgrade deployment plan |
| "Memory error" | Delete old logs, restart bot |

---

## Key Database Collections

| Collection | Stores | Key Fields |
|------------|--------|-----------|
| users | User profiles | user_id, username, rename_count |
| thumbnails | User images | user_id, file_id |
| rename_formats | User formats | user_id, format |
| affixes | Prefix/suffix | user_id, prefix, suffix |
| captions | Custom text | user_id, caption |
| admins | Admin list | user_id |
| force_sub_channels | Required channels | username |
| sequences | Batch files | user_id, files |
| metadata | Title/author | user_id, title, author |

---

## Important Paths

```
Environment Variables: .env
Example Template: .env.example
Main Code: main.py
Database Code: database.py
Handlers: handlers/ folder
Logs: Check Render/Heroku dashboard
```

---

## Python Version

Must use: **Python 3.11+**

Check:
```bash
python --version
```

---

## Dependencies

All in `requirements.txt`:
- pyrogram==1.4.16 (Telegram API)
- pymongo==4.6.0 (MongoDB)
- TgCrypto==1.2.5 (Encryption)
- python-dotenv==1.0.0 (Environment)
- requests==2.31.0 (HTTP)
- Pillow==10.1.0 (Images)

Install:
```bash
pip install -r requirements.txt
```

---

## Important URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Telegram API | https://my.telegram.org | Get API credentials |
| BotFather | @BotFather | Create bot |
| MongoDB | https://mongodb.com/cloud/atlas | Database |
| Render | https://render.com | Deployment |
| Heroku | https://heroku.com | Deployment |
| Railway | https://railway.app | Deployment |

---

## Commands by Category

### Basic (4)
- /start, /help, /ping, /donate

### Rename (3)
- /autorename, /showformat, /setmedia

### Sequence (2)
- /start_sequence, /end_sequence

### Thumbnail (2)
- /viewthumb, /delthumb

### Caption (3)
- /set_caption, /see_caption, /del_caption

### Metadata (4)
- /set_prefix, /see_prefix, /del_prefix
- /set_suffix, /see_suffix, /del_suffix
- /metadata

### User (3)
- /tutorial, /leaderboard, /status

### Admin (16)
- /add_admin, /deladmin, /admins
- /ban, /unban, /banned
- /addchnl, /delchnl, /listchnl
- /broadcast, /restart

**Total: 38 commands**

---

## Format Variables

Use in `/autorename`:
- `{season}` = Season number
- `{episode}` = Episode number
- `{title}` = Original filename
- `{quality}` = Video quality
- `{audio}` = Audio codec

Example: `S{season}E{episode} - {title}` → `S01E01 - MyVideo`

---

## MongoDB Indexes

Add for performance:
```python
db.users.create_index("user_id")
db.thumbnails.create_index("user_id")
db.rename_formats.create_index("user_id")
db.admins.create_index("user_id")
```

---

## Useful Telegram Bots

- @BotFather - Create/manage bots
- @userinfobot - Get user/chat IDs
- @RawDataBot - Debug bot data

---

## Support Resources

- **Pyrogram Docs**: https://docs.pyrogram.org
- **MongoDB Docs**: https://docs.mongodb.com
- **Telegram Bot API**: https://core.telegram.org/bots
- **Python Docs**: https://docs.python.org

---

## Quick Start (TL;DR)

```bash
# 1. Clone
git clone https://github.com/yourusername/file-rename-bot.git
cd file-rename-bot

# 2. Setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 3. Configure
cp .env.example .env
# Edit .env with your credentials

# 4. Test
python main.py
# Send /start to bot

# 5. Deploy
# Push to GitHub, go to Render, deploy
```

---

## Remember

✅ Never commit `.env` file
✅ Keep `BOT_TOKEN` secret
✅ API_ID must be a number
✅ Add IP to MongoDB whitelist
✅ Create log channel before testing
✅ Python 3.11+ required
✅ All credentials are required

---

## Version Info

- **Bot Version**: 1.0
- **Python**: 3.11.5+
- **Pyrogram**: 1.4.16
- **MongoDB**: 4.6.0+
- **Status**: Production Ready

---

**Need more help?**
- QUICKSTART.md - 5-minute setup
- README.md - Full documentation
- INSTALLATION.md - Detailed guide
- DEPLOYMENT.md - Platform-specific

Happy botting! 🚀
