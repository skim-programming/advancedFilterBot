import nextcord, regex
from nextcord.ext import commands
from nextcord import ui
from ofa import filter, filteredWords, substitutes, messageThreshold
import emoji

TESTING_GUILD_ID =   # Replace with your guild ID

bot = commands.Bot(intents=nextcord.Intents.all())
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Filter stuff
@bot.slash_command(description="Set similarity threshhold", guild_ids=[TESTING_GUILD_ID])
@commands.has_permissions(manage_guild=True)
async def t(interaction:nextcord.Interaction, threshhold):
    global messageThreshold
    try:
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
    message_handled = False
    if not message_handled and filter(message.content) > messageThreshold:
        await message.delete()
        await message.channel.send(f"{message.author.mention} naughty...", delete_after=2)
        message_handled = True

    #print("Threshold is: " + str(messageThreshold))
    #print(filter(message.content) >= messageThreshold)
    print(message.content + ": " + str(filter(message.content)))

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
            return
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
            return
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

bot.run('')
