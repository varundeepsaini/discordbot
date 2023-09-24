from discord.ext import commands
from discord import ApplicationContext
from codeforces_api import CodeforcesApi
from datetime import datetime
from utils.mongo import problems_collection


class DailyCP(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cf_api = CodeforcesApi()

    @commands.slash_command(description="Get your daily challenge")
    async def daily_cp(self, ctx: ApplicationContext):
        user_id = ctx.author.id
        dateAndTime = datetime.now()
        date = dateAndTime.date()
        today_problems = problems_collection.find_one(
            {"discord_id": user_id, "date": date}
        )
        if today_problems is not None:
            given_problems = today_problems.problems
            await ctx.respond(
                f"problem 1 (same rating) - {given_problems[0].link}\nproblem 1 (highger rating) - {given_problems[1].link}"
            )
            return


def setup(bot):
    bot.add_cog(DailyCP(bot))
