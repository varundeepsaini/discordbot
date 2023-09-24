from discord.ext import commands
from discord import Interaction, ApplicationContext
from codeforces_api import CodeforcesApi
from datetime import datetime
from utils.mongo import problems_collection, user_collection
from utils.codeforces import getTwoProblems
from requests import get


class DailyCP(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cf_api = CodeforcesApi()

    @commands.slash_command(description="Get your daily challenge")
    async def daily_cp(self, ctx: Interaction | ApplicationContext):
        await ctx.response.defer()
        user_id = ctx.author.id
        dateAndTime = datetime.now()
        date = dateAndTime.strftime("%d/%m/%Y")
        user_obj = user_collection.find_one({"discord_id": user_id})
        if user_obj is None:
            await ctx.respond("First you need to register using `/register` command")
        today_problems = problems_collection.find_one(
            {"discord_id": user_id, "date": date}
        )
        if today_problems is not None:
            given_problems = today_problems["problems"]
            msg = f"problem 1 - {given_problems[0]['link']}\nproblem 1 - {given_problems[1]['link']}"
            await ctx.respond(msg)
            return
        username = user_obj["username"]
        url = f"https://codeforces.com/api/user.info?handles={username}"
        formatted_response = get(url)
        if formatted_response.status_code != 200:
            await ctx.respond("Oopsie, an error occurred")
            return
        try:
            data = formatted_response.json()
        except ValueError:
            await ctx.respond("Oopsie, an error occurred")
            return
        if "rating" not in data["result"][0]:
            await ctx.respond("Skill Issue: you are unrated")
            return
        new_problems = getTwoProblems(username, data["result"][0]["rating"])
        new_problems_doc = {
            "discord_id": user_id,
            "problems": [
                {
                    "contestId": new_problems[0]["contestId"],
                    "index": new_problems[0]["index"],
                    "link": f"https://codeforces.com/problemset/problem/{new_problems[0]['contestId']}/{new_problems[0]['index']}",
                },
                {
                    "contestId": new_problems[1]["contestId"],
                    "index": new_problems[1]["index"],
                    "link": f"https://codeforces.com/problemset/problem/{new_problems[1]['contestId']}/{new_problems[1]['index']}",
                },
            ],
            "date": date,
        }
        problems_collection.insert_one(new_problems_doc)
        msg = f"problem 1 - {new_problems_doc['problems'][0]['link']}\nproblem 2 - {new_problems_doc['problems'][1]['link']}"
        await ctx.respond(msg)


def setup(bot):
    bot.add_cog(DailyCP(bot))
