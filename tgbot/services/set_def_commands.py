from aiogram import Bot, types

async def set_default_commands(bot: Bot):
    await bot.set_my_commands(
        [
            types.BotCommand(command="start",description= "Run the bot"),
            types.BotCommand(command= "help",description= "Display Help"),
            types.BotCommand(command= "common",description= "Get the most common cryptocurrencies"), 
        ]
    )