#This file is part of FennecBot.
#FennecBot is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#FennecBot is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
#You should have received a copy of the GNU Affero General Public License along with FennecBot. If not, see <https://www.gnu.org/licenses/>.

# bot.py
# Import all of the necessary libaries
import os 
import random
import discord
import hashlib
import datetime
import time

from discord.ext import commands
from dotenv import load_dotenv

# Gets my discord bot token from an external file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Manual commands use the prefix #!
bot = commands.Bot(command_prefix='#!')

agplNotice = "FennecBot, a project that will eventually be forked into Free6\nCopyright (C) 2022  Kenneth Davis\n\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU Affero General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU Affero General Public License for more details.\n\nYou should have received a copy of the GNU Affero General Public License\nalong with this program.  If not, see <https://www.gnu.org/licenses/>."

##
##
## INFORMATIONAL COMMANDS
##
##

# the help command, #!helppls, #!man, #!?
@bot.command(name='helppls', aliases=['man', '?'])
async def helppls(message):
    # Send the help message
    await message.channel.send("```\nThis bot manages formatting/filtering links. (Version 2022.02.27.A)\n\nCommands:\n\n#!man - shows the help page.\n#!source - attaches the main .py file for the bot, and a copy of the GNU Affero General Public License v3.\n#!agpl - displays the AGPL notice.\n#!github - shows a link to FennecBot's GitHub repo\n\n#!toggleNSFW - toggles the NSFW filter (enabled by default, requires admin to disable)\n#!addNSFW <arg> - creates a server specific list of links to be filtered if it does not already exists, and adds the argument to the list\n#!rmNSFW <arg> - removes argument from above list\n#!showNSFW - sends list of NSFW links banned in the server to the user\n#!addBadWord <arg> - Creates a server specific list of words/links not allowed to be said in any channel, and adds argument to the list.\n#!rmBadWord <arg> - Removes argument from above list\n#!showBadWords - sends list of bad words banned in the server to the user\n#!toggleYT - toggles the YouTube Shorts formatter (enabled by default, requires admin to disable)\n\nAt this time broken discord embedded links are fixed automatically and cannot be toggled.\n```")

# Gives the user the main source code for the application.
@bot.command(name='sourceCode', aliases=['source'])
async def sourceCode(ctx):
    await ctx.send(file=discord.File('README.md'))
    await ctx.send(file=discord.File('COPYING'))
    await ctx.send(file=discord.File('FennecBot.py'))

@bot.command(name='agplNoticeDisplay', aliases=["agpl"])
async def agplNoticeDisplay(message):
    await message.channel.send(f"```\n{agplNotice}\n```")

@bot.command(name='githubSource', aliases=["github"])
async def githubSource(message):
    await message.channel.send(f"{message.author.mention} https://github.com/CoatlessEskimo/FennecBot")

# Lists debug commands
@bot.command(name='debugInfo', aliases=['debug'])
async def debugInfo(ctx):
    await ctx.send("```\nThis is an incomplete list of commands intended for the bot's HOST only. Please be advised.\n\n#!permission - tells a user whether or not they have admin privileges in a server.\n```")

##
##
## COMMANDS
##
##

# the nsfw filter command, and the beginning of the spaghetti
@bot.command(name='addNSFWLink', aliases=['addNSFW'])
async def addNSFWLink(ctx, *, arg):
    customList = f'customLists/{ctx.guild.id}-NSFW.txt'
    addLink = f'{arg}'
    if ctx.message.author.guild_permissions.administrator:
        if os.path.exists(customList):
            pass
        else:
            await ctx.send("Custom NSFW list does not exist for this server.")
            try:
                await ctx.send("Trying to create...")
                open(customList, 'a').close()
            except OSError:
                await ctx.send("Couldn't create list.")
            else:
                await ctx.send("Created list!")
        with open(customList, 'r') as file:
            if not f"{arg}" in file.read():
                with open(customList, 'a') as file:
                    file.write(f"{arg}\n")
                    await ctx.send("Added link/word to list!")
            else:
                await ctx.send("This link/word is already in the list!")
                return
    else:
        await ctx.send("You don't have permission to do that.")

