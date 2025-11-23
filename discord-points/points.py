import discord
import aiosqlite
import os
import logging
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database Manager Class
class DatabaseManager:
    def __init__(self, db_name="points.db"):
        self.db_name = db_name

    async def initialize(self):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''CREATE TABLE IF NOT EXISTS points (user_id INTEGER PRIMARY KEY, points INTEGER)''')
            await db.commit()

    async def get_points(self, user_id):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT points FROM points WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()
                if result:
                    return result[0]
                else:
                    await db.execute("INSERT INTO points (user_id, points) VALUES (?, ?)", (user_id, 0))
                    await db.commit()
                    return 0

    async def update_points(self, user_id, points):
        current_points = await self.get_points(user_id)
        new_points = current_points + points
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("UPDATE points SET points = ? WHERE user_id = ?", (new_points, user_id))
            await db.commit()
        return new_points

    async def set_points(self, user_id, points):
         async with aiosqlite.connect(self.db_name) as db:
            # Ensure user exists first
            await self.get_points(user_id)
            await db.execute("UPDATE points SET points = ? WHERE user_id = ?", (points, user_id))
            await db.commit()

    async def get_leaderboard(self, limit=10):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT user_id, points FROM points ORDER BY points DESC LIMIT ?", (limit,)) as cursor:
                return await cursor.fetchall()

# Bot Class
class PointsBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="-", intents=intents)
        self.db = DatabaseManager()

    async def setup_hook(self):
        await self.db.initialize()
        await self.tree.sync()
        logger.info("Slash commands synced and database initialized.")

    async def on_ready(self):
        logger.info(f"{self.user} is online and ready!")
        await self.change_presence(activity=discord.Game(name="Managing points!"))

bot = PointsBot()

# Slash Commands
@bot.tree.command(name="mypoints", description="Check your current points.")
async def mypoints(interaction: discord.Interaction):
    points = await bot.db.get_points(interaction.user.id)
    await interaction.response.send_message(f"{interaction.user.mention}, you have {points} points.")

@bot.tree.command(name="addpoints", description="Add points to a user.")
@discord.app_commands.checks.has_permissions(administrator=True)
async def addpoints(interaction: discord.Interaction, member: discord.Member, points: int):
    await bot.db.update_points(member.id, points)
    await interaction.response.send_message(f"{points} points have been added to {member.mention}.")

@bot.tree.command(name="removepoints", description="Remove points from a user.")
@discord.app_commands.checks.has_permissions(administrator=True)
async def removepoints(interaction: discord.Interaction, member: discord.Member, points: int):
    # Removing points is effectively adding negative points, but let's handle it safely
    # Logic in original was max(0, current - points). Let's replicate that logic in update or here.
    # The original logic was: new_points = max(0, current_points - points)
    # My update_points just adds. Let's do it manually here to preserve logic or update the manager.
    # Let's use a custom logic here to match original behavior of not going below 0.
    
    current = await bot.db.get_points(member.id)
    new_amount = max(0, current - points)
    await bot.db.set_points(member.id, new_amount)
    
    await interaction.response.send_message(f"{points} points have been removed from {member.mention}. New total: {new_amount}")

@bot.tree.command(name="leaderboard", description="Show the top 10 users.")
async def leaderboard(interaction: discord.Interaction):
    leaderboard_data = await bot.db.get_leaderboard()
    if leaderboard_data:
        leaderboard_message = "**Leaderboard:**\n"
        for idx, (user_id, points) in enumerate(leaderboard_data, start=1):
            try:
                user = await bot.fetch_user(user_id)
                name = user.name
            except:
                name = "Unknown User"
            leaderboard_message += f"{idx}. {name} - {points} points\n"
        await interaction.response.send_message(leaderboard_message)
    else:
        await interaction.response.send_message("No points have been recorded yet.")

@addpoints.error
@removepoints.error
async def admin_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.MissingPermissions):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
    else:
        await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token or token == "YOUR_BOT_TOKEN_HERE":
        logger.error("No valid DISCORD_TOKEN found in .env file.")
    else:
        bot.run(token)
