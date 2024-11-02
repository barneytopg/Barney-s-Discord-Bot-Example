from discord.ext import commands
from discord.ext.commands import Context
import aiohttp
import random
import asyncpraw
import discord
from core import keys

# Here we name the cog and create a new class for the cog.
class Images(commands.Cog, name="images"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.error_message = ":x: **An API error occured. Probably just a hiccup.\nIf this error persist for several days, please report it.**"
        self.reddit = asyncpraw.Reddit(
            client_id=keys.get_REDID(),
            client_secret=keys.get_REDSECRET(),
            user_agent=keys.get_REDUSERAGENT(),
        )

    @commands.hybrid_command(
        name="cat",
        description="Summon a image of a cat",
    )
    async def cat(self, context: Context) -> None:
        """
        Summon a image of a cat
        """

        wait_msg = await context.send("**One moment please :heart:**")

        subreddit = await self.reddit.subreddit("catpics")
        posts = []
        async for post in subreddit.hot(limit=200):
            if post.url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                posts.append(post)
        if posts:
            random_post = random.choice(posts)


            embed = discord.Embed(
                color=0x7ed1e6,
            )
            embed.set_image(url=random_post.url
                )
            embed.set_footer(text=f"Requested by {context.author}")
            await wait_msg.edit(embed=embed)

        else:
            await wait_msg.edit(":x: **Sorry, I can't get images at the moment :sad:**")


async def setup(bot) -> None:
    await bot.add_cog(Images(bot))
