# Project Structure & Architecture

Complete guide to understanding the File Rename Bot codebase.

## Directory Tree

```
file-rename-bot/
├── main.py                      # Bot entry point
├── config.py                    # Configuration and constants
├── database.py                  # MongoDB operations
├── utils.py                     # Utility functions
│
├── handlers/                    # Command handlers
│   ├── __init__.py
│   ├── start_handler.py         # /start, /help, /ping, /donate
│   ├── rename_handler.py        # /autorename, /showformat, file rename
│   ├── thumbnail_handler.py     # /viewthumb, /delthumb, thumbnail upload
│   ├── caption_handler.py       # /set_caption, /see_caption, /del_caption
│   ├── metadata_handler.py      # /metadata, prefix, suffix handling
│   ├── user_handler.py          # /leaderboard, /tutorial, /status
│   └── admin_handler.py         # Admin commands
│
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore patterns
│
├── Deployment Files
├── Procfile                     # Heroku deployment
├── runtime.txt                  # Python version
├── render.yaml                  # Render deployment
│
└── Documentation
    ├── README.md                # Main documentation
    ├── QUICKSTART.md            # Quick start guide
    ├── INSTALLATION.md          # Detailed installation
    └── PROJECT_STRUCTURE.md     # This file
```

## Core Files Explained

### main.py

**Purpose**: Bot initialization and startup

**Key Functions**:
- `app` - Pyrogram Client instance
- `set_commands()` - Registers bot commands in Telegram UI
- `main()` - Startup function that initializes database and starts bot

**Imports All Handlers**: When main.py starts, it automatically imports all handlers which register their command listeners.

### config.py

**Purpose**: Centralized configuration management

**Contains**:
- Environment variable loading
- Bot settings (file sizes, extensions)
- Message templates (START_MESSAGE, HELP_MESSAGE, etc.)
- Constants (thumbnail dimensions, allowed extensions)

**Usage**:
```python
from config import OWNER_ID, BOT_TOKEN, FORCE_SUBS
```

### database.py

**Purpose**: MongoDB database operations

**Main Class**: `Database`

**Key Collections**:
- `users` - User information and statistics
- `thumbnails` - User thumbnail files
- `captions` - Custom captions
- `rename_formats` - Rename format settings
- `affixes` - Prefixes and suffixes
- `metadata` - User metadata
- `force_sub_channels` - Force subscribe channels
- `admins` - Administrator list
- `sequences` - Active file sequences

**Usage**:
```python
from database import db

# Add user
db.add_user(user_id, username, first_name)

# Set thumbnail
db.set_thumbnail(user_id, file_id, file_unique_id)

# Increment counter
db.increment_rename_count(user_id)
```

### utils.py

**Purpose**: Reusable utility functions

**Key Functions**:

| Function | Purpose |
|----------|---------|
| `send_log()` | Send log messages to admin channel |
| `is_admin()` | Check if user is admin |
| `check_user_ban()` | Check if user is banned |
| `sanitize_filename()` | Clean filename for file system |
| `parse_rename_format()` | Parse format string with variables |
| `format_bytes()` | Convert bytes to readable format |
| `create_leaderboard_text()` | Generate leaderboard display |

**Usage**:
```python
from utils import sanitize_filename, send_log, is_admin

new_name = sanitize_filename(name)
await send_log(app, "User action", user_id)
if await is_admin(app, user_id):
    # Admin action
```

## Handlers Explained

### start_handler.py

**Handles**: `/start`, `/help`, `/ping`, `/donate` commands

**Callbacks**: Help, tutorial, about, back home buttons

**Key Features**:
- Welcome message with inline buttons
- Help text display
- Tutorial guide
- Bot status check

**State Management**: Uses inline buttons to navigate between different help sections

### rename_handler.py

**Handles**: `/autorename`, `/showformat`, `/setmedia`, `/start_sequence`, `/end_sequence`

**File Processing**: 
- Accepts video/document files
- Applies user's custom format
- Adds prefix/suffix if set
- Sends renamed file back

**State Management**: 
- `rename_formats` dict stores users waiting for format input
- Tracks sequence mode state in database

**Example Flow**:
1. User sends `/autorename`
2. Bot waits for format string
3. User sends format: `S{season}E{episode}`
4. Format saved to database
5. User sends video file
6. Bot parses format and renames file

