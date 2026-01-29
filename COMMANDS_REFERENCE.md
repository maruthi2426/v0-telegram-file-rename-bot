# Telegram Bot Commands Reference

## User Commands

### File Management
- `/start` - Start the bot and see welcome message
- `/help` - Show all available commands
- `/autorename [format]` - Set custom rename format
  - Example: `/autorename S{season}E{episode} - {title}`
- `/showformat` - View your current rename format
- `/setmedia [type]` - Set output file type (document/video)

### Thumbnail Management
- `/viewthumb` - Show your current thumbnail
- `/delthumb` - Delete your thumbnail

### Caption Management
- `/set_caption [text]` - Set custom caption for files
  - Supports Markdown formatting: **bold**, *italic*, `code`
- `/see_caption` - View your current caption
- `/del_caption` - Delete your caption

### File Metadata
- `/metadata` - View file metadata and information
- `/start_sequence [name]` - Start file sequence mode
- `/end_sequence` - End file sequence mode
- `/setmedia [type]` - Set file output type

### Affixes (Prefix/Suffix)
- `/set_prefix [text]` - Add prefix to renamed files
- `/see_prefix` - View current prefix
- `/del_prefix` - Delete prefix
- `/set_suffix [text]` - Add suffix to renamed files
- `/see_suffix` - View current suffix
- `/del_suffix` - Delete suffix

### Statistics & Info
- `/leaderboard` - View top users by rename count
- `/ping` - Check bot response time
- `/donate` - See donation information
- `/tutorial` - View usage tutorial

---

## Admin Commands

### User Management
- `/users` - Show all registered users
- `/ban_user [user_id]` - Ban a user from using bot
- `/unban_user [user_id]` - Unban a user
- `/user_info [user_id]` - Get detailed user information

### Broadcasting & Notifications
- `/broadcast [message]` - Send message to all users
- `/notice [message]` - Send important notice
- `/stats` - Show bot statistics
- `/logs` - View recent activity logs

### Bot Management
- `/status` - Check bot status
- `/restart` - Restart bot service
- `/shutdown` - Shutdown bot (careful!)

### Database Operations
- `/backup` - Create database backup
- `/clear_logs` - Clear activity logs
- `/export_users` - Export user list

---

## Rename Format Variables

Use these in `/autorename` command:

| Variable | Description | Example |
|----------|-------------|---------|
| `{season}` | Season number | `S01` |
| `{episode}` | Episode number | `E05` |
| `{title}` | File title | `Episode Name` |
| `{quality}` | Video quality | `720p`, `1080p` |
| `{audio}` | Audio track | `HINDI`, `ENGLISH` |
| `{date}` | Current date | `2024-01-15` |
| `{time}` | Current time | `14:30:45` |

### Example Rename Formats

```
S{season}E{episode} - {title}
[{quality}] {title} [{audio}]
{date} - {title}
Episode {episode} - {title} [{quality}]
{title} [REMASTERED]
```

---

## Markdown Formatting in Captions

Use these in `/set_caption`:

| Syntax | Result |
|--------|--------|
| `**text**` | **Bold** |
| `*text*` | *Italic* |
| `__text__` | __Underline__ |
| `` `text` `` | `Code` |
| `[text](url)` | [Link](url) |
| `\n` | Line break |

### Example Caption

```
**File Details:**
Quality: *{quality}*
Audio: **{audio}**
Date: `{date}`
```

---

## User Statistics

What data is tracked:

- Total files renamed
- Thumbnails uploaded
- Captions created
- Affixes added
- Last activity time
- Join date
- Ban status

View with: `/leaderboard`

---

## Admin Statistics

Track with `/stats`:

- Total users
- Active users (24h)
- Total renames done
- Files processed
- Database size
- Bot uptime

---

## Setting Up Custom Rename

### Step 1: Send Format
```
/autorename S{season}E{episode} - {title}
```

### Step 2: Confirm
Bot will confirm format is saved

