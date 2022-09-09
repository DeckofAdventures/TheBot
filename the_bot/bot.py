"""Discord Bot.
Adapted from https://github.com/lionel-panhaleux/archon-bot/tree/master/archon_bot
"""
import os
import json
import logging
import requests
from dotenv import load_dotenv

# import hikari
import lightbulb

# Logger
logger = logging.getLogger()
logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG") else logging.INFO,
    format="[%(asctime)s][%(levelname)s]: %(message)s",
)

# - Discord client -
load_dotenv()
load_dotenv("TheBot/the_bot/.env")
# bot = hikari.GatewayBot(os.getenv("DISCORD_TOKEN") or "") # base hikari
bot = lightbulb.BotApp(
    token=os.getenv("DISCORD_TOKEN"),
    # default_enabled_guilds=(os.getenv("GUILD_ID")),  # only this server
    logs="DEBUG",
)

# - Bot events -
@bot.command
@lightbulb.option("desc", "Description")
@lightbulb.option("title", "Title")
@lightbulb.command("feedback", "Post GitHub Issue")
@lightbulb.implements(lightbulb.SlashCommand)
async def feedback(ctx):
    if load_dotenv() or load_dotenv("TheBot/the_bot/.env"):
        GITHUB_USER = os.environ.get("GITHUB_USER")
        GITHUB_PASS = os.environ.get("GITHUB_TOKEN")
        REPO_OWNER = os.environ.get("REPO_OWNER")
        REPO_NAME = os.environ.get("REPO_NAME")
        if not all([GITHUB_USER, GITHUB_PASS, REPO_OWNER, REPO_NAME]):
            logger.error("Could not find all credentials")
            return
    else:
        logger.error("Could not find env file")
        return

    logger.info(f"New issue from {ctx.author.username}")  # or .user?
    issue = {
        "title": ctx.options.title,
        "body": ctx.options.desc + f"\n\nPosted by {ctx.author.username}",
        "assignee": GITHUB_USER,  # assigned to user who provided credentials
        "labels": ["DiscordBot", "Under Consideration"],
    }
    url = "https://api.github.com/repos/%s/%s/issues" % (REPO_OWNER, REPO_NAME)
    # Create an authenticated session to create the issue
    session = requests.Session()
    session.auth = (GITHUB_USER, GITHUB_PASS)

    response = session.post(url, json.dumps(issue))
    if response.status_code == 201:
        logger.info('Successfully created Issue "%s"' % ctx.options.title)
        resp_url = json.loads(response.content)["html_url"]
        await ctx.respond(f"Issue URL: {resp_url}")
    else:
        logger.error("Response: ", response.content)
        await ctx.respond(
            'Could not create Issue "%s". Please contact Admin.' % ctx.options.title
        )


def main():
    """Entrypoint for the Discord Bot."""
    if load_dotenv() or load_dotenv("TheBot/the_bot/.env"):
        logger.info("Credentials loaded")
    else:
        logger.error("Could not find credentials")
        return
    bot.run()


if __name__ == "__main__":
    main()
