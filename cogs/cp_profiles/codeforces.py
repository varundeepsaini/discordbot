from discord import Embed
from discord.ext import commands
import requests


def codeforces_embed(formatted_response: dict):
    embed = Embed(
        title="Codeforces Profile",
        description="Here is your Codeforces Profile.",
        color=0x00FF00,
    )
    keys = formatted_response.keys()
    handle = formatted_response["handle"]
    if "firstName" in keys:
        name = formatted_response["firstName"] + " " + formatted_response["lastName"]
        embed.add_field(name="Name", value=name, inline=False)
    if "rank" in keys:
        rank = formatted_response["rank"]
        embed.add_field(name="Rank", value=rank.capitalize(), inline=False)

    if "maxRank" in keys:
        max_rank = formatted_response["maxRank"]
        embed.add_field(name="Max Rank", value=max_rank.capitalize(), inline=False)

    if "rating" in keys:
        rating = formatted_response["rating"]
        max_rating = formatted_response["maxRating"]
        embed.add_field(name="Max Rating", value=max_rating, inline=False)
    else:
        rating = "*unrated*"
    profile_url = f"https://codeforces.com/profile/{handle}"

    embed.add_field(name="Rating", value=rating, inline=False)
    embed.add_field(name="Handle", value=f"[{handle}]({profile_url})", inline=False)

    return embed


class codeforces(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="Get Your Codeforces Profile")
    async def codeforces(self, ctx: commands.Context, username: str):
        formatted_response = Embed(
            title="Codeforces Profile",
            description="Here is your Codeforces Profile.",
            color=0x00FF00,
        )
        url = f"https://codeforces.com/api/user.info?handles={username}"
        formatted_response = requests.get(url)
        if formatted_response.status_code != 200:
            print(
                f"Failed to get data from API. Status code: {formatted_response.status_code}"
            )
            return
        try:
            data = formatted_response.json()
        except ValueError:
            print("Failed to decode JSON data from API response.")
            return
        if data["status"] == "FAILED":
            await ctx.respond("Invalid username")
            return
        else:
            embed = codeforces_embed(data["result"][0])

        await ctx.respond(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(codeforces(bot))
