import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import emojidatabase

load_dotenv() # Loads from the .env file in the same directory
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Intents are required for certain events
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content

# Create bot instance with a command prefix
bot = commands.Bot(command_prefix="!", intents=intents)

##### COMMANDS #####

@bot.command(name="hello")
async def hello_command(ctx):
    """Responds with a greeting."""
    await ctx.send(f"Hello, {ctx.author.mention}! 👋")

@bot.command(name="praiseme")
async def praiseme_command(ctx):
    """Responds with some praise."""
    await ctx.send(f"You're such a good boy, {ctx.author.mention}.")

@bot.command(name="instruction")
async def button (ctx):
    """Sends a message with a clickable button"""
    view = MyView()
    await ctx.send("Are you going to behave?", view=view)

@bot.command(name="newreact")
async def addreact_command(ctx, word, emoji):
    """Tries to add a new pair to the database"""
    edb.addPairToDB(word, emoji)


@bot.command(name="shutdown")
async def shutdown(ctx):
    """Shuts down the bot"""
    await ctx.send("Shutting down...")
    await bot.close()

# Define a simple View with a Button
class MyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # No timeout for the view

    @discord.ui.button(label="Yessir", style=discord.ButtonStyle.primary)
    async def click_me(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            f"Oh my, {interaction.user.mention}. You are so good at following directions.",
            ephemeral=True  # Only visible to the user who clicked
        )

##### EVENTS #####

@bot.event
async def on_command_error(ctx, error):
    """Handles errors gracefully."""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Try `!hello`.")
    else:
        await ctx.send("⚠️ An error occurred.")
        raise error  # Log the error for debugging

@bot.event
async def on_ready():
    """Triggered when the bot is ready."""
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content[0] == "!":
        return

    for word in edb.getListOfTriggerWords():
        if word.lower() in message.content.lower():
            try:
                await message.add_reaction(edb.getEmojiFromDB(word))
                print(f"Reacted to message: {message.content}")
            except discord.HTTPException as e:
                print(f"⚠️ Failed to react{e}")

##### MAIN #####

if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR: Please set the DISCORD_BOT_TOKEN environment variable.")
    else:
        try:
            edb = emojidatabase.EmojiDatabase()

            bot.run(TOKEN)
        except KeyboardInterrupt:
            print("\nBot stopped manually.")
