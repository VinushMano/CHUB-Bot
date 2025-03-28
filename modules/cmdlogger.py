import disnake

import config
from modules import misc

log_msgs: dict[int, disnake.Message] = {}


async def on_slash_command(inter: disnake.AppCmdInter):
    full_command = misc.make_cmd_str(inter)
    print(f'{inter.author.name} used {full_command}')
    embed = disnake.Embed(
        color=disnake.Color.red(),
        title=full_command[:256],
        description="Command is still processing or has crashed..."
    )
    embed.set_author(
        icon_url=inter.author.display_avatar,
        name=f"{inter.author.display_name} ({inter.author.name} | {inter.author.id})"
    )
    if inter.guild:
        embed.set_footer(
            icon_url=inter.guild.icon if inter.guild else inter.author.avatar,
            text=f"{inter.guild.name} ({inter.guild.id})"
        )
        
    else:
        embed.set_footer(
            text='DMs'
        )
    view = disnake.ui.View()
    message = await inter.original_message()
    if message:
        view.add_item(disnake.ui.Button(
            label="View Message",
            url=message.jump_url,
            style=disnake.ButtonStyle.link
        ))
    channel = inter.bot.get_channel(config.LOG_CHANNEL)
    log_msgs[inter.id] = await channel.send(embed=embed, view=view) # type: ignore


async def on_slash_command_completion(inter: disnake.AppCmdInter):
    if inter.id not in log_msgs:
        return
    # ping = round(inter.created_at.timestamp() - time.time())
    msg = log_msgs[inter.id]
    og_embed = msg.embeds[0]
    og_embed.description = f"Command finished. Response (if applicable) is attached."
    og_embed.colour = disnake.Color.green()
    embeds = [og_embed]
    try:
        response = await inter.original_response()
    except disnake.NotFound:
        # this means the slash command timed out (usually an internet issue or hypixel api rate limiting)
        return
    embeds.extend(response.embeds)
    await msg.edit(embeds=embeds)
