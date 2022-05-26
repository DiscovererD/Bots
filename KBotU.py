import discord 
from discord.ext import commands
from discord.utils import get
from asyncio import sleep
import aiohttp
import datetime
import warnings
import random

client = commands.Bot(command_prefix = ['Boob, ', 'Boob ', 'B ', 'b '])
warnings.filterwarnings("ignore", category=DeprecationWarning)
intents = discord.Intents.all()
client.session = aiohttp.ClientSession()

@client.command()
async def Hi(ctx):
	greet = [
	"I love seeing you happy and my biggest reward is seeing you smile =w=",
	"I only saw you for a second, but it made my day. ＼(≧▽≦)／",
	"My love for you keeps increasing every second. o(≧▽≦)o",
	"I love the way you love me ヽ(>∀<☆)ノ",
	"You are so good to me … what did I ever do to deserve you? (＞ｍ＜)",
	"Loving you is like breathing. I can’t stop and it’s necessary for my survival. (´｡• ᵕ •｡) ♡",
	]
	await ctx.send(random.choice(greet))

@client.event
async def on_message(ctx):
	if "https:" in (ctx.content):
		if ctx.content.count("https:") > 5:
			msg = await ctx.channel.send("Split up your message in many links?")
			await msg.add_reaction("✅")
			await msg.add_reaction("❌")
			await sleep(10)
			cache_msg = discord.utils.get(client.cached_messages, id = msg.id)
			if cache_msg.reactions[0].count > 1:
				c = ctx.content
				#print(c)
				c = c.split("\n")
				cnum = len(c)
				#print(cnum)
				for i in range(0, cnum):
					if c[i] != '':
						await ctx.channel.send(c[i])
				await ctx.delete()
		else:
			await client.process_commands(ctx)
	else:
		await client.process_commands(ctx)

	
@client.command()
async def Vmute(ctx, member: discord.Member):
	msg = await ctx.send(f"**MUTE** POLL by {ctx.author.mention}!\nShould we mute {'<@' + str(member.id) + '>'}?\nIf YES put ✅. If NO put ❌.")
	await msg.add_reaction("✅")
	await msg.add_reaction("❌")
	await sleep(2)
	cache_msg = discord.utils.get(client.cached_messages, id = msg.id)
	await ctx.send("You have 30 seconds to vote!")
	await sleep(30)
	print("sleep is over")
	if cache_msg.reactions[0].count > cache_msg.reactions[1].count and cache_msg.reactions[0].count > 2:
		await member.edit(mute = True)
		await ctx.send(f"{member} has been muted!")
	elif cache_msg.reactions[0].count > 2:
		await ctx.send(f"{member} has not been muted!")
	elif cache_msg.reactions[0].count <= 2 and cache_msg.reactions[1].count <= 2:
		await ctx.send("Not enough people has voted!")

@client.command()
async def VUmute(ctx, member: discord.Member):
	msg = await ctx.send(f"**UNMUTE** POLL by {ctx.author.mention}!\nShould we unmute {'<@' + str(member.id) + '>'}?\nIf YES put ✅. If NO put ❌.")
	await msg.add_reaction("✅")
	await msg.add_reaction("❌")
	await sleep(2)
	cache_msg = discord.utils.get(client.cached_messages, id = msg.id)
	await ctx.send("You have 30 seconds to vote!")
	await sleep(30)
	print("sleep is over")
	if cache_msg.reactions[0].count > cache_msg.reactions[1].count and cache_msg.reactions[0].count > 2:
		await member.edit(mute = False)
		await ctx.send(f"{member} has been unmuted!")
	elif cache_msg.reactions[0].count > 2:
		await ctx.send(f"{member} is still muted!")
	elif cache_msg.reactions[0].count <= 2 and cache_msg.reactions[1].count <= 2:
		await ctx.send("Not enough people has voted!")

async def timeout_user(*, user_id: int, guild_id: int, until):
    headers = {"Authorization": f"Bot {client.http.token}"}
    url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
    timeout = (datetime.datetime.utcnow() + datetime.timedelta(minutes=until)).isoformat()
    json = {'communication_disabled_until': timeout}
    async with client.session.patch(url, json=json, headers=headers) as session:
        if session.status in range(200, 299):
           return True
        return False

@client.command()
async def VTout(ctx: commands.Context, member: discord.Member, until: int):
	msg = await ctx.send(f"**TIMEOUT** POLL by {ctx.author.mention}!\nShould we timeout {'<@' + str(member.id) + '>'}?\nIf YES put ✅. If NO put ❌.")
	await msg.add_reaction("✅")
	await msg.add_reaction("❌")
	await sleep(2)
	cache_msg = discord.utils.get(client.cached_messages, id = msg.id)
	await ctx.send("You have 30 seconds to vote!")
	await sleep(30)
	print("sleep is over")
	if cache_msg.reactions[0].count > cache_msg.reactions[1].count and cache_msg.reactions[0].count > 2:
		handshake = await timeout_user(user_id=member.id, guild_id=ctx.guild.id, until=until)
		if handshake:
			return await ctx.send(f"Successfully timed out user for {until} minutes.")
		await ctx.send("Something went wrong")
	elif cache_msg.reactions[0].count <= 2 and cache_msg.reactions[1].count <= 2:
		await ctx.send("Not enough people has voted!")

client.remove_command('help')

@client.command()
async def help(ctx):
	embed = discord.Embed()
	embed.description = "__Here is the list of commands you can use__\n Prefix for bot - 'B', 'Boob'.\n**Hi** - say hi to the bot\n**Vmute** - mute member by starting a poll\n**VUmute** - unmute member by starting a poll\n**VTout** - timeout user by starting a poll\n **__EXAMPLES__**\n B Vmute @Knoukl\n B VTout @Knoukl 5\nFull list of commands [here](https://youtu.be/dQw4w9WgXcQ)."
	await ctx.send(embed = embed)

#---------------------------------------------------------------------------------------------#

@client.command()
@commands.is_owner()
async def SendMSG(ctx):
	msg = None
	print("Message for...")
	id = int(input())
	print("Your message...")
	while msg != 'Over':
		msg = input()
		user = await client.fetch_user(id)
		try:
			await user.send(msg)
		except:
			print("Can not deliver message")

@client.command()
@commands.is_owner()
async def timeout(ctx: commands.Context, member: discord.Member, until: int):
    handshake = await timeout_user(user_id=member.id, guild_id=ctx.guild.id, until=until)
    if handshake:
        return await ctx.send(f"Successfully timed out user for {until} minutes.")
    await ctx.send("Something went wrong")

@client.command(pass_context = True)
async def Amute(ctx, member: discord.Member):
	if ctx.message.author.guild_permissions.administrator or ctx.author.id == 597027086703656963:
		await member.edit(mute = True)

@client.command()
async def AUmute(ctx, member: discord.Member):
	if ctx.message.author.guild_permissions.administrator or ctx.author.id == 597027086703656963:
			await member.edit(mute = False)

@client.command()
@commands.is_owner()
async def restart(ctx):
    await ctx.bot.close()
    client.run('')


client.run('')

