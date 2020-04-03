import discord
import requests
from datetime import date
from datetime import timedelta
from discord.ext import commands

DISCORD_TOKEN = 'TOKEN_HERE'
AV_API_KEY = 'TOKEN_HERE'

bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
    print('Stock Bot is ready.')

@bot.command()
async def dp(ctx, *args):
    symbol = args[0]
    to_return = ''

    if len(args) > 1 and args[1].isdigit():
        num_days = int(args[1])
        if num_days > 3:
            to_return = f"breh API won't let me check more than 3 days..."
            num_days = 3
    else:
        num_days = 1

    req = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&apikey=' + AV_API_KEY)

    try:
        for x in range(0, num_days):
            if req.status_code == 200:
                result = req.json()
                data_for_all_days = result['Time Series (Daily)']
                today = data_for_all_days[f"{date.today() - timedelta(x)}"]

                to_print = f"{symbol.upper()} - {date.today() - timedelta(x)}" \
                            f"\nOpen: {today['1. open']}" \
                            f"\nHigh: {today['2. high']}" \
                            f"\nLow: {today['3. low']}" \
                            f"\nClose: {today['4. close']}" \
                            f"\nVolume: {today['5. volume']}"
                if len(to_return) > 1:
                    to_return = f"{to_return}\n\n{to_print}"
                else:
                    to_return = to_print

    except KeyError:
        await ctx.send(f"`Symbol is not valid bruh...`")

    if len(to_return) > 0:
        await ctx.send(f"```\n{to_return}\n```")


@bot.command()
async def alert():
    print('alert here')

@bot.command()
async def help():
    print('help here')

bot.run(DISCORD_TOKEN)