### Step 3: Use It
Send a file and it will be renamed using your format

### Step 4: Check
```
/showformat
```
Bot shows your current format

---

## Setting Up Caption

### Step 1: Create Caption
```
/set_caption 📁 **{title}** [{quality}] - Enjoy!
```

### Step 2: Confirm
Bot confirms caption saved

### Step 3: Use It
Send a file and caption will be added

### Step 4: View
```
/see_caption
```
Bot shows your current caption

---

## Setting Up Thumbnail

### Step 1: Send Image
Send a photo or image file (will be used as thumbnail)

### Step 2: Set Thumbnail
```
/set_thumbnail
```
(Or just send image and reply with /setthumb)

### Step 3: View
```
/viewthumb
```
See your thumbnail image

### Step 4: Delete (if needed)
```
/delthumb
```
Remove current thumbnail

---

## Batch Processing

For processing multiple files:

1. Turn ON batch mode: `/start_sequence my_series`
2. Send multiple files
3. Turn OFF: `/end_sequence`
4. All will be renamed with sequence

---

## Error Messages & Solutions

| Error | Solution |
|-------|----------|
| "Format not set" | Run `/autorename` to set format |
| "No caption" | Run `/set_caption` to add caption |
| "User banned" | Admin will need to `/unban_user` |
| "DB connection error" | Wait and try again |
| "Invalid file type" | Send supported file type |

---

## Command Examples

### Example 1: Simple Rename
```
User: /autorename Episode {episode} - {title}
Bot: Format saved!
User: [Sends file]
Bot: [Renames to: Episode 5 - Final Battle]
```

### Example 2: With Prefix/Suffix
```
User: /set_prefix [SERIES NAME]
Bot: Prefix set!
User: /set_suffix [REMASTERED]
Bot: Suffix set!
User: [Sends file named "Episode 1"]
Bot: [Renames to: [SERIES NAME] Episode 1 [REMASTERED]]
```

### Example 3: With Thumbnail
```
User: [Sends thumbnail image]
User: /viewthumb
Bot: [Shows your thumbnail]
User: [Sends file to process]
Bot: [Applies thumbnail to file]
```

### Example 4: Broadcast (Admin)
```
Admin: /broadcast 🎉 New feature available! Use /help
Bot: Sends message to all users
```

---

## Pro Tips

1. **Save commonly used formats:**
   ```
   /autorename S{season}E{episode} - {title}
   /set_caption Download from @YourChannel
   ```

2. **Use affixes creatively:**
   - Prefix for series name
   - Suffix for quality or resolution

3. **Batch processing:**
   - Start with `/start_sequence series_name`
   - Send multiple files
   - End with `/end_sequence`

4. **Check your data:**
   - `/leaderboard` - See where you rank
   - `/showformat` - Confirm your format
   - `/metadata` - Check file details

5. **For admins:**
   - `/stats` - Monitor bot health
   - `/users` - Track user base
   - `/broadcast` - Make announcements

---

## Quick Command Cheat Sheet

```
FILE MANAGEMENT:
  /start          - Start bot
  /help           - Help menu
  /autorename     - Set rename format
  /showformat     - View format

THUMBNAILS:
  /viewthumb      - See thumbnail
  /delthumb       - Delete thumbnail

CAPTIONS:
  /set_caption    - Add caption
  /see_caption    - View caption
  /del_caption    - Delete caption

STATS:
  /leaderboard    - Rankings
  /ping           - Bot status
  /metadata       - File info

AFFIXES:
  /set_prefix     - Add prefix
  /del_prefix     - Remove prefix
  /set_suffix     - Add suffix
  /del_suffix     - Remove suffix

ADMIN:
  /users          - User list
  /stats          - Bot stats
  /broadcast      - Send to all
  /ban_user       - Ban user
  /unban_user     - Unban user
```

---

## Need Help?

- Send `/help` in Telegram
- Send `/tutorial` for walkthrough
- Contact: @Admin or bot support

Enjoy renaming your files! 🎉
