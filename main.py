import os
import nextcord
from nextcord.ext import commands
from gtts import gTTS

bot = commands.Bot(command_prefix="!", description='Simple TTS bot')

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.event
async def on_message(message):
    if nextcord.utils.get(bot.voice_clients, guild=message.guild) is None:
        channel = message.author.voice.channel
        await channel.connect()
    if message.channel.id == os.getenv('CHANNEL'):
        guilds = message.guild
        myobj = gTTS(text=message.content, lang='ru', slow=False)
        myobj.save("message.mp3")
        source = nextcord.PCMVolumeTransformer(nextcord.FFmpegPCMAudio('message.mp3'))
        guilds.voice_client.play(source, after=None)
    await bot.process_commands(message)

bot.run(os.getenv('BOT_TOKEN'))
