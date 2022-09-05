"""Discord Bot.
Adapted from https://github.com/lionel-panhaleux/archon-bot/tree/master/archon_bot
"""
import logging
import os

import hikari

# Logger
logger = logging.getLogger()
logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG") else logging.INFO,
    format="[%(asctime)s][%(levelname)s]: %(message)s",
)

# Discord client
bot = hikari.GatewayBot(os.getenv("DISCORD_TOKEN") or "")

# Bot events
@bot.listen()
async def on_ready(event: hikari.StartedEvent) -> None:
    """Login success informative log."""
    logger.info("Ready as %s", bot.get_me().username)
    

@bot.listen()
async def on_connected(event: hikari.GuildAvailableEvent) -> None:
    """Connected to a guild."""
    logger.info("Logged in %s as %s", event.guild.name, bot.get_me().username)


async def _interaction_response(instance, interaction, content):
    """Default response to interaction (in case of error)"""


@bot.listen()
async def on_interaction(event: hikari.InteractionCreateEvent) -> None:
    """Handle interactions (slash commands)."""
    logger.info("Interaction %s", event.interaction)
    if not event.interaction.guild_id:
        await _interaction_response(
            event.interaction,
            "Bot cannot be used in a private channel",
        )
        return
    if event.interaction.type == hikari.InteractionType.APPLICATION_COMMAND:
        pass

    elif event.interaction.type == hikari.InteractionType.MESSAGE_COMPONENT:
        pass


def main():
    """Entrypoint for the Discord Bot."""
    bot.run()
