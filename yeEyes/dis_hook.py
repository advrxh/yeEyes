import discord_webhook
from discord import File

from yeEyes.settings import HOOK_URL


class Hook:
    def __init__(self) -> None:
        self.hook = discord_webhook.DiscordWebhook(HOOK_URL)

    def notify(self, loc):
        self.embed = discord_webhook.DiscordEmbed(
            title="Motion Detected 👇", color="ff070b"
        )

        self.hook.add_embed(self.embed)
        self.hook.execute()
        self.hook.remove_embeds()

        with open(loc, "rb") as f:
            self.hook.add_file(file=f.read(), filename="clip.gif")

        self.hook.execute()
        self.hook.remove_files()
