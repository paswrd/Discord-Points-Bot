import discord, sqlite3
from discord.ext import commands, tasks

# Database setup
conn = sqlite3.connect("points.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS points (user_id INTEGER PRIMARY KEY, points INTEGER)''')
conn.commit()

# Function to fetch or initialize points for a user
def get_or_initialize_user_points(user_id):
    cursor.execute("SELECT points FROM points WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute("INSERT INTO points (user_id, points) VALUES (?, ?)", (user_id, 0))
        conn.commit()
        return 0

# Add points to a user
def add_points(user_id, points):
    current_points = get_or_initialize_user_points(user_id)
    cursor.execute("UPDATE points SET points = ? WHERE user_id = ?", (current_points + points, user_id))
    conn.commit()

# Remove points from a user
def remove_points(user_id, points):
    current_points = get_or_initialize_user_points(user_id)
    new_points = max(0, current_points - points)
    cursor.execute("UPDATE points SET points = ? WHERE user_id = ?", (new_points, user_id))
    conn.commit()

# Initialize bot with all intents enabled
intents = discord.Intents.all()
PointsBot = commands.Bot(command_prefix="-", intents=intents)

@PointsBot.event
async def on_ready():
    print(f"{PointsBot.user} is online and ready!")
    await PointsBot.change_presence(activity=discord.Game(name="Managing points!"))
    try:
        await PointsBot.tree.sync()
        print("Slash commands synced.")
    except Exception as e:
        print(f"Error syncing slash commands: {e}")

# Slash command to check your points
@PointsBot.tree.command(name="mypoints", description="Check your current points.")
async def mypoints(interaction: discord.Interaction):
    points = get_or_initialize_user_points(interaction.user.id)
    await interaction.response.send_message(f"{interaction.user.mention}, you have {points} points.")

# Slash command to add points (admin only)
@PointsBot.tree.command(name="addpoints", description="Add points to a user.")
async def addpoints(interaction: discord.Interaction, member: discord.Member, points: int):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return
    add_points(member.id, points)
    await interaction.response.send_message(f"{points} points have been added to {member.mention}.")

# Slash command to remove points (admin only)
@PointsBot.tree.command(name="removepoints", description="Remove points from a user.")
async def removepoints(interaction: discord.Interaction, member: discord.Member, points: int):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return
    remove_points(member.id, points)
    await interaction.response.send_message(f"{points} points have been removed from {member.mention}.")

# Slash command to display the leaderboard
@PointsBot.tree.command(name="leaderboard", description="Show the top 10 users.")
async def leaderboard(interaction: discord.Interaction):
    cursor.execute("SELECT user_id, points FROM points ORDER BY points DESC LIMIT 10")
    leaderboard_data = cursor.fetchall()
    if leaderboard_data:
        leaderboard_message = "**Leaderboard:**\n"
        for idx, (user_id, points) in enumerate(leaderboard_data, start=1):
            user = await PointsBot.fetch_user(user_id)
            leaderboard_message += f"{idx}. {user.name} - {points} points\n"
        await interaction.response.send_message(leaderboard_message)
    else:
        await interaction.response.send_message("No points have been recorded yet.")

# Bot token and start logic
TOKEN = "YOUR_BOT_TOKEN"  # Replace with your bot token
PointsBot.run(TOKEN)