### thumbnail_handler.py

**Handles**: `/viewthumb`, `/delthumb`, thumbnail upload

**State Management**: `thumbnail_states` dict tracks upload requests

**Workflow**:
1. User sends `/viewthumb`
2. Bot displays current thumbnail or prompt to upload
3. User sends photo
4. Bot stores in database and uses for all files

### caption_handler.py

**Handles**: `/set_caption`, `/see_caption`, `/del_caption`

**State Management**: `caption_states` dict tracks caption input

**Features**:
- Supports Markdown formatting
- Stores custom captions per user
- Shows preview before saving

### metadata_handler.py

**Handles**: 
- Prefix/suffix: `/set_prefix`, `/see_prefix`, `/del_prefix`, `/set_suffix`, `/see_suffix`, `/del_suffix`
- Metadata: `/metadata` for title, author management

**State Management**: `metadata_states` dict tracks all metadata operations

**Database Collections Used**:
- `affixes` - Prefixes and suffixes
- `metadata` - Title and author

### user_handler.py

**Handles**: `/leaderboard`, `/tutorial`, `/status`

**Features**:
- Displays top 10 users by rename count
- Shows user's rank and statistics
- Tutorial with usage examples
- Bot status information

**Callback Handlers**: 
- Refresh leaderboard
- Navigate between sections

### admin_handler.py

**Handles**: All admin commands

**Commands**:
- `/add_admin`, `/deladmin`, `/admins` - Admin management
- `/ban`, `/unban`, `/banned` - User banning
- `/addchnl`, `/delchnl`, `/listchnl` - Force subscribe channels
- `/broadcast` - Message broadcasting
- `/restart` - Bot restart

**State Management**: `admin_states` dict tracks admin actions

**Security**: All commands check `is_admin()` before executing

**Broadcast Logic**:
1. Collects all users from leaderboard
2. Sends message to each user
3. Reports success/failure count

## Database Schema

### users Collection

```json
{
  "_id": ObjectId,
  "user_id": 123456789,
  "username": "john_doe",
  "first_name": "John",
  "joined_date": "2024-01-15T10:30:00Z",
  "rename_count": 45,
  "is_banned": false
}
```

### thumbnails Collection

