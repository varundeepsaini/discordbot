import discord
from discord import Embed
import responses

intents = discord.Intents.default()
intents.message_content = True


async def send_message(message, user_message):
    try:
        response = responses.handleResponse(user_message)
        if response:
            if isinstance(response, Embed):  # Check if the response is an Embed object
                await message.channel.send(embed=response)
            else:
                await message.channel.send(response)
    except Exception as e:
        print(e)
        await message.channel.send("An error occurred")


def run_discord_bot():
    TokenFile = open("token.txt", "r")
    token = TokenFile.read()
    TokenFile.close()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} is ready and running")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username}: {user_message} ({channel})")

        if user_message[:2] == "a!":
            user_message = user_message[2:]
            await send_message(message, user_message)

    client.run(token)
