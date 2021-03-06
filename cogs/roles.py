import discord
from discord.ext import commands

role_message = 0  # add id of the role message here


def setup(bot: commands.Bot):
    bot.add_cog(Roles(bot=bot))


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @property
    def lvl_20_role(self):
        return self.bot.guild.get_role(611734174017257485)

    @property
    def roles(self) -> dict:
        return {
            # emoji_id: role_id
            736112775352287232: self.bot.guild.get_role(740689745532682290),  # python
            737030552770576395: self.bot.guild.get_role(740691624979333272),  # csharp
            740694148876599409: self.bot.guild.get_role(740690985926787093),  # js
            740694256053911675: self.bot.guild.get_role(740690527325782038),  # java
            740694321216356564: self.bot.guild.get_role(740691348977352754),  # ruby
        }

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        if reaction.message.id != role_message:
            return

        if any(role in user.roles for role in self.roles.values()) or self.lvl_20_role not in user.roles:
            return await reaction.remove()

        await user.add_roles(self.roles[reaction.emoji.id])
        try:
            await user.send(f"Gave you the **{self.roles[reaction.emoji.id].name}** role!")
        except discord.HTTPException:
            pass

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User):
        if reaction.message.id != role_message:
            return

        if self.roles[reaction.emoji.id] not in user.roles or self.lvl_20_role not in user.roles:
            return

        await user.remove_roles(self.roles[reaction.emoji.id])
        try:
            await user.send(f"Removed your **{self.roles[reaction.emoji.id].name}** role!")
        except discord.HTTPException:
            pass
