from discord import *
from discord.ext import commands
import requests


def codeforces_embed(formatted_response):
    handle = formatted_response['result'][0]['handle']
    name = formatted_response['result'][0]['firstName'] + " " + formatted_response['result'][0]['lastName']
    rank = formatted_response['result'][0]['rank']
    max_rank = formatted_response['result'][0]['maxRank']
    rating = formatted_response['result'][0]['rating']
    max_rating = formatted_response['result'][0]['maxRating']
    profile_url = f"https://codeforces.com/profile/{handle}"

    embed = Embed(title="Codeforces Profile", description="Here is your Codeforces Profile.", color=0x00ff00)
    embed.add_field(name="Name", value=name, inline=False)
    embed.add_field(name="Handle", value=f"[{handle}]({profile_url})", inline=False)  # hyperlink the handle
    embed.add_field(name="Rating", value=rating, inline=False)
    embed.add_field(name="Rank", value=rank.capitalize(), inline=False)
    embed.add_field(name="Max Rating", value=max_rating, inline=False)
    embed.add_field(name="Max Rank", value=max_rank.capitalize(), inline=False)

    return embed


class codeforces(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="Get Your Codeforces Profile")
    async def codeforces(self, ctx: commands.Context, username: str):
        formatted_response = Embed(title="Codeforces Profile", description="Here is your Codeforces Profile.",
                                   color=0x00ff00)
        url = f"https://codeforces.com/api/user.info?handles={username}"
        formatted_response = requests.get(url)
        if formatted_response.status_code != 200:
            print(f"Failed to get data from API. Status code: {formatted_response.status_code}")
            return []
        try:
            data = formatted_response.json()
        except ValueError:
            print("Failed to decode JSON data from API response.")
            return []
        print(data)
        if data['status'] == "FAILED":
            await ctx.send("Invalid username")
            return
        else:
            embed = codeforces_embed(data)

        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(codeforces(bot))
