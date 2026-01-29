# File Rename & Thumbnail Bot

A powerful Telegram bot for renaming video files with custom formats and adding thumbnails. Built with Pyrogram and MongoDB.

## Features

- **Fast File Renaming**: Rename files according to custom formats instantly
- **Thumbnail Support**: Set custom thumbnails for your renamed files
- **Custom Captions**: Add personalized captions to every file
- **Sequence Mode**: Rename multiple files at once in perfect order
- **Prefix/Suffix Support**: Add custom prefixes and suffixes to filenames
- **Leaderboard System**: Built-in leaderboard to track top users
- **Force Subscribe**: Require users to join channels before using the bot
- **User Management**: Ban/unban users, manage admins
- **Broadcasting**: Send messages to all users at once
- **Metadata Management**: Store and manage file metadata
- **Secure**: All sensitive data loaded from environment variables
- **Admin Controls**: Full control panel for bot management

## Tech Stack

- **Framework**: Pyrogram (Telegram Bot API)
- **Database**: MongoDB
- **Language**: Python 3.11+
- **Deployment**: Render, Heroku, Railway, Koyeb

## Project Structure

```
file-rename-bot/
├── main.py                 # Main bot entry point
├── config.py              # Configuration and constants
├── database.py            # MongoDB database operations
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── Procfile               # Deployment configuration
├── render.yaml            # Render deployment config
├── runtime.txt            # Python version specification
├── README.md              # This file
└── handlers/              # Bot command handlers
    ├── __init__.py
    ├── start_handler.py   # /start command
    ├── rename_handler.py  # File rename functionality
    ├── thumbnail_handler.py # Thumbnail management
    ├── caption_handler.py # Caption management
    ├── metadata_handler.py # Metadata and prefix/suffix
    ├── user_handler.py    # User commands
    └── admin_handler.py   # Admin commands
```

## Installation

### Prerequisites

- Python 3.11 or higher
- MongoDB account (MongoDB Atlas recommended)
- Telegram account and Bot Token from @BotFather
- Telegram API credentials (API_ID and API_HASH)

### Step 1: Get Telegram Credentials

1. Go to https://my.telegram.org/auth
2. Login with your phone number
3. Click "API development tools"
4. Create a new application
5. Note down your **API_ID** and **API_HASH**
6. Create a bot at @BotFather and get your **BOT_TOKEN**

### Step 2: Setup MongoDB

1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free account
3. Create a new cluster
4. Get your connection string (DATABASE_URL)

### Step 3: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/file-rename-bot.git
cd file-rename-bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

### Step 3: Configure Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Telegram Configuration
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token

# Database Configuration
DB_URL=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=file_rename_bot

# Admin Configuration
OWNER_ID=your_telegram_user_id
LOG_CHANNEL=-1001234567890

# Optional Settings
FORCE_SUBS=channel_username
START_PIC=https://example.com/image.jpg
```

### Step 4: Get Your User ID

1. Start the bot by running `python main.py`
2. Send `/start` to the bot
3. Check the logs to find your User ID
4. Update `OWNER_ID` in `.env`

### Step 5: Create Log Channel

1. Create a private channel in Telegram
2. Add the bot as an admin
3. Send a message to the channel
4. Forward it to @userinfobot to get the channel ID (with -100 prefix)
5. Update `LOG_CHANNEL` in `.env`

## Running the Bot

### Local Development

```bash
# Make sure virtual environment is activated
python main.py
```

The bot will start and display:
```
Bot started successfully
Bot name: YourBotName (@yourbotusername)
```

### Testing Commands

Send these commands to your bot:
- `/start` - Start the bot
- `/help` - Show all available commands
- `/autorename` - Set custom rename format
- `/viewthumb` - View current thumbnail
- `/leaderboard` - View user leaderboard

## Deployment

### Deploy to Render

1. Push your code to GitHub
2. Go to https://render.com
3. Connect your GitHub account
4. Click "New +" → "Web Service"
5. Select your repository
6. Set environment variables (copy from `.env`)
7. Click "Deploy"

### Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set API_ID=xxx
heroku config:set API_HASH=xxx
heroku config:set BOT_TOKEN=xxx
heroku config:set DB_URL=xxx
heroku config:set OWNER_ID=xxx
heroku config:set LOG_CHANNEL=xxx

# Deploy
git push heroku main
```

