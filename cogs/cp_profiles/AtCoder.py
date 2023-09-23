from requests import get
from bs4 import BeautifulSoup
from discord import Embed, Colour,  ApplicationContext, bot
from discord.ext import commands

class AtCoderProfile:
    success = False
    def __init__(self, username: str):
        response = get(f"https://atcoder.jp/users/{username}")
        if not response.ok:
            self.success = False
            return
        soup = BeautifulSoup(response.content, 'html5lib')
        self.username = soup.find('a', attrs={'class': 'username'}).contents[0].getText()
        self.kyu = soup.find('div', attrs={'id': 'main-container'}).find('h3').find('b').contents[0]
        statsRows = soup.findAll('div', attrs={'id': 'main-container', 'class': 'container'})[0].findAll('table')[1].findAll('tr')
        self.rank = statsRows[0].td.getText()
        self.rating = statsRows[1].td.span.getText()
        self.highestRating = statsRows[2].td.span.getText()
        self.ratedMatches = statsRows[3].td.getText()
        self.success = True
    
    def embed(self):
        embed = Embed(title=self.username, color=Colour.dark_grey())
        embed.set_author(name="AtCoder", icon_url="https://img.atcoder.jp/assets/icon/avatar.png")
        embed.add_field(name="", value=f"**{self.kyu}**", inline=False)
        embed.add_field(name="Rank", value=self.rank)
        embed.add_field(name="Rated Matches", value=self.ratedMatches)
        embed.add_field(name="Rating", value=self.rating)
        embed.add_field(name="Highest Rating", value=self.highestRating)
        return embed

class AtCoder(commands.Cog):

    @commands.slash_command()
    async def at_coder(self, ctx: ApplicationContext, username: str):
        profile = AtCoderProfile(username)
        if (not profile.success):
            await ctx.respond("Invalid username")
            return
        await ctx.respond(embed=profile.embed())

def setup(bot: bot.Bot):
    bot.add_cog(AtCoder(bot))