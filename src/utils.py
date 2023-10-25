import discord

# Function to create an Admin role if it doesn't exist
async def create_admin_role(guild):
    role = discord.utils.get(guild.roles, name='Admin')
    if role is None:
        role = await guild.create_role(name='Admin', permissions=discord.Permissions.all())
    return role


# List of funny catchphrases for ban without a specific reason
catchphrases = [
    "Because bananas are too slippery.",
    "For being a pineapple on pizza advocate.",
    "They spilled coffee on the server rack.",
    "Their keyboard was too clicky.",
    "The duck said so.",
]