### Deploy to Railway

1. Push code to GitHub
2. Go to https://railway.app
3. Create new project
4. Connect GitHub
5. Set environment variables
6. Deploy

### Deploy to Koyeb

1. Push code to GitHub
2. Go to https://koyeb.com
3. Create new app
4. Select GitHub
5. Set environment variables
6. Deploy

## Commands Reference

### User Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/autorename` | Set auto rename format |
| `/showformat` | View your rename format |
| `/tutorial` | Usage guide |
| `/leaderboard` | View leaderboard |
| `/viewthumb` | View thumbnail |
| `/delthumb` | Delete thumbnail |
| `/set_caption` | Set custom caption |
| `/see_caption` | View caption |
| `/del_caption` | Delete caption |
| `/setmedia` | Set output file type |
| `/start_sequence` | Start file sequencing |
| `/end_sequence` | End file sequencing |
| `/metadata` | View metadata |
| `/ping` | Check bot status |
| `/donate` | Support developer |
| `/set_prefix` | Set filename prefix |
| `/see_prefix` | View prefix |
| `/del_prefix` | Delete prefix |
| `/set_suffix` | Set filename suffix |
| `/see_suffix` | View suffix |
| `/del_suffix` | Delete suffix |
| `/status` | Check bot status |

### Admin Commands

| Command | Description |
|---------|-------------|
| `/add_admin` | Add new admin |
| `/deladmin` | Remove admin |
| `/admins` | List all admins |
| `/ban` | Ban a user |
| `/unban` | Unban a user |
| `/banned` | Show banned users |
| `/addchnl` | Add force subscribe channel |
| `/delchnl` | Remove force subscribe channel |
| `/listchnl` | View all channels |
| `/broadcast` | Broadcast message to all users |
| `/restart` | Restart the bot |

## Rename Format Variables

When setting a custom rename format, you can use these variables:

- `{season}` - Season number
- `{episode}` - Episode number
- `{title}` - File title
- `{quality}` - Video quality (e.g., 720p, 1080p)
- `{audio}` - Audio type (e.g., AAC, MP3)

### Example Formats

```
S{season}E{episode} - {title}
{title} ({quality})
{title} [{audio}] - {quality}
S{season}E{episode} {title} {quality}p
```

## Database Schema

### Collections

- **users**: User information and rename count
- **thumbnails**: User thumbnails
- **captions**: Custom captions
- **rename_formats**: Rename format settings
- **affixes**: Prefixes and suffixes
- **metadata**: User metadata
- **force_sub_channels**: Force subscribe channels
- **admins**: Admin users
- **sequences**: Active file sequences

## Troubleshooting

### Bot not responding

1. Check if bot token is correct
2. Verify internet connection
3. Check logs for errors
4. Ensure MongoDB connection is working

### Database connection error

1. Verify DATABASE_URL is correct
2. Check MongoDB cluster is running
3. Ensure IP whitelist includes your IP
4. Check database user password

### File rename not working

1. Ensure you've set a rename format first
2. Check file size is within limits
3. Verify bot has necessary permissions
4. Check logs for detailed error

### API_ID/API_HASH errors

1. Verify credentials from https://my.telegram.org
2. Check if values are correct type (API_ID should be number)
3. Regenerate credentials if needed

## Security

- All sensitive data is stored in environment variables
- Database credentials are never committed to git
- Bot validates all user inputs
- Admin commands require authentication
- Secure session management

## Performance

- Handles unlimited file renaming
- Fast database queries with indexing
- Optimized image processing
- Efficient memory usage
- Scales well with users

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, issues, or feature requests, please:

1. Check existing issues on GitHub
2. Create a detailed bug report
3. Include logs and error messages
4. Describe steps to reproduce

## Developer

**Created by**: Your Name  
**Support**: @dev_username  
**Updates**: Follow this channel for updates

---

Made with ❤️ using Pyrogram and MongoDB
