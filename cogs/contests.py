import requests
from datetime import datetime
from discord import *
from discord.ext import commands
from bs4 import BeautifulSoup


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


def codeforces_contests_given_by_user(handle: str) -> Embed:
    url = f"https://codeforces.com/api/user.rating?handle={handle}"
    response = requests.get(url)
    data = response.json()

    if data["status"] != "OK":
        return Embed(
            title="Error",
            description="Error fetching data from Codeforces API",
            color=0xFF0000,
        )

    contests = sorted(
        data["result"], key=lambda x: x["ratingUpdateTimeSeconds"], reverse=True
    )

    recent_contests = contests[:5]

    embed = Embed(
        title=f"Recent contests of {handle}",
        description="Here are the 5 most recent contests participated in by the user:",
        color=0x00FF00,
    )

    for contest in recent_contests:
        contest_name = contest["contestName"]
        rank = contest["rank"]
        old_rating = contest["oldRating"]
        new_rating = contest["newRating"]
        diff = new_rating - old_rating

        field_name = "Contest Details"
        field_value = f"**Contest:** {contest_name}\n"
        field_value += f"**Rank:** {rank}\n"
        field_value += f"**Old Rating:** {old_rating}\n"
        field_value += f"**New Rating:** {new_rating}\n"
        field_value += f"**Diff:** {diff}"

        embed.add_field(name=field_name, value=field_value, inline=False)

    return embed


def atcoder_contests_given_by_user(username: str):
    url = f"https://atcoder.jp/users/{username}/history"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    contest_rows = soup.select("table#history tbody tr")
    contests = []
    for row in contest_rows:
        date = row.select_one("td[data-order]").text.strip()
        contest_name = row.select_one("td.text-left a").text.strip()
        rank = row.select_one("td:nth-child(3) a").text.strip()
        performance = row.select_one("td:nth-child(4)").text.strip()
        new_rating = row.select_one("td:nth-child(5) span").text.strip()
        diff = row.select_one("td:nth-child(6)").text.strip()

        contests.append(
            {
                "Date": date,
                "Contest": contest_name,
                "Rank": rank,
                "Performance": performance,
                "New Rating": new_rating,
                "Diff": diff,
            }
        )
    embed = Embed(
        title="Contest History",
        description="Here are the contests participated in by the user:",
        color=0x00FF00,
    )

    for contest in contests:
        contest_name = contest["Contest"]
        start_time = contest["Date"]
        rank = contest["Rank"]
        performance = contest["Performance"]
        new_rating = contest["New Rating"]
        diff = contest["Diff"]

        field_name = "Contest Details"
        field_value = f"**Contest:** {contest_name}\n"
        field_value += f"**Start Time:** {start_time}\n"
        field_value += f"**Rank:** {rank}\n"
        field_value += f"**Performance:** {performance}\n"
        field_value += f"**New Rating:** {new_rating}\n"
        field_value += f"**Diff:** {diff}"

        embed.add_field(name=field_name, value=field_value, inline=False)

    return embed


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

        await ctx.respond(embed=response)

    @commands.slash_command(
        description="Get the list of the recent 5 contests given by you on the website "
    )
    async def recent_contest(self, ctx: commands.Context, website: str, username: str):
        website_to_function = {
            "codeforces": codeforces_contests_given_by_user,
            "atcoder": atcoder_contests_given_by_user,
        }

        if website.lower().rstrip().lstrip() in website_to_function:
            embed = website_to_function[website](username)
            if embed is None:
                await ctx.respond("Invalid username")
                return
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("Invalid Website")


def setup(bot: commands.Bot):
    bot.add_cog(contests(bot))
