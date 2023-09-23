from discord import ApplicationContext, Bot
from utils.env import DISCORD_BOT_TOKEN
import os
bot = Bot()


@bot.command(description="Pinggg")
async def ping(ctx: ApplicationContext):
    await ctx.respond(f"Pong! Latency is {bot.latency}")


@bot.event
async def on_ready():
    print(f"Saini Certified is online.")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded {filename[:-3]} cog')
    else:
        for subFileName in os.listdir(f'./cogs/{filename}'):
            if subFileName.endswith('.py'):
                bot.load_extension(f'cogs.{filename}.{subFileName[:-3]}')
                print(f'Loaded {filename}.{subFileName[:-3]} cog')


bot.run(DISCORD_BOT_TOKEN)
