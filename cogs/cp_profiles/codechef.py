from discord import *
from discord.ext import commands
import requests


def codechef_embed(formatted_response, handle: str):
    name = formatted_response["name"]
    rating = formatted_response["currentRating"]
    max_rating = formatted_response["highestRating"]
    stars = formatted_response["stars"][:1]
    global_rank = formatted_response["globalRank"]
    country_rank = formatted_response["countryRank"]
    profile_url = f"https://www.codechef.com/users/{handle}"

    embed = Embed(
        title="Codechef Profile",
        description="Here is your Codechef Profile.",
        color=0x00FF00,
    )
    embed.add_field(name="Name", value=name, inline=False)
    embed.add_field(
        name="Handle", value=f"[{handle}]({profile_url})", inline=False
    )  # hyperlink the handle
    embed.add_field(name="Rating", value=rating, inline=False)
    embed.add_field(name="Max Rating", value=max_rating, inline=False)
    embed.add_field(name="Stars", value=stars, inline=False)
    embed.add_field(name="Global Rank", value=global_rank, inline=False)
    embed.add_field(name="Country Rank", value=country_rank, inline=False)

    return embed


class codechef(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="Get Your CodeChef Profile")
    async def codechef(self, ctx: commands.Context, handle: str):
        url = f"https://codechef-api.vercel.app/{handle}"
        response = requests.get(url)
        formatted_response = response.json()
        print(formatted_response)
        """
        Sample Response from API: 
        {'success': True, 'profile': 
        'https://cdn.codechef.com/sites/default/files/uploads/pictures/60948f5631d5838ad84e18af4e753b14.jpeg', 
        'name': 'varundeepsaini', 'currentRating': 1309, 'highestRating': 1309, 'countryFlag': 
        'https://cdn.codechef.com/download/flags/24/in.png', 'countryName': 'India', 'globalRank': 66569, 'countryRank': 
        61804, 'stars': '1★'}
        """
        if formatted_response["success"]:
            embed = codechef_embed(formatted_response, handle)
            await ctx.respond(embed=embed)
            return
        else:
            await ctx.respond("Invalid username")


def setup(bot: commands.Bot):
    bot.add_cog(codechef(bot))
