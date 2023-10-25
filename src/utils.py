import discord

# Function to create an Admin role if it doesn't exist
async def create_admin_role(guild):
    role = discord.utils.get(guild.roles, name='Admin')
    if role is None:
        role = await guild.create_role(name='Admin', permissions=discord.Permissions.all())
    return role


# List of funny catchphrases for ban without a specific reason
catchphrases = [
    "For wearing socks with sandals.",
    "Because they're a closet teletubby fan.",
    "Their favorite movie is 'The Emoji Movie'.",
    "They put ketchup on their spaghetti.",
    "For having too many cat pictures on their phone.",
    "They're allergic to fun.",
    "They can't dance even if their life depended on it.",
    "Because their favorite song is 'Baby Shark'.",
    "For using Comic Sans in official documents.",
    "Their password is 'password'.",
    "They like pineapple on pizza.",
    "For saying 'YOLO' unironically.",
    "They still use Internet Explorer.",
    "Their favorite color is brown. Yes, brown.",
    "Because they spoil every movie ending.",
]
