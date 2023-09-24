import random
import discord
import requests
from datetime import datetime
from discord import *
from discord.ext import commands


def fetch_upcoming_contests():
    url = "https://kontests.net/api/v1/all"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to get data from API. Status code: {response.status_code}")
        return []

    try:
        data = response.json()
    except ValueError:
        print("Failed to decode JSON data from API response.")
        return []

    print(data)  # For debugging
    upcoming_contests = []
    current_time = datetime.utcnow().strftime(
        "%Y-%m-%dT%H:%M:%S.%fZ"
    )  # Get current time in UTC
    count = 0
    for contestList in data:
        if (
            "name" in contestList
            and "start_time" in contestList
            and "end_time" in contestList
        ):
            start_time_str = contestList["start_time"]
            end_time_str = contestList["end_time"]

            if (
                start_time_str > current_time and count < 7
            ):  # Check if the contest is after the current time
                try:
                    start_time = datetime.strptime(
                        start_time_str, "%Y-%m-%dT%H:%M:%S.%fZ"
                    )
                    end_time = datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                except ValueError:
                    print(
                        f"Could not parse date-time string: {start_time_str} or {end_time_str}"
                    )
                    continue

                upcoming_contests.append(
                    {
                        "Name": contestList["name"],
                        "Start Time": start_time.strftime(
                            "%H:%M %d-%m-%Y"
                        ),  # Format the datetime object to a string
                        "End Time": end_time.strftime(
                            "%H:%M %d-%m-%Y"
                        ),  # Format the datetime object to a string
                        "Site": contestList["site"],
                        "URL": contestList["url"],
                    }
                )
                count += 1

    return upcoming_contests


class contests(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="Get the list of all the Upcoming Contests")
    async def upcoming_contest(self, ctx: commands.Context):
        contest_item = fetch_upcoming_contests()
        response = Embed(
            title="Upcoming Contests",
            description="Here are some upcoming coding contests.",
            color=0x00FF00,
        )

        for contestList in contest_item:
            contest_name = contestList["Name"]
            contest_url = contestList.get("URL", "No URL provided")
            start_time = contestList["Start Time"]
            end_time = contestList["End Time"]
            site = contestList["Site"]

            field_name = "Contest Details"
            field_value = (
                f"[{contest_name}]({contest_url})\n"  # Hyperlink the contest name
            )
            field_value += f"Start Time: {start_time}\n"
            field_value += f"End Time: {end_time}\n"
            field_value += f"Site: {site}"

            response.add_field(name=field_name, value=field_value, inline=False)

        await ctx.send(embed=response)


def setup(bot: commands.Bot):
    bot.add_cog(contests(bot))
