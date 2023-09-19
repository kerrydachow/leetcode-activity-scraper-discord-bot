from discord import Embed
from discord.ext import commands
from models import Client
from config import EMBED_SUBMISSIONS_COLOR


async def send_submission_embed(ctx, user: list[str | dict]):
    """
    Print the user's last submissions as a Discord embed.

    :param ctx: discord context
    :param user: user's last submission details
    :return: None
    """
    embed = Embed(title=user[0], color=EMBED_SUBMISSIONS_COLOR)
    for problem_name, timestamp in user[1].items():
        embed.add_field(name=problem_name, value=timestamp,
                        inline=False)
    await ctx.send(embed=embed)


class LeetCode(commands.Cog):
    """
    LeetCode discord commands.
    """

    def __init__(self, bot):
        self.bot = bot
        self.leetcode_client = Client()

    @commands.command(name="add")
    async def add(self, ctx, person):
        """
        Add user to LeetCode client's list of users.

        :param ctx: discord context
        :param person: LeetCode username
        :return: None
        """
        is_added = self.leetcode_client.add_user(person)
        if is_added:
            await ctx.send(f"Successfully added `{person}` to my list!")
        else:
            await ctx.send(f"`{person}` already exists in my list.")

    @commands.command(name="remove")
    async def remove(self, ctx, person):
        """
        Remove user from LeetCode client's list of users.

        :param ctx: discord context
        :param person: LeetCode username
        :return: None
        """
        is_removed = self.leetcode_client.remove_user(person)
        if is_removed:
            await ctx.send(f"Successfully removed `{person}` from my list!")
        else:
            await ctx.send(f"`{person}` does not exist in my list.")

    @commands.command(name="list")
    async def get_list(self, ctx):
        """
        Print the current list of users on discord.

        :param ctx: discord context
        :return: None
        """
        users = "\n".join(self.leetcode_client.get_users())
        response = f"Current users are:\n>>> {users}"
        await ctx.send(response)

    @commands.command(name="scrape")
    async def scrape(self, ctx, person=None):
        """
        Scrape user(s) LeetCode submissions.

        :param ctx: discord context
        :param person: optional parameter to scrape 1 user
        :return: None
        """
        if person:
            try:
                user = self.leetcode_client.execute_request(3, person)
                await send_submission_embed(ctx, user)
            except KeyError:
                await ctx.send(f"`{person}` does not exist.")

        elif len(self.leetcode_client.get_users()) > 0:
            try:
                self.leetcode_client.execute_request(1)
                res = self.leetcode_client.execute_request(2)
                for user in res:
                    await send_submission_embed(ctx, user)
            except KeyError:
                await ctx.send(f"Invalid user exists in list.")
        else:
            help_message = f"List is empty. Use `!scrape <username>` " \
                           f"to scrape a user or add user to list using " \
                           f"`!add <username>`."
            await ctx.send(help_message)


async def setup(bot: commands.Bot):
    """
    Setup discord bot COGs with LeetCode commands.

    :param bot: discord bot
    :return: None
    """
    await bot.add_cog(LeetCode(bot))
