import random
from utils import create_admin_role
from discord.ext import commands
import discord

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents = intents # Set up basic permissions
)

bot.author_id = 469966130593923082  # Change to your Discord ID

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.command()
async def pong(ctx):
    await ctx.send('pong')
    
@bot.command()
async def name(ctx):
    await ctx.send(ctx.author.name)

@bot.command()
async def d6(ctx):
    await ctx.send(random.randint(1, 6))

@bot.command()
async def admin(ctx, member: discord.Member):
    if ctx.author.guild_permissions.administrator:
        admin_role = await create_admin_role(ctx.guild)
        await member.add_roles(admin_role)
        await ctx.send(f'{member.mention} has been granted the Admin role.')
    else:
        await ctx.send("You don't have permission to use this command.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == "salut tout le monde":
        response = f"Salut tout seul, {message.author.mention}!"
        await message.channel.send(response)
    
    await bot.process_commands(message)

# Command to ban a user with an optional reason
@bot.command()
async def ban(ctx, member: discord.Member, *, reason="No specific reason"):
    # Check if the user issuing the command has the "Ban Members" permission
    if ctx.author.guild_permissions.ban_members:
        try:
            await member.ban(reason=reason)
            await ctx.send(f'{member.mention} has been banned for the reason: {reason}')
        except discord.Forbidden:
            await ctx.send("I don't have the necessary permissions to ban members.")
    else:
        await ctx.send("You don't have permission to use this command.")

# Command to ban a user with a random catchphrase as the reason
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        catchphrase = random.choice(catchphrases)
        await ctx.send(f"Banning {ctx.message.content.split(' ')[1]}: {catchphrase}")

token = "MTE2Njc4NTE5MzAxNzg3MjU1NQ.GvmUKe.lW4qVqGnb7SpGjJCYghVaFer0pfl5eYe5K7Zsg"
bot.run(token)  # Starts the bot
