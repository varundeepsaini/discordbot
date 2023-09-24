from discord import ApplicationContext, Bot
from utils.env import DISCORD_BOT_TOKEN
from utils.mongo import user_collection
import os

bot = Bot()


@bot.command(description="Pinggg")
async def ping(ctx: ApplicationContext):
    await ctx.respond(f"Pong! Latency is {bot.latency}")


@bot.event
async def on_ready():
    print(f"Saini Certified is online.")


@bot.command(description="register for daily cp questions")
async def register(ctx: ApplicationContext):
    if user_collection.find_one({"discord_id": ctx.author.id}) is not None:
        await ctx.respond(f"Already Registered")
        return
    user_collection.insert_one(
        {"discord_id": ctx.author.id, "discord_username": ctx.author.name}
    )
    await ctx.respond("Registered!")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        print(f"Loaded {filename[:-3]} cog")
    else:
        for subFileName in os.listdir(f"./cogs/{filename}"):
            if subFileName.endswith(".py"):
                bot.load_extension(f"cogs.{filename}.{subFileName[:-3]}")
                print(f"Loaded {filename}.{subFileName[:-3]} cog")


bot.run(DISCORD_BOT_TOKEN)