@bot.command(name='removeNSFWLink', aliases=['rmNSFW'])
async def removeBadWord(ctx, *, arg):
    customList = f'customLists/{ctx.guild.id}-NSFW.txt'
    if ctx.message.author.guild_permissions.administrator:
        if os.path.exists(customList):
            pass
        else:
            ctx.send("You don't have a custom NSFW link list yet. Add a link to begin.")
            return
        with open(customList, 'r+') as file:
            newCustomList = file.read().replace(f'{arg}\n', '')
            file.seek(0)
            file.write(newCustomList)
            file.truncate()
            await ctx.send("Removed link/word from list.")

@bot.command(name='showNSFWLinks', aliases=['showNSFW'])
async def showNSFWLinks(ctx):
    customList = f'customLists/{ctx.guild.id}-NSFW.txt'
    if ctx.message.author.guild_permissions.administrator:
        if os.path.exists(customList):
            with open(customList, 'r') as file:
                sentCustomList = file.read()
                try:
                    await ctx.message.author.send(f'Here is a list of NSFW links from {ctx.guild.name}:\n```\n{sentCustomList}\n```')
                except Exception:
                    await ctx.send(f"{ctx.message.author.mention}, I couldn't send you the list. This is because either you cannot accept direct messages, or because the list exists, but is empty.")
                else:
                    await ctx.send(f"Sent list of NSFW links to {ctx.message.author.mention}. Check your messages.")
        else:
            await ctx.send("There is no NSFW link list. Add a word to get started.")
    else:
        await ctx.send("You don't have permission for that {ctx.message.author.mention}.")

@bot.command(name='addBadWord')
async def addBadWord(ctx, *, arg):
    customList = f'customLists/{ctx.guild.id}-GLOBAL.txt'
    addLink = f'{arg}'
    if ctx.message.author.guild_permissions.administrator:
        if os.path.exists(customList):
            pass
        else:
            await ctx.send("Custom banned link/word list does not exist for this server.")
            try:
                await ctx.send("Trying to create...")
                open(customList, 'a').close()
            except OSError:
                await ctx.send("Couldn't create list.")
            else:
                await ctx.send("Created list!")
        with open(customList, 'r') as file:
            if not f"{arg}" in file.read():
                with open(customList, 'a') as file:
                    file.write(f"{arg}\n")
                    await ctx.send("Added link/word to list!")
            else:
                await ctx.send("This link/word is already in the list!")
                return
    else:
        await ctx.send("You don't have permission to do that.")

@bot.command(name='removeBadWord', aliases=['rmBadWord'])
async def removeBadWord(ctx, *, arg):
    customList = f'customLists/{ctx.guild.id}-GLOBAL.txt'
    if ctx.message.author.guild_permissions.administrator:
        if os.path.exists(customList):
            pass
        else:
            ctx.send("You don't have a custom banned word/link list yet. Add a word/link to begin.")
            return
        with open(customList, 'r+') as file:
            newCustomList = file.read().replace(f'{arg}\n', '')
            file.seek(0)
            file.write(newCustomList)
            file.truncate()
            await ctx.send("Removed link/word from list.")

@bot.command(name='showBadWords', aliases=['lsBadWords'])
async def showBadWords(ctx):
    customList = f'customLists/{ctx.guild.id}-GLOBAL.txt'
    if ctx.message.author.guild_permissions.administrator:
        if os.path.exists(customList):
            with open(customList, 'r') as file:
                sentCustomList = file.read()
                try:
                    await ctx.message.author.send(f'Here is a list of bad words from {ctx.guild.name}:\n```\n{sentCustomList}\n```')
                except Exception:
                    await ctx.send(f"{ctx.message.author.mention}, I couldn't send you the list. This is because either you cannot accept direct messages, or because the list exists, but is empty.")
                else:
                    await ctx.send(f"Sent list of bad words to {ctx.message.author.mention}. Check your messages.")

