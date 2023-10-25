import random
import asyncio
import aiohttp
from utils import create_admin_role, catchphrases
from discord.ext import commands, tasks
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
    
    if not message.author.bot:
        author_id = message.author.id
        message_counts[author_id] = message_counts.get(author_id, 0) + 1
    
    await bot.process_commands(message)

# Command to ban a user with an optional reason
@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    # Check if the user issuing the command has the "Ban Members" permission
    if ctx.author.guild_permissions.ban_members:
        try:
            if reason is None:
                reason = random.choice(catchphrases)
            await member.ban(reason=reason)
            await ctx.send(f'{member.mention} has been banned for the reason: {reason}')
        except discord.Forbidden:
            await ctx.send("you don't have the necessary permissions to ban members.")
    else:
        await ctx.send("You don't have permission to use this command.")

# Define a dictionary to store user message counts
message_counts = {}

# Store flood state
is_flooding = False

# Define a warning message
warning_message = "You're sending too many messages! Stop it or I'll ban you."

# Command to (de)activate the flood monitoring
@bot.command()
async def flood(ctx):
    global is_flooding
    if is_flooding is False:
        flood_monitor.start(ctx)
        is_flooding = True
        await ctx.send("Flood monitoring activated.")
    else:
        flood_monitor.cancel()
        is_flooding = False
        await ctx.send("Flood monitoring deactivated.")

# Function to check for message floods
@tasks.loop(seconds=10.0)
async def flood_monitor(ctx):
    guild = ctx.guild
    for member, count in list(message_counts.items()):
        if count >= 5:  # Adjust the threshold as needed
            user = guild.get_member(member)
            if user:
                await ctx.send(f'{user.mention} {warning_message}')
        del message_counts[member]

        
# Command to post a random xkcd comic
@bot.command()
async def xkcd(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://xkcd.com/info.0.json') as response:
            if response.status == 200:
                data = await response.json()
                comic_num = random.randint(1, data['num'])
                async with session.get(f'https://xkcd.com/{comic_num}/info.0.json') as comic_response:
                    res = await comic_response.json()
                    await ctx.send(res['img'])
                    # if comic_response.status == 200:
                    #     comic_data = await comic_response.json()
                    #     embed = discord.Embed(
                    #         title=comic_data['safe_title'],
                    #         url=f'https://xkcd.com/{comic_data["num"]}',
                    #         description=comic_data['alt']
                    #     )
                    #     embed.set_image(url=comic_data['img'])
                    #     await ctx.send(embed=embed)
            else:
                await ctx.send("Sorry, I couldn't retrieve an xkcd comic at the moment.")

# Command to create a poll with time limit
@bot.command()
async def poll(ctx, *, question):
    poll_message = await ctx.send(f'@here {ctx.author.mention} asks: {question}')  # Mention @here
    await poll_message.add_reaction('👍')  # Add a thumbs up reaction
    await poll_message.add_reaction('👎')  # Add a thumbs down reaction

    time_limit = 60  # Set the time limit for the poll in seconds (1 minute)

    await asyncio.sleep(time_limit)

    final_result = await ctx.channel.fetch_message(poll_message.id)
    thumbs_up = 0
    thumbs_down = 0

    for reaction in final_result.reactions:
        if reaction.emoji == '👍':
            thumbs_up = reaction.count - 1  # Subtract 1 to exclude the bot's reaction
        elif reaction.emoji == '👎':
            thumbs_down = reaction.count - 1  # Subtract 1 to exclude the bot's reaction

    await ctx.send(f'The poll "{question}" has ended! Final results:\n👍: {thumbs_up}\n👎: {thumbs_down}')
    await poll_message.delete()

token = "MTE2Njc4NTE5MzAxNzg3MjU1NQ.GBc3GC.9fBknewukQt7gAonbNF0oi1R5oj_r1M8r4Sw2E"
bot.run(token)  # Starts the bot