```json
{
  "_id": ObjectId,
  "user_id": 123456789,
  "file_id": "AgAC...",
  "file_unique_id": "AQAD...",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### rename_formats Collection

```json
{
  "_id": ObjectId,
  "user_id": 123456789,
  "format": "S{season}E{episode} - {title}",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### affixes Collection

```json
{
  "_id": ObjectId,
  "user_id": 123456789,
  "prefix": "[HD]",
  "suffix": "[1080p]"
}
```

### sequences Collection

```json
{
  "_id": ObjectId,
  "user_id": 123456789,
  "is_active": true,
  "files": [
    { "original_name": "file1.mp4", "new_name": "S01E01.mp4" },
    { "original_name": "file2.mp4", "new_name": "S01E02.mp4" }
  ],
  "started_at": "2024-01-15T10:30:00Z"
}
```

## Data Flow Diagrams

### File Rename Process

```
User sends file
    ↓
Get user's rename format (database)
    ↓
Get prefix/suffix (database)
    ↓
Parse format with variables
    ↓
Sanitize filename
    ↓
Increment rename counter
    ↓
Send renamed file back
    ↓
Log action
```

### Thumbnail Upload Process

```
User sends /viewthumb
    ↓
Check if thumbnail exists
    ├─ YES → Display with options
    └─ NO → Prompt for upload
    ↓
User sends photo
    ↓
Extract file_id and file_unique_id
    ↓
Store in database
    ↓
Use for all future file operations
```

### Admin Broadcast Process

```
Admin sends /broadcast
    ↓
Bot waits for message
    ↓
Admin sends message
    ↓
Fetch all users from database
    ↓
Send message to each user (async)
    ↓
Count successes/failures
    ↓
Report results to admin
    ↓
Log broadcast action
```

## State Management

### In-Memory States

Some operations require temporary state:

```python
# In rename_handler.py
rename_formats = {
    user_id: {
        "state": "waiting_format",
        "msg_id": message_id
    }
}

# In thumbnail_handler.py
thumbnail_states = {
    user_id: {
        "action": "waiting_thumb"
    }
}

# In admin_handler.py
admin_states = {
    user_id: {
        "action": "waiting_admin_id"
    }
}
```

These are cleared after the operation completes.

## Environment Variables

**Required:**
```
API_ID          - Telegram API ID
API_HASH        - Telegram API Hash
BOT_TOKEN       - Bot token from @BotFather
DB_URL          - MongoDB connection string
OWNER_ID        - Owner's Telegram user ID
LOG_CHANNEL     - Log channel ID (with -100 prefix)
```

**Optional:**
```
DATABASE_NAME   - MongoDB database name (default: file_rename_bot)
FORCE_SUBS      - Force subscribe channels (comma-separated)
START_PIC       - Custom start image URL
```

## Dependencies

From `requirements.txt`:

| Package | Version | Purpose |
|---------|---------|---------|
| pyrogram | 1.4.16 | Telegram Bot API |
| TgCrypto | 1.2.5 | Telegram encryption |
| pymongo | 4.6.0 | MongoDB driver |
| python-dotenv | 1.0.0 | Environment variables |
| requests | 2.31.0 | HTTP requests |
| Pillow | 10.1.0 | Image processing |

## Deployment Considerations

### Render
- Free tier available
- Auto-deploys from GitHub
- Environment variables via UI
- Logs accessible in dashboard

### Heroku
- Requires Procfile (provided)
- Requires runtime.txt (provided)
- CLI deployment via `git push heroku main`
- Environment via `heroku config:set`

### Railway/Koyeb
- Similar to Render
- GitHub integration
- Web UI for environment variables

## Scaling Considerations

### Database
- Add indexes to frequently queried fields
- Consider partitioning if users exceed 100k
- Archive old logs periodically

### Bot Performance
- Implement request throttling
- Use connection pooling
- Optimize image processing

### Infrastructure
- Use load balancer for multiple instances
- Redis for caching frequently accessed data
- CDN for image delivery

## Security Best Practices

1. **Never commit .env** - Use .env.example instead
2. **Validate all inputs** - Use sanitization functions
3. **Rate limiting** - Prevent abuse
4. **Admin verification** - Check `is_admin()` before sensitive operations
5. **Secure credentials** - Use environment variables only
6. **Log sensitive actions** - Keep audit trail
7. **User privacy** - Don't expose user data
8. **Database security** - Use strong passwords, IP whitelisting

## Performance Tips

1. Use database indexes on frequently queried fields
2. Cache leaderboard data (update periodically, not on every request)
3. Batch database operations when possible
4. Optimize image processing (resize, compress)
5. Use connection pooling for MongoDB
6. Implement request timeouts
7. Monitor memory usage for file operations

## Testing the Bot

### Manual Testing

```python
# Test each command manually
/start              # Should show welcome
/autorename         # Should ask for format
S{season}E{episode} # Should save format
/showformat         # Should display format
[Send video file]   # Should rename and send back
/leaderboard        # Should show top users
```

### Error Testing

```python
# Test error handling
Send invalid file
Send empty message
Ban user and try command
Set invalid database URL
Send oversized file
```

## Future Enhancement Ideas

1. **Image Recognition** - Auto-detect season/episode from file
2. **Batch Processing** - Queue for processing large files
3. **Video Preview** - Generate thumbnails from video
4. **Advanced Filtering** - Filter leaderboard by date range
5. **Scheduled Tasks** - Daily digests, cleanup tasks
6. **Webhooks** - External integration support
7. **Analytics** - Detailed usage statistics
8. **API** - RESTful API for external clients
9. **Web Dashboard** - Monitor bot statistics
10. **Multi-language** - Support for multiple languages

## Debugging Tips

### Enable Detailed Logging

Edit main.py:
```python
logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Check Logs

```bash
# Local
python main.py > logs.txt 2>&1

# Render
View in dashboard Logs tab

# Heroku
heroku logs --tail
```

### Test Database Connection

```python
from database import db
db.connect()
test_user = db.get_user(123456)
print(test_user)
```

## Conclusion

The bot is modular and extensible. Each handler manages its own commands, and the database layer provides clean abstraction. Follow the existing patterns when adding new features.

For questions or contributions, refer to README.md and open issues on GitHub.
