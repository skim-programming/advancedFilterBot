import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import json
import tracemalloc
import gc
from ofa import filter, blacklist, substitutes, whitelist, messageThreshold, is_valid_pattern
import emoji

TESTING_GUILD_ID =   # Replace with your guild ID

# ---------------- INTENTS ----------------
intents = nextcord.Intents.default()
intents.message_content = True
# Enable members intent only if needed:
# intents.members = True
tracemalloc.start()

bot = commands.Bot(intents=intents)

# ---------------- JSON LOAD/SAVE ----------------
def save_filter_data():
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump({
            "blacklist": blacklist,
            "whitelist": whitelist,
            "substitutes": substitutes,
            "threshold": messageThreshold
        }, f, ensure_ascii=False, indent=4)

# ---------------- EVENTS ----------------
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('bronx'):
        await message.channel.send("haiiiii nigga", delete_after=2)

    elif message.content.startswith('test'):
        channel = message.channel
        msg = (message.content.replace('test', '') if message.content != 'test' else 'test') + " is working on bro"
        await channel.send(msg, delete_after=2)
        await channel.send("aight ts working on bro", delete_after=2)

    if filter(message.content) > messageThreshold:
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention} naughty...", delete_after=2)
        except nextcord.errors.NotFound:
            print("Tried to delete a message that was already deleted.")
        except nextcord.errors.Forbidden:
            print("Missing permissions to delete message.")
        except Exception as e:
            print(f"Unexpected error deleting message: {e}")

    await bot.process_commands(message)

# ---------------- SLASH COMMANDS ----------------
@bot.slash_command(description="Set similarity threshhold", guild_ids=[TESTING_GUILD_ID])
@commands.has_permissions(manage_guild=True)
async def t(interaction: Interaction, threshhold):
    global messageThreshold
    try:
        messageThreshold = float(threshhold)
        await interaction.response.send_message(f"Threshold set to: {messageThreshold}")
    except:
        await interaction.response.send_message("Please enter a valid number 1-100")

@bot.slash_command(description="Add substitute", guild_ids=[TESTING_GUILD_ID])
@commands.has_permissions(read_message_history=True)
async def addsub(interaction: Interaction, sub, real_letter):
    if sub.startswith(":"):
        try:
            sub = emoji.emojize(sub)
        except:
            await interaction.response.send_message("Not a valid emoji")
            return
    if real_letter.lower() == "none":
        real_letter = ""
    substitutes[sub] = real_letter
    save_filter_data()
    await interaction.response.send_message(f"Substitute added: {sub} -> {real_letter}")

@bot.slash_command(description="Add word to blacklist", guild_ids=[TESTING_GUILD_ID])
@commands.has_permissions(manage_guild=True)
async def addbw(interaction: Interaction, word):
    if not is_valid_pattern(word):
        # Reject or warn user about too generic pattern
        await interaction.response.send_message("Pattern too generic, rejected")
    else:
        blacklist.append(word)
        save_filter_data()
    await interaction.response.send_message(f"Added word to blacklist: {word}")

@bot.slash_command(description="ez bypass", guild_ids=[TESTING_GUILD_ID])
@commands.has_permissions(manage_guild=True)
async def ezbypass(interaction: Interaction, bypassword):
    word = ""
    for i in bypassword:
        word+="_"
    whitelist.append(word)
    save_filter_data()
    await interaction.response.send_message("Bypass loaded")
@bot.slash_command(description="ez bypass remove", guild_ids=[TESTING_GUILD_ID])
@commands.has_permissions(manage_guild=True)
async def removeezbypass(interaction: Interaction, bypassword):
    word = ""
    for i in bypassword:
        word+="_"
    try:
        whitelist.remove(word)
        save_filter_data()
        await interaction.response.send_message("Bypass removed")
    except:
        await interaction.response.send_message("Bypass probably isnt in whitelist")
