#Refbot

import discord
import random
import string
import requests
from discord.ext import commands
from pprint import pprint

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a+b)

@bot.command()
async def multiply(ctx, a: int, b: int):
    await ctx.send(a*b)

@bot.command()
async def greet(ctx):
    await ctx.send(":smiley: :wave: Hello, there!")

@bot.command()
async def cat(ctx):
    await ctx.send("https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif")

@bot.command()
async def roll(ctx, dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    if "3" in result.split():
        await ctx.send("THREE!!!!")
    else:
    	await ctx.send(result)

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="nice bot", description="Nicest bot there is ever.", color=0xeee657)

    # give info about you here
    embed.add_field(name="Author", value="<YOUR-USERNAME>")

    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    # give users a link to invite thsi bot to their server
    embed.add_field(name="Invite", value="[Invite link](<insert your OAuth invitation link here>)")

    await ctx.send(embed=embed)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="nice bot", description="A Very Nice bot. List of commands are:", color=0xeee657)

    embed.add_field(name="$add X Y", value="Gives the addition of **X** and **Y**", inline=False)
    embed.add_field(name="$multiply X Y", value="Gives the multiplication of **X** and **Y**", inline=False)
    embed.add_field(name="$greet", value="Gives a nice greet message", inline=False)
    embed.add_field(name="$cat", value="Gives a cute cat gif to lighten up the mood.", inline=False)
    embed.add_field(name="$info", value="Gives a little info about the bot", inline=False)
    embed.add_field(name="$help", value="Gives this message", inline=False)
    embed.add_field(name="$roll NdN", value="Rolls dice", inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def simpsons(ctx):
    url = "https://frinkiac.com/api/random"
    r = requests.get(url, verify=True)
    dic = r.json()
    await ctx.send("https://frinkiac.com/img/"+dic["Frame"]["Episode"]+"/"+str(dic["Frame"]["Timestamp"])+".jpg")

@bot.command()
async def futurama(ctx):
    url = "https://morbotron.com/api/random"
    r = requests.get(url, verify=True)
    dic = r.json()
    await ctx.send("https://morbotron.com/img/"+dic["Frame"]["Episode"]+"/"+str(dic["Frame"]["Timestamp"])+".jpg")

@bot.command()
async def poop(ctx):
    await ctx.send("https://i.kinja-img.com/gawker-media/image/upload/s--eg2Q6azC--/c_scale,fl_progressive,q_80,w_800/183ob861iy0ckjpg.jpg")


@bot.event
async def on_message(message):
    words = message.content.split(" ")
    if "I'm" in words[0]:
    	if any(word in words[1] for word in ("cold", "tired", "hungry", "bored")):
            await message.channel.send("You're " + words[1] +"!?! Feel THESE nipples!")


    #lets the commands continue working
    await bot.process_commands(message)

#Checks for changes in Members' voice states and logs it in the 'log' channel
@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel != before.channel:
        for channel in bot.get_all_channels():
            if channel.name == "log":
                if before.channel != None:
                    await channel.send(member.name + " left " + before.channel.name)
                if after.channel != None:
                    await channel.send(member.name + " joined " + after.channel.name)

    if before.self_mute != after.self_mute:
        for channel in bot.get_all_channels():
            if channel.name == "log":
                if after.self_mute:
                    await channel.send(member.name + " has muted")
                if not after.self_mute:
                    await channel.send(member.name + " has unmuted")

    if before.self_deaf != after.self_deaf:
        for channel in bot.get_all_channels():
            if channel.name == "log":
                if after.self_deaf:
                    await channel.send(member.name + " has deafened")
                if not after.self_deaf:
                    await channel.send(member.name + " has deafened")







token_filename = "token.txt"
token_file = open(token_filename, "r")
for line in token_file:
    token = line

bot.run(token.strip())
