# Discord Points Bot

A robust Discord bot built with Python and `discord.py` to manage user points, display leaderboards, and enable administrators to adjust points dynamically via slash commands. This bot is designed to replace outdated legacy solutions, offering a modern, asynchronous, and database-backed system for engaging communities.

---

## Features

- **User Points Management**:
  - Users can check their points with `/mypoints`.
  - Administrators can add or remove points for users with `/addpoints` and `/removepoints`.

- **Leaderboard**:
  - Display the top 10 users with the most points using `/leaderboard`.

- **Slash Command Interface**:
  - Intuitive commands that integrate seamlessly into the Discord UI.

- **Reliability**:
  - Powered by `aiosqlite` for non-blocking database operations.
  - Secure token management using environment variables.

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
  - [Download Python](https://www.python.org/downloads/)

- **Discord Bot Token**:
  - Create one via the [Discord Developer Portal](https://discord.com/developers/applications).

## Permissions & Intents

To ensure the bot functions correctly, please configure the following in the Discord Developer Portal:

### 1. OAuth2 Scopes
- `bot`
- `applications.commands`

### 2. Bot Permissions
- `Manage Messages`
- `Use Slash Commands`
- `Read Messages`
- `Send Messages`

### 3. Privileged Gateway Intents
- **Server Members Intent**: Required for the bot to access member details.

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/discord-points-bot.git
cd discord-points-bot/discord-points
```

### 2. Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the required Python libraries:

```bash
pip install discord.py aiosqlite python-dotenv
```

### 4. Configure the Bot

Create a `.env` file in the `discord-points` directory and add your bot token:

```env
DISCORD_TOKEN=your_actual_token_here
```

### 5. Run the Bot

Start the bot using the following command:

```bash
python points.py
```

*Note: If you are not in the virtual environment, use `./venv/bin/python points.py`*

---

## License

This project is licensed under the MIT License.