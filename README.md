# Discord Points Bot

A **Discord bot** created in python and built using `discord.py` to manage user points, display leaderboards, and enable admins to adjust points dynamically via slash commands. I made this to replace all of the outdated / broken points bots scattered from early Discord. This bot is perfect for engaging communities and gamifying participation in your server!

---

## 🚀 Features

- **User Points Management**:
  - Users can check their points with `/mypoints`.
  - Admins can add or remove points for users with `/addpoints` and `/removepoints`.

- **Leaderboard**:
  - Display the top 10 users with the most points using `/leaderboard`.

- **Slash Command Interface**:
  - Easy-to-use commands that integrate seamlessly into Discord's UI.

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
  - [Download Python](https://www.python.org/downloads/)
- **discord.py 2.0+**
  - Install it via pip:
    ```bash
    pip install -U discord.py
    ```

- **SQLite3**:
  - Comes pre-installed with most Python distributions. Verify by running:
    ```bash
    python -c "import sqlite3"
    ```

- A **Discord Bot Token**:
  - Create one via the [Discord Developer Portal](https://discord.com/developers/applications).

---

## Getting Started

### Install Dependencies

Install the required Python libraries:

```bash
pip install -U discord.py
```

### Configure the Bot Token

Open the script and replace `YOUR_BOT_TOKEN` with your bot's token:

```python
TOKEN = "YOUR_BOT_TOKEN"  # Replace this with your bot token
```

### Run the Bot

Run the bot with:

```bash
python points.py
```
A DB will generate after running the points.py file for the first time.
---

## Permissions & Intents

To set up your bot correctly, follow these steps to configure permissions and intents:

### **1. Setting Up the Bot in the Discord Developer Portal**

1. **Create a New Application**:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications).
   - Click the **New Application** button.
   - Enter a name for your bot (e.g., "Points Bot") and click **Create**.

2. **Create the Bot**:
   - In your application settings, navigate to the **Bot** tab.
   - Click **Add Bot** and confirm.
   - You will now see your bot token. Click **Copy** to save it. *(Keep this token private!)*

3. **Set Up OAuth2 URL**:
   - Go to the **OAuth2** > **URL Generator** section.
   - Under **Scopes**, select:
     - `bot`
     - `applications.commands`
   - Under **Bot Permissions**, select the following:
     - `Manage Messages`
     - `Use Slash Commands`
     - `Read Messages`
     - `Send Messages`
   - Copy the generated URL, paste it into your browser, and invite the bot to your server.

---

### **2. Enabling Privileged Gateway Intents**

1. In the **Bot** settings, scroll to the **Privileged Gateway Intents** section.
2. Enable:
   - **Server Members Intent**: Required for the bot to access member details.
   - **Message Content Intent**: Optional; needed only if analyzing text messages (not required for this bot).

Click **Save Changes**.

---

### **3. Verifying Bot Permissions in Your Server**

1. Go to your Discord server.
2. Navigate to **Server Settings** > **Roles**.
3. Locate the bot’s role and ensure it has:
   - **Manage Guild**
   - **Manage Messages**
   - **Use Slash Commands**

4. Ensure the bot's role is placed **above** roles it needs to manage in the role hierarchy.

---

### **4. Syncing Slash Commands**

When the bot starts, it automatically syncs slash commands to your server. If slash commands are not appearing:
- Restart the bot to force a sync.
- Ensure the bot has `applications.commands` scope in the OAuth2 setup.

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).
