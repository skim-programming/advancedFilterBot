import nextcord, regex
from nextcord.ext import commands
from nextcord import ui
from ofa import filter, filteredWords, substitutes
import emoji

TESTING_GUILD_ID =  # Replace with your guild ID

bot = commands.Bot(".", intents=nextcord.Intents.all())

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Filter stuff
@bot.slash_command(description="Set similarity threshhold", guild_ids=[TESTING_GUILD_ID])
@commands.has_permissions(manage_guild=True)
async def t(interaction:nextcord.Interaction, threshhold):
    try:
        global messageThreshold
        messageThreshold = float(threshhold)
        await interaction.send("Done")
        await interaction.send("Threshhold is: " + str(messageThreshold))
    except:
        await interaction.send("Please enter a valid float")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    elif message.content.startswith('bronx'):
        await message.channel.send("haiiiii nigga", delete_after=2)
    elif message.content.startswith('test'):   
        channel = message.channel
        await channel.send((message.content.replace('test', '') if message.content != 'test' else 'test') + " is working on bro", delete_after=2) # ???
        await channel.send("aight ts working on bro", delete_after=2)
    
    # Filter offensive content
    offensive_patterns = [
        # Basic pattern with character substitutions and repetitions
        r'n+[i1!|l]+[g6q9]+[g6q9]*[e3]*[r®]+s?',
        
        # More specific patterns for common variations
        r'n[i1!|l]*g{1,3}[e3]*r+s?',
        r'n+[i1!|l]+g{1,3}[e3]*r+s?',
        
        # Pattern for spaced or separated characters
        r'n[\s\-_\.]*[i1!|l]+[\s\-_\.]*[g6q9]+[\s\-_\.]*[g6q9]*[\s\-_\.]*[e3]*[\s\-_\.]*[r®]+[\s\-_\.]*s?',
        
        # Pattern for zero-width characters and unicode variations
        r'n[\u200b\u200c\u200d\ufeff]*[i1!|l]+[\u200b\u200c\u200d\ufeff]*[g6q9]+[\u200b\u200c\u200d\ufeff]*[g6q9]*[\u200b\u200c\u200d\ufeff]*[e3]*[\u200b\u200c\u200d\ufeff]*[r®]+[\u200b\u200c\u200d\ufeff]*s?',
        
        # Add more patterns here as needed
    ]
    
    message_handled = False
    if not message_handled and filter(message.content) > messageThreshold and message.author!=bot.user: # or not message_handled and regex.search(pattern, message.content, regex.IGNORECASE) 
        await message.delete()
        await message.channel.send(f"{message.author.mention} naughty...", delete_after=2)

        message_handled = True

    print("Threshold is: " + str(messageThreshold))
    print(filter(message.content) >= messageThreshold)
    print(filter(message.content))

    await bot.process_commands(message)





# command stuff

@bot.slash_command(description="Add sub", guild_ids=[TESTING_GUILD_ID])
@commands.has_permissions(manage_guild=True)
async def addsub(interaction: nextcord.Interaction, sub, real_letter):
    if(sub.startswith(":")):
        try:
            sub = sub.emojize(sub)
        except:
            print("Not a valid emoji")
    substitutes[sub] = real_letter
    await interaction.send("Sub: " + sub + " Letter: " + real_letter, delete_after=2)
@bot.slash_command(description="Add word", guild_ids=[TESTING_GUILD_ID])
@commands.has_permissions(manage_guild=True)
async def addword(interaction: nextcord.Interaction, word):
    filteredWords.append(word)
    await interaction.send("Added word: " + word, delete_after=2)

@bot.slash_command(description="Remove substitute", guild_ids=[TESTING_GUILD_ID])
@commands.has_permissions(manage_guild=True)
async def removesub(interaction: nextcord.Interaction, sub):
    if(sub.startswith(":")):
        try:
            sub = sub.emojize(sub)
        except:
            print("Not a valid emoji")
    try:
        substitutes.pop(sub)
        await interaction.send("Removed sub: " + sub, delete_after=2)
    except:
        await interaction.send("Error (probably no such sub)", delete_after=2)

@bot.slash_command(description="Remove word from filter list", guild_ids=[TESTING_GUILD_ID])
@commands.has_permissions(manage_guild=True)
async def removeword(interaction: nextcord.Interaction, word):
    try:
        filteredWords.remove(word)
        await interaction.send("Removed sub: " + word, delete_after=2)
    except:
        await interaction.send("Error (probably no such word in filter list)", delete_after=2)

@bot.slash_command(description="My first slash command", guild_ids=[TESTING_GUILD_ID])
@commands.has_permissions(manage_guild=True)
async def hello(interaction: nextcord.Interaction):
    await interaction.send("hello goat!")

@bot.slash_command(description="embed / interaction test", guild_ids=[TESTING_GUILD_ID])
@commands.has_permissions(manage_guild=True)
async def embed(interaction: nextcord.Interaction):
    embed = nextcord.Embed(title="hi...", description="> **This** is a __test__ embed.", color=nextcord.Color.blue())
    embed.set_footer(text="hohohohoho", icon_url=interaction.guild.icon.url if interaction.guild.icon else interaction.user.default_avatar.url)
    embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)

    class drop(ui.Select):
        def __init__(self):
            options = [
                nextcord.SelectOption(label="Option 1", description="First option"),
                nextcord.SelectOption(label="Option 2", description="Second option"),
                nextcord.SelectOption(label="Option 3", description="Third option"),
            ]
            super().__init__(placeholder="choose...", min_values=1, max_values=1, options=options)

        async def callback(self, interaction: nextcord.Interaction):
            await interaction.response.send_message(f"You selected: {self.values[0]}", ephemeral=True)

    class view(ui.View):
        def __init__(self):
            super().__init__()
            self.add_item(drop())

        @ui.button(label="Click Me!", style=nextcord.ButtonStyle.primary)
        async def button_callback(self, button: ui.Button, interaction: nextcord.Interaction):
            await interaction.response.send_message("push my byuttowns nghhhh~", ephemeral=True)

    view = view()
    await interaction.send(embed=embed, view=view)

bot.run('')