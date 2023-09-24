from requests import get
from discord import Embed, ApplicationContext, bot
from discord.ext import commands

def getLeetCodeEmbed(username: str) -> Embed | None:
    profile_url = f"https://leetcode.com/{username}/"
    response = get(f"https://leetcode-stats-api.herokuapp.com/{username}")
    if not response.ok:
        return None
    data = response.json()
    embed = Embed(title=username, color=0x00ff00)
    embed.set_author(name="LeetCode", icon_url="https://www.google.com/url?sa=i&url=https%3A%2F%2Fleetcode.com%2F&psig=AOvVaw1bZXtsAts5pg_h6It7I9kX&ust=1695556446675000&source=images&cd=vfe&opi=89978449&ved=0CBAQjRxqFwoTCOi11o_WwIEDFQAAAAAdAAAAABAE")
    embed.add_field(name="Handle", value=f"[{username}]({profile_url})", inline=False)
    embed.add_field(name="Ranking", value=data['ranking'], inline=False)
    embed.add_field(name="Total Solved", value=f"{data['totalSolved']} / {data['totalQuestions']}", inline=False)
    embed.add_field(name="Percentage Solved", value=f"{round(100 * data['totalSolved'] / data['totalQuestions'], 2)}%", inline=False)
    embed.add_field(name="Total Easy Solved", value=f"{data['easySolved']} / {data['totalEasy']}", inline=False)
    embed.add_field(name="Percentage Easy Solved", value=f"{round(100 *  data['easySolved']/ data['totalEasy'], 2)}%", inline=False)
    embed.add_field(name="Total Medium Solved", value=f"{data['mediumSolved']} / {data['totalMedium']}", inline=False)
    embed.add_field(name="Percentage Medium Solved", value=f"{round(100 * data['mediumSolved'] / data['totalMedium'], 2)}%",inline=False)
    embed.add_field(name="Total Hard Solved", value=f"{data['hardSolved']} / {data['totalHard']}", inline=False)
    embed.add_field(name="Percentage Hard Solved", value=f"{round(100 * data['hardSolved'] / data['totalHard'], 2)}%", inline=False)
    embed.add_field(name="Acceptance Rate", value=f"{data['acceptanceRate']}%", inline=False)
    return embed
        
class LeetCode(commands.Cog):

    @commands.slash_command()
    async def leetcode(self, ctx: ApplicationContext, username: str):
        profile = getLeetCodeEmbed(username)
        if (profile is None):
            await ctx.respond("Invalid username")
            return
        await ctx.respond(embed=profile)

def setup(bot: bot.Bot):
    bot.add_cog(LeetCode(bot))