@bot.command(name='toggleFilterNSFW', aliases=['toggleNSFW'])
async def toggleFilterNSFW(message):
    if message.author.guild_permissions.administrator:
        currentList = 'nsfwfilter-disabled.txt'
        if os.path.exists(currentList):
            pass
        else:
            try:
                open(currentList, 'a').close()
            except OSError:
                await message.channel.send("Failed to create list file!")
                return
            else:
                await message.channel.send("Created list file!")
        with open('nsfwfilter-disabled.txt', 'r') as file:
            nsfwServers = file.read()
            if not f"{message.guild.id}" in nsfwServers:
                with open('nsfwfilter-disabled.txt', 'a') as file:
                    file.write(f"{message.guild.id}\n")
                    #print(f"Added {message.guild.id} to the list of servers that are free of nsfw scanning.")
                    await message.channel.send("NSFW Filter has been disabled!")
                return
            elif f"{message.guild.id}" in nsfwServers:
                with open('nsfwfilter-disabled.txt', 'w') as file:
                    newNSFWServers = nsfwServers.replace(f'{message.guild.id}\n', '')
                    file.write(f"{newNSFWServers}")
                    #print(f"Removed {message.guild.id} from the list of scan-free servers.")
                    await message.channel.send("NSFW Filter has been enabled!")
    else:
        await message.channel.send(f"You don't have permissions for that, {message.author.mention}!")

# Toggles the YouTube Shorts formatter
@bot.command(name='toggleFilterYT', aliases=['toggleYT'])
async def toggleFilterNSFW(message):
    if message.author.guild_permissions.administrator:
        currentList = 'ytfilter-disabled.txt'
        if os.path.exists(currentList):
                pass
        else:
            try:
                open(currentList, 'a').close()
            except OSError:
                await message.channel.send("Failed to create list file!")
                return
            else:
                await message.channel.send("Created list file!")
        with open('ytfilter-disabled.txt', 'r') as file:
            ytServers = file.read()
            if not f"{message.guild.id}" in ytServers:
                with open('ytfilter-disabled.txt', 'a') as file:
                    file.write(f"{message.guild.id}\n")
                    #print(f"Added {message.guild.id} to the list of servers that are free of yt scanning.")
                    await message.channel.send("YT Formatter has been disabled!")
                return
            elif f"{message.guild.id}" in ytServers:
                with open('ytfilter-disabled.txt', 'w') as file:
                    newYTServers = ytServers.replace(f'{message.guild.id}\n', '')
                    file.write(f"{newYTServers}")
                    #print(f"Removed {message.guild.id} from the list of YT scan-free servers.")
                    await message.channel.send("YT Formatter has been enabled!")
    else:
        await message.channel.send(f"You don't have permissions for that, {message.author.mention}!")

@bot.command(name='dragoninstall', aliases=['214214H', '214214S', 'sakkai', '632146S'])
async def dragoninstall(ctx):
    installs = [
        'https://cdn.discordapp.com/attachments/848668986258489354/935570976295501844/dragoninstall.gif',
        'https://cdn.discordapp.com/attachments/848668986258489354/935571234228424805/nice-balls.gif'
    ]
    install = random.choice(installs)
    await ctx.send(f"{install}")

##
##
## AUTOMATED TASKS
##
##

