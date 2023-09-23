from discord import ApplicationContext, Bot
from utils.env import DISCORD_BOT_TOKEN

bot  = Bot()

@bot.command(description="Pinggg")
async def ping(ctx: ApplicationContext):
    await ctx.respond(f"Pong! Latency is {bot.latency}")

@bot.event
async def on_ready():
    print("Saini Certified is online.")

bot.run(DISCORD_BOT_TOKEN)