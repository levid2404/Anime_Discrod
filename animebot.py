import json
import random
import requests
import discord
from discord.ext import commands

bot = discord.Client
bot = commands.Bot(command_prefix='$')

AnimeList = ['Fate', 'KonoSuba: God’s Blessing on this Wonderful World!', 'Inuyasha', 'Cowboy Bebop', 'Yu-Gi-Oh!', 'Code Geass', 'My Hero Academia', 'Steins;Gate', 'Tokyo Ghoul',
'OreGairu: My Teen Romantic Comedy SNAFU', 'The Melancholy of Haruhi Suzumiya', 'Detective Conan', 'Laid-Back Camp', 'Violet Evergarden', 'Attack on Titan', 'Fullmetal Alchemist', 'Anohana: The Flower We Saw That Day',
'Love Live!', 'Ghost in the Shell', 'Dragon Ball', 'Death Note', 'Pokémon', 'Re:Zero -Starting Life in Another World-', 'JoJo’s Bizarre Adventure', 'Neon Genesis Evangelion', 'One Piece', 'Monogatari Series', 'Clannad', 'Naruto', ' Demon Slayer: Kimetsu no Yaiba']

def get_anime_quote():
    response2 = requests.get("https://animechanapi.xyz/api/quotes/random")
    raw_quote = response2.content
    quote_json = json.loads(raw_quote)
    data = quote_json['data']
    data2 = data[0]
    quoteAnime = data2['quote']
    character = data2['character']
    anime = data2['anime']
    anime_quote = quoteAnime + " - " + character + " from " + anime
    return anime_quote

def AnimeRec():
    anime_rec = random.choice(AnimeList)
    return anime_rec

@bot.command(description="Pong!")
async def ping(ctx):
    print(f"{bot.user.name} has executed a command!")
    latency = bot.latency
    await ctx.send(f'pong {latency}')


@bot.command(description="Random Anime Quote")
async def animequote(ctx):
    FirstQuote = get_anime_quote()
    SelfQuote, character = FirstQuote.split('- ')
    CheckPointChar = character
    RealChar, Anime = CheckPointChar.split('from ')
    embedVar = discord.Embed(title=Anime,color=0x00ff00)
    embedVar.add_field(name=RealChar, value=SelfQuote)
    await ctx.send(embed=embedVar)

@bot.command(description="Anime Recommendation!")
async def recommend(ctx):
    rec = AnimeRec()
    embedVar = discord.Embed(name="Recommendation!", color=0x00ff00)
    embedVar.add_field(name="You can watch!", value=rec)
    await ctx.send(embed=embedVar)

@bot.command(description="Kick a user!")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)

@bot.command(description="Ban a User")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}")

@bot.command(description="Unban a user!")
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.name}#{user.discriminator}")
            return


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(status=discord.Status.online,activity=discord.Game("Anime"))

@bot.event
async def on_message(message):
    if message.content.startswith('Hello Anime Bot'):
        await message.channel.send("Hello!")
    await bot.process_commands(message)