@bot.listen()
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if "https://media.discordapp.net" in message.content: # Discord handling
        newLink = message.content.replace('media.discordapp.net', 'cdn.discordapp.com')
        await message.delete() # Delete the message
        await message.channel.send(f"From {message.author.mention} {newLink}") # Mention the user with an updated link
    if "hi braixen" in message.content.lower() or "hewwo braixen" in message.content.lower():
        braixPhrases = [
            'hi uwu',
            'uwu',
        ]
        await message.channel.send(f"{random.choice(braixPhrases)}")
    if "obama" in message.content.lower():
        await message.channel.send(f"{message.author.mention} obama")
    
    with open('ytfilter-disabled.txt', 'r') as file:
        ytServers = file.read()
        if f"{message.guild.id}" in ytServers:
            #print("filter disabled")
            return
        if "youtube.com/shorts/" in message.content: # Shorts handling
            newLink = message.content.replace('shorts/', 'watch?v=')
            newestLink = newLink.replace('?feature=share', '')
            await message.delete() # Delete the message
            await message.channel.send(f"From {message.author.mention} {newestLink}") # Mention the user with an updated link
            
    with open('nsfwfilter-disabled.txt', 'r') as file:
        customList = f'customLists/{message.guild.id}-NSFW.txt'
        nsfwServers = file.read()
        if f"{message.guild.id}" in nsfwServers or message.channel.is_nsfw():
            pass
        else:
            with open("nsfwlinks.txt", "r") as linklist:
                if os.path.exists(customList):
                    with open(customList, "r") as otherlinklist:
                        links = linklist.read().splitlines() + otherlinklist.read().splitlines()
                else:
                    links = linklist.read().splitlines()
                for word in links: # NSFW Handling
                    if word in message.content:
                        randomIPLinks = [ # A list of IP grabber memes to choose from
                            'https://cdn.discordapp.com/attachments/848668986258489354/935382738679263262/neco-arc-ip-address.mp4',
                            'https://cdn.discordapp.com/attachments/848668986258489354/935383696108838942/ip-potato-quality.mp4',
                            'https://cdn.discordapp.com/attachments/850585083652210748/935548361648517251/captain-underpants-ip-address.mp4'
                        ]
                        await message.delete() # Delete the user's message
                        await message.channel.send(f"{message.author.mention} {random.choice(randomIPLinks)}") # Ping them with an IP grabber meme

    with open('bannedwords.txt', 'r') as file:
            customList = f'customLists/{message.guild.id}-GLOBAL.txt'
            with open("bannedwords.txt", "r") as linklist:
                if os.path.exists(customList):
                    with open(customList, "r") as otherlinklist:
                        links = linklist.read().splitlines() + otherlinklist.read().splitlines()
                else:
                    links = linklist.read().splitlines()
                for word in links:
                    if word in message.content:
                        await message.delete() # Delete the user's message
                        await message.channel.send(f"{message.author.mention} you aren't allowed to say that.")
                        try:
                            await message.author.send(f'Your message in {message.guild.name} was deleted for containing "{word}"')
                        except Exception:
                            pass
    # LEVELS
    # Previous levels implementation was hot garbage, replacing it before going any further
##
##
## DEBUG COMMANDS
##
##

@bot.command()
@commands.has_permissions(administrator = True)
async def permission(ctx):
    await ctx.send('You have administrator access...')

@bot.event
async def on_ready():
    # Show GPL Notice
    print(f"{agplNotice}\n")
    # File System Check that occurs automatically
    fileNumber = 0
    for repeat_count in range(4):
        fileNumber += 1
        if fileNumber == 1:
            currentFile = "nsfwfilter-disabled.txt"
        elif fileNumber == 2:
            currentFile = "ytfilter-disabled.txt"
        elif fileNumber == 3:
            currentFile = "nsfwlinks.txt"
        elif fileNumber == 4:
            currentFile = "bannedwords.txt"
        if os.path.exists(currentFile):
            #print(f"{currentFile} found")
            pass
        else:
            try:
                open(currentFile, 'a').close()
            except OSError:
                #print(f"Failed to create file {currentFile}")
                return
            else:
                #print(f"Created file {currentFile}")
                pass
        if os.path.exists("customLists"):
            if os.path.isfile("customLists"):
                #print("File found where directory should be")
                os.remove("customLists")
                try:
                    os.mkdir("customLists")
                except OSError:
                    return
                    #print("Failed to create custom list directory")
                else:
                    pass
                    #print("Created directory")
            elif os.path.isdir("customLists"):
                #print("Found custom lists directory")
                pass
        else:
            try:
                os.mkdir("customLists")
            except OSError:
                #print("Failed to create custom list directory")
                return
    games = [
        "Persona 2: Innocent Sin",
        "GUILTY GEAR XX ACCENT CORE PLUS R",
        "Metal Gear Solid",
        "METAL GEAR RISING REVENGEANCE",
        "Shin Megami Tensei V",
        "Yoshi Commits Tax Fraud",
        "Duck Game",
        "pressure-vessel-wrapper",
        "kekcroc",
        "Yu-Gi-Oh! Master Duel"
    ]
    await bot.change_presence(activity=discord.Game(name=f"{random.choice(games)}"))

bot.run(TOKEN)