@bot.slash_command(description="Remove substitute", guild_ids=[TESTING_GUILD_ID])
@commands.has_permissions(manage_guild=True)
async def removesub(interaction: Interaction, sub):
    if sub.startswith(":"):
        try:
            sub = emoji.emojize(sub)
        except:
            await interaction.response.send_message("Not a valid emoji")
            return
    try:
        substitutes.pop(sub)
        save_filter_data()
        await interaction.response.send_message(f"Removed substitute: {sub}")
    except KeyError:
        await interaction.response.send_message("No such substitute found.")

@bot.slash_command(description="Remove word from blacklist", guild_ids=[TESTING_GUILD_ID])
@commands.has_permissions(manage_guild=True)
async def removebw(interaction: Interaction, word):
    try:
        blacklist.remove(word)
        save_filter_data()
        await interaction.response.send_message(f"Removed word from blacklist: {word}")
    except ValueError:
        await interaction.response.send_message("No such word in blacklist.")

@bot.slash_command(description="Add word to whitelist", guild_ids=[TESTING_GUILD_ID])
@commands.has_permissions(manage_guild=True)
async def addww(interaction: Interaction, word):
    whitelist.append(word)
    save_filter_data()
    await interaction.response.send_message(f"Added word to whitelist: {word}")

@bot.slash_command(description="Remove word from whitelist", guild_ids=[TESTING_GUILD_ID])
@commands.has_permissions(manage_guild=True)
async def removeww(interaction: Interaction, word):
    try:
        whitelist.remove(word)
        save_filter_data()
        await interaction.response.send_message(f"Removed word from whitelist: {word}")
    except ValueError:
        await interaction.response.send_message("No such word in whitelist.")

@bot.slash_command(description="View blacklist", guild_ids=[TESTING_GUILD_ID])
@commands.has_permissions(manage_guild=True)
async def viewbl(interaction: Interaction):
    await interaction.response.send_message("Blacklist: " + ", ".join(blacklist))

@bot.slash_command(description="View whitelist", guild_ids=[TESTING_GUILD_ID])
@commands.has_permissions(manage_guild=True)
async def viewwl(interaction: Interaction):
    await interaction.response.send_message("Whitelist: " + ", ".join(whitelist))

@bot.slash_command(description="View substitutes", guild_ids=[TESTING_GUILD_ID])
@commands.has_permissions(manage_guild=True)
async def viewsub(interaction: Interaction):
    await interaction.response.send_message("Substitutes: " + ", ".join(substitutes.keys()))

@bot.slash_command(description="Mimics what you say", guild_ids=[TESTING_GUILD_ID])
@commands.has_permissions(manage_guild=True)
async def mimic(interaction: Interaction, channelid: str, message: str):
    try:
        channel = bot.get_channel(int(channelid))
        if channel is None:
            raise ValueError("Invalid channel ID")
        await channel.send(message)
        await interaction.response.send_message(f"Sent message to <#{channelid}>")
    except Exception:
        await interaction.response.send_message("Invalid channel ID or bot lacks access.")

# ------------- MEMORY TRACKING COMMANDS -------------
@bot.slash_command(description="Track memory usage", guild_ids=[TESTING_GUILD_ID])
@commands.has_permissions(read_message_history=True)
async def trackmem(interaction: Interaction):
    await interaction.response.defer()
    try:
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')

        result_lines = ["Top 10 memory usage lines:"]
        for stat in top_stats[:10]:
            result_lines.append(str(stat))

        output = "\n".join(result_lines)
        if len(output) > 1900:
            output = output[:1900] + "\n... (truncated)"

        await interaction.followup.send(f"```py\n{output}\n```")
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

@bot.slash_command(description="Force garbage collection", guild_ids=[TESTING_GUILD_ID])
async def gcflush(interaction: Interaction):
    collected = gc.collect()
    await interaction.response.send_message(f"Forced garbage collection.\nObjects collected: `{collected}`")

# ---------------- RUN ----------------
bot.run("BOT_TOKEN_HERE")  # Replace with your token
