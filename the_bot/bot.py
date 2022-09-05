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
# bot = hikari.GatewayBot(os.getenv("DISCORD_TOKEN") or "") # base hikari
bot = lightbulb.BotApp(
    os.getenv("DISCORD_TOKEN") or "",
    default_enabled_guilds=(955796331375517787),  # only this server
)

# - Bot events -
@bot.command
@lightbulb.option("desc", "Description")
@lightbulb.option("title", "Title")
@lightbulb.command("temp2", "Post GitHub Issue")
@lightbulb.implements(lightbulb.SlashCommand)
async def temp2(ctx):
    logger.info(f"New issue from {ctx.author.username}")  # or .user?

    GITHUB_USER = os.environ.get("GITHUB_USER")
    GITHUB_PASS = os.environ.get("GITHUB_PASS")
    REPO_OWNER = os.environ.get("REPO_OWNER")
    REPO_NAME = os.environ.get("REPO_NAME")

    issue = {
        "title": ctx.options.title,
        "body": ctx.options.desc,
        "assignee": GITHUB_USER,
        "labels": ["Discord", "Under Consideration"],
    }
    url = "https://api.github.com/repos/%s/%s/issues" % (REPO_OWNER, REPO_NAME)
    # Create an authenticated session to create the issue
    session = requests.Session()
    session.auth = (GITHUB_USER, GITHUB_PASS)

    response = session.post(url, json.dumps(issue))
    if response.status_code == 201:
        logger.info('Successfully created Issue "%s"' % ctx.options.title)
        resp_obj = json.loads(response.content)
        logger.info("Response: ", resp_obj["url"])
    else:
        logger.info('Could not create Issue "%s"' % ctx.options.title)
        logger.info("Response: ", response.content)

    await ctx.respond("Conditional response here with issue #")


def main():
    """Entrypoint for the Discord Bot."""
    load_dotenv()
    bot.